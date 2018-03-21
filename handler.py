import json
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key,Attr

DYNAMO_TABLE_NAME = "dev-jjv"

SERVER_NAME = "jjv-server"
SERVER_VERSION = "0.1.2"


def hello(event, context):
    body = {
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }

    return response


def upload(event, context):

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( DYNAMO_TABLE_NAME )

    yy = json.loads(event["body"])

    user_id = yy["user_id"]
    dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')
    filename = yy["filename"]
    xml = yy["xml"]
    comment = yy["comment"]
    upload_date = yy["upload_date"]

    table.put_item(
        Item={
            "user_id": user_id,
            "created_at": dt,
            "filename": filename,
            "xml": xml,
            "comment": comment,
            "upload_date": upload_date
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }

    return response



'''
user_idがuploadしたファイルの一覧を返す
クエリー文字列で渡す

user_id=xxxx な感じ

{
    user_id: xxxx
}

'''

def get_files(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( DYNAMO_TABLE_NAME )

    if( event["queryStringParameters"] is not None ):
        params = event["queryStringParameters"]
        user_id = params.get("user_id")
        if user_id is not None:
            response = table.query(
                        KeyConditionExpression=Key('user_id').eq( user_id )
                    )

            items = response['Items']
        else:
            items = ["a","b"]
    else:
        items = ["x","Z"]


    body = {
        "files": items,
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }

    return response


'''
user_id + creaeted_at で一意に決まるファイルを返す
クエリー文字列で渡す

user_id=xxxx&created_at=yyyyyyy な感じ

{
    user_id: xxxx
    created_at: yyyyy
}

'''

def download(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( DYNAMO_TABLE_NAME )

    if( event["queryStringParameters"] is not None ):
        params = event["queryStringParameters"]
        user_id = params.get("user_id")
        created_at = params.get("created_at")
        if user_id is not None:
            response = table.get_item(
                Key={
                    'user_id': user_id,
                    'created_at': created_at
                }
                    )

            item = response['Item']
        else:
            item = ["a","b"]
    else:
        item = ["x","Z"]

    body = {
        "result": item,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }

    return response
