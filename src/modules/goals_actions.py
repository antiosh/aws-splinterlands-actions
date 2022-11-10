import beemgraphenebase.ecdsasig
from binascii import hexlify
from datetime import datetime
from time import time
from time import sleep
import requests
from src.modules.logger import log

AIRDROP_CLAIM_WAIT_TIME = 20

def get_goals_balance(hive_name: str):
  balances = []
  try:
    balances = requests.get(f'https://validator.genesisleaguesports.com/balances?account={hive_name}').json()
  except Exception as e:
    log(f"ERROR: Could not fetch GOALS balances for {hive_name}")
    log(f"{e}")
    return 0
  glx = 0
  for balance in balances:
    if balance['token'] == 'GLX':
      glx = balance['balance']
      break

  return glx
