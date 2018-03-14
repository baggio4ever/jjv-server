import json
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key,Attr


def hello(event, context):
    if "headers" in event:
        if "origin" in event["headers"]:
            origin = event["headers"]["origin"]  # どこから聞かれても返せるように
        else:
            origin = ""
    else:
        origin = ""

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":origin
        }
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def post_log(event, context):
    if "headers" in event:
        if "origin" in event["headers"]:
            origin = event["headers"]["origin"]  # どこから聞かれても返せるように
        else:
            origin = ""
    else:
        origin = ""

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dev-jjv')

    yy = json.loads(event["body"])

    user_id = yy["user_id"]
    dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')
    message = yy["message"]
    comment = yy["comment"]

    table.put_item(
        Item={
            "user_id": user_id,
            "created_at": dt,
            "message": message,
            "comment": comment
        }
    )

    xx = json.loads(
        '''
        {
            "user_id":"taro",
            "message":"よこはまたそがれ"
        }
        '''
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":origin
        }
    }

    return response
