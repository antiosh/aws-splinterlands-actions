from slack import WebClient
from slack.errors import SlackApiError

def send_slack_message(token: str, channel: str, message: str,):
    client = WebClient(token=token)
    try:
        client.chat_postMessage(channel=f'#{channel}', text=message)
    except SlackApiError as e:
        print(f"SLACK ERROR: {e.response['error']}")
        print(f"Unable to send message ({message}) to {channel}")