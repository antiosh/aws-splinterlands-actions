import beemgraphenebase.ecdsasig
from binascii import hexlify
from datetime import datetime
from time import time
from time import sleep
import requests
from src.modules.logger import log

AIRDROP_CLAIM_WAIT_TIME = 20

def get_sps_balance(hive_name: str):
  balances = []
  try:
    balances = requests.get(f'https://api2.splinterlands.com/players/balances?username={hive_name}').json()
  except Exception as e:
    log(f"ERROR: Could not fetch Splinterlands balances for {hive_name}")
    log(f"{e}")
    return 0
  sps = 0
  for balance in balances:
    if balance['token'] == 'SPS':
      sps = balance['balance']
      break

  return sps

def claim_hive_sps_airdrop(hive_name: str, posting_key: str):
  timestamp = int(time() * 1000)
  sig_bytes = beemgraphenebase.ecdsasig.sign_message(f"{hive_name}{timestamp}", posting_key)
  signature = hexlify(sig_bytes).decode("ascii")
  token = None
  try:
    login_response = requests.get(f"https://api2.splinterlands.com/players/login?name={hive_name}&ts={timestamp}"
                                  f"&sig={signature}").json()
    token = login_response['token']
  except Exception as e:
    log(f"ERROR: Could not log in to Splinterlands for token with account {hive_name}")
    log(f"{e}")
    return

  # Claim Airdrop
  try:
    claim_sig_bytes = beemgraphenebase.ecdsasig.sign_message(f"hive{hive_name}{timestamp}", posting_key)
    claim_signature = hexlify(claim_sig_bytes).decode("ascii")
    result = requests.get(f"https://ec-api.splinterlands.com/players/claim_sps_airdrop?platform=hive&address={hive_name}"
                 f"&sig={claim_signature}&token={token}&username={hive_name}&ts={timestamp}")
    json = result.json()
    if json['success'] is True:
      sleep(AIRDROP_CLAIM_WAIT_TIME) 
      log(f"{datetime.now()} | {hive_name} | Claimed SPS Airdrop from HIVE Assets")

  except Exception as e:
    log(f"ERROR: Could not claim HIVE SPS airdrop with account {hive_name}")
    log(f"Reason: {json['error']}")
    return