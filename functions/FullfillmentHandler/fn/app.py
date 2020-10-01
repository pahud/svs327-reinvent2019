import json
import os
import logging
import datetime
import boto3
import uuid
import sys

logger = logging.getLogger()
logger.setLevel('INFO')


def proceed_items(message_id_list):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    logger.info(table_name)
    table = dynamodb.Table(table_name)
    for m in message_id_list:
        resp = table.update_item(
            Key={
                'message_id': m
            },
            UpdateExpression="set booking_status = :r, booking_completed_at = :b, confirm_code = :c",
            ExpressionAttributeValues={
                ':r': 'completed',
                ':b': datetime.datetime.utcnow().isoformat(),
                ':c': str(uuid.uuid4())

            },
            ReturnValues="UPDATED_NEW"
        )
        logger.info(resp)


def lambda_handler(event, context):
    logger.info(json.dumps(event))
    try:
        items_to_proceed = [x['dynamodb']['NewImage']['message_id']['S']
                            for x in event['Records'] if x['eventName'] == 'INSERT']
        logger.info(items_to_proceed)
        proceed_items(items_to_proceed)
    except:
        logger.error(sys.exc_info())
