from beem import Hive
from datetime import datetime
from time import sleep
from src.modules.splinterlands_actions import get_sps_balance
from src.modules.goals_actions import get_goals_balance
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

def stake_goals(hive: Hive, hive_name: str, glx: float):
  json_data = {
    "token": "GLX",
    "qty": glx,
    "to_player": hive_name,
  }

  try:
    hive.custom_json("gls-plat-stake_tokens", required_auths=[hive_name], json_data=json_data)
    sleep(BLOCK_WAIT_TIME) 
  except Exception as e:
    log(f"ERROR: Staking GOALS for {hive_name}")
    log(f"{e}")
    return

  if glx == 0:
    log(f"{datetime.now()} | {hive_name} | Claiming GOALS staking rewards")
    new_balance = get_goals_balance(hive_name)
    log(f"{datetime.now()} | {hive_name} | New balance GOALS {new_balance}")
  else:
    log(f"{datetime.now()} | {hive_name} | Staked GOALS {glx}")

def stake_goals_packs(hive: Hive, hive_name: str, amount: float):
  json_data = {
    "token": "GMLSPA",
    "qty": amount,
  }

  try:
    hive.custom_json("gls-plat-stake_tokens", required_auths=[hive_name], json_data=json_data)
    sleep(BLOCK_WAIT_TIME) 
  except Exception as e:
    log(f"ERROR: Staking GOALS Packs for {hive_name}")
    log(f"{e}")
    return

  if amount == 0:
    log(f"{datetime.now()} | {hive_name} | Claiming GOALS Packs staking rewards")
    new_balance = get_goals_balance(hive_name)
    log(f"{datetime.now()} | {hive_name} | New balance GOALS Packs {new_balance}")
  else:
    log(f"{datetime.now()} | {hive_name} | Staked GOALS Packs {amount}")

def stake_goals_nodes(hive: Hive, hive_name: str, amount: float):
  json_data = {
    "token": "GLSNODE",
    "qty": amount,
  }

  try:
    hive.custom_json("gls-plat-stake_tokens", required_auths=[hive_name], json_data=json_data)
    sleep(BLOCK_WAIT_TIME) 
  except Exception as e:
    log(f"ERROR: Staking GOALS Nodes for {hive_name}")
    log(f"{e}")
    return

  if amount == 0:
    log(f"{datetime.now()} | {hive_name} | Claiming GOALS Nodes staking rewards")
    new_balance = get_goals_balance(hive_name)
    log(f"{datetime.now()} | {hive_name} | New balance GOALS Nodes {new_balance}")
  else:
    log(f"{datetime.now()} | {hive_name} | Staked GOALS Nodes {amount}")