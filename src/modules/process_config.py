from beem import Hive
from beem.account import Account
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
from src.modules.logger import *
from src.modules.splinterlands_actions import *
from src.modules.goals_actions import *
from src.modules.hive_actions import *

DEFAULT_SLACK_CHANNEL = 'splinterlands-updates'

def setup_logger(config):
  slack_token = None
  if 'slack-token' in config:
    slack_token = config['slack-token']
  if 'slack-channel' in config:
    slack_channel = config['slack-channel']
  else:
    slack_channel = DEFAULT_SLACK_CHANNEL
  init_logger(slack_token, slack_channel)

def process_config_tasks(config_file_name: str, writeable_directory_path: str = None):
    with open(config_file_name) as config_file:
        config = yaml.load(config_file, Loader=SafeLoader)
        setup_logger(config)
        hive_node = config['hive-node']
        for account in config['accounts']:
            hive_name = account['name']
            keys = []
            has_active_key = False
            if 'posting-key' in account.keys():
              keys.append(account['posting-key'])
            if 'active-key' in account.keys():
              has_active_key = True
              keys.append(account['active-key'])
            
            if len(keys) == 0:
              log(f"ERROR: No keys for {hive_name}")
              continue
            
            log(f"Applying {config_file_name} for {hive_name}")
            if writeable_directory_path is None:
              hive = Hive(keys=keys, node=hive_node, blocking='irreversible')
            else:
              hive = Hive(keys=keys, node=hive_node, blocking='irreversible', data_dir=writeable_directory_path)
            hive_account = Account(hive_name, blockchain_instance=hive)
            
            for action in account['actions']:
                if action == 'claim-hive-sps-airdrop':
                    claim_hive_sps_airdrop(hive_name, account['posting-key'])
                elif action == 'claim-staking-rewards':
                    stake(hive, hive_name, 0)
                elif action == 'stake':
                    sps = get_sps_balance(hive_name)
                    stake(hive, hive_name, sps)
                elif action == 'claim-staking-rewards-goals':
                    stake_goals(hive, hive_name, 0)
                elif action == 'claim-staking-rewards-goals-packs':
                    stake_goals_packs(hive, hive_name, 0)
                elif action == 'stake-goals':
                    glx = get_goals_balance(hive_name)
                    stake_goals(hive, hive_name, glx)
                elif 'transfer-sps-to-player' in action:
                    if has_active_key:
                      player_to_transfer_to = action.partition(':')[2]
                      sps = get_sps_balance(hive_name)
                      log(f"{datetime.now()} | {hive_name} | Starting transfer of {sps} SPS to {player_to_transfer_to}")
                      transfer_token_to_player(hive, hive_name, sps, player_to_transfer_to)
                    else:
                      log("ERROR: Active key is required to transfer sps")
                
                else:
                    log(f"ERROR: Invalid action ({action}) supplied for {hive_name}")
                
            log('***************************************')
