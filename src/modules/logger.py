from src.modules.slack_client import send_slack_message

SLACK_TOKEN = None
SLACK_CHANNEL = None

def init_logger(slack_token, slack_channel):
  if slack_token is not None:
    global SLACK_TOKEN
    SLACK_TOKEN = slack_token
    
  global SLACK_CHANNEL
  SLACK_CHANNEL = slack_channel

def log(message: str, ):
  if SLACK_TOKEN is None:
    print(message)
  else:
    send_slack_message(SLACK_TOKEN, SLACK_CHANNEL, message)

