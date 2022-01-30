from beem import Hive
from datetime import datetime
from time import sleep
from src.modules.splinterlands_actions import get_sps_balance
from src.modules.logger import log

APP_NAME = 'splinterlands-actions'
BLOCK_WAIT_TIME = 4 # wait time for block to be broadcast and received

def stake(hive: Hive, hive_name: str, sps: float):
  json_data = {
    "token": "SPS",
    "qty": sps,
    "app": APP_NAME
  }

  try:
    hive.custom_json("sm_stake_tokens", required_posting_auths=[hive_name], json_data=json_data)
    sleep(BLOCK_WAIT_TIME) 
  except Exception as e:
    log(f"ERROR: Staking for {hive_name}")
    log(f"{e}")
    return

  if sps == 0:
    log(f"{datetime.now()} | {hive_name} | Claiming staking rewards")
    new_balance = get_sps_balance(hive_name)
    log(f"{datetime.now()} | {hive_name} | New balance {new_balance}")
  else:
    log(f"{datetime.now()} | {hive_name} | Staked {sps}")

def transfer_token_to_player(hive: Hive, hive_name: str, sps: float, receiver: str):
  if sps == 0:
    return
  json_data = {
    "to": receiver,
    "memo": receiver,
    "qty": sps,
    "token": "SPS",
    "type": "withdraw",
    "app": APP_NAME
  }

  try:
    hive.custom_json("sm_token_transfer", required_auths=[hive_name], json_data=json_data)
    sleep(BLOCK_WAIT_TIME) 
  except Exception as e:
    log(f"ERROR: Transfering SPS for {hive_name}")
    log(f"{e}")
    return

  log(f"{datetime.now()} | {hive_name} | Transferred {sps} SPS to {receiver}")