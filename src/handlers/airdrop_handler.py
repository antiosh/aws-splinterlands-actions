from src.modules.process_config import process_config_tasks

CONFIG_FILE_NAME = 'src/handlers/airdrop_config.yaml'
AWS_WRITEABLE_DIRECTORY_PATH = '/tmp'

def run(event, context):
    try:
        process_config_tasks(CONFIG_FILE_NAME, AWS_WRITEABLE_DIRECTORY_PATH)
    except:
        print('Failed!')
        raise
    else:
        print('Passed!')
