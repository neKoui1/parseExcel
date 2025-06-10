import logging
import boto3
import csv

from botocore.exceptions import ClientError
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

aws_access_key_id2=config['Azure']['AWS_ACCESS_KEY_ID']
aws_secret_access_key2=config['Azure']['AWS_SECRET_ACCESS_KEY']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def converse(brt, model_id, user_message):
    conversation = [
        {
            'role': 'user',
            'content':[
                {
                    'text':user_message
                }
            ]
        }
    ]
    try:
        response=brt.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                'temperature':0.5,
                'topP':0.9,
            }
        )

        return response['output']['message']['content'][0]['text']
    except(ClientError, Exception) as e:
        print(f'ERROR: Cant invoke {model_id}. Reason: {e}')
        raise

def main():
    with open('./zhu_accessKeys.csv', 'r', encoding='utf-8') as f:
        keylist=[v for v in csv.reader(f, skipinitialspace=True)]
    f.close()

    aws_access_key_id=keylist[1][0]
    aws_secret_access_key=keylist[1][1]
    brt=boto3.client(
        'bedrock-runtime',
        aws_access_key_id=aws_access_key_id2,
        aws_secret_access_key=aws_secret_access_key2,
        region_name='us-east-1',
    )
    model_id="anthropic.claude-sonnet-4-20250514-v1:0"
    message = "Describe the purpose of a 'hello world' program in one line."
    response = converse(brt, model_id, message)
    print(f'Response: {response}')
    logger.info('Done.')

main()
