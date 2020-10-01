import json
import os
import logging
import datetime
import boto3
from botocore.exceptions import ClientError
import sys

logger = logging.getLogger()
logger.setLevel('INFO')


class DecimalEncoder(json.JSONEncoder):
    # Helper class to convert a DynamoDB item to JSON.
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def query(message_id):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    logger.info(table_name)
    table = dynamodb.Table(table_name)
    try:
        resp = table.get_item(
            Key={
                'message_id': message_id
            }
        )
        # logger.info(json.dumps(resp))
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return None
    else:
        item = resp['Item'] if 'Item' in resp else None
        if item:
            logger.info("Got item")
            logger.info(json.dumps(item, indent=4, cls=DecimalEncoder))
        else:
            logger.info("No item")
        return item


def lambda_handler(event, context):
    logger.info(json.dumps(event))
    message_id = event['pathParameters']['proxy']
    logger.info('message_id={}'.format(message_id))
    resp = query(message_id)
    if not resp:
        # empty return - no message_id found
        return {
            'statusCode': 200,
            'headers': {
                'content-type': 'application/json'
            },
            'body': json.dumps({
                'result': 'message_id not found',
                'message_id': message_id
            })
        }
    # OK we got message_id, check it's status
    if 'confirm_code' in resp:
        # cooking conpleted
        return {
            'statusCode': 200,
            'headers': {
                'content-type': 'application/json'
            },
            'body': json.dumps({
                'result': 'booking completed',
                'confirm_code': resp['confirm_code'],
                'message_id': resp['message_id']
            })
        }
    else:
        # message_id exists but booking not completed
        return {
            'statusCode': 200,
            'headers': {
                'content-type': 'application/json'
            },
            'body': json.dumps({
                'result': 'booking still in the process',
                'message_id': message_id
            })
        }
