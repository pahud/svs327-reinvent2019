import boto3
import json
import os
import logging
import datetime

logger = logging.getLogger()
logger.setLevel('INFO')


def lambda_handler(event, context):
    logger.info(json.dumps(event))
    payload = [{
        'queue_id': e['messageId'],
        'body': e['body'],
        'sent_ts': e['attributes']['SentTimestamp']}
        for e in event['Records']]
    logger.info(payload)
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    logger.info(table_name)
    table = dynamodb.Table(table_name)
    for i in payload:
        i['booking_status'] = 'new'
        i['booking_created_at'] = datetime.datetime.utcnow().isoformat()
        i['body'] = json.loads(i['body'])
        i['message_id'] = i['body']['MessageId']
        resp = table.put_item(
            Item=i)
        logger.info(resp)

    return 'OK'
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         'status': 'message processed'
    #     }, indent=2),
    # }
