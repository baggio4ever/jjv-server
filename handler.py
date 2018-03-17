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

def upload(event, context):
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


DYNAMO_TABLE_NAME = "dev-jjv"

'''
user_idがuploadしたファイルの一覧を返す
クエリー文字列で渡す

user_id=xxxx な感じ

{
    user_id: xxxx
}

'''

def get_files(event, context):
    if event["headers"] is not None:
        if "origin" in event["headers"]:
            origin = event["headers"]["origin"]  # どこから聞かれても返せるように
        else:
            origin = ""
    else:
        origin = ""

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dev-jjv')

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

#    yy = json.loads(event["queryStringParameters"])

#    user_id = yy["user_id"]

#    user_id = json.loads(event["user_id"]);

#    response = table.query(
#        KeyConditionExpression=Key('user_id').eq( user_id )
#    )
#    items = response['Items']


    body = {
        "files": items,
        "input": event,
        "origin":origin
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
    if event["headers"] is not None:
        if "origin" in event["headers"]:
            origin = event["headers"]["origin"]  # どこから聞かれても返せるように
        else:
            origin = ""
    else:
        origin = ""

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dev-jjv')

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

#    yy = json.loads(event["queryStringParameters"])

#    user_id = yy["user_id"]

#    user_id = json.loads(event["user_id"]);

#    response = table.query(
#        KeyConditionExpression=Key('user_id').eq( user_id )
#    )
#    items = response['Items']


    body = {
        "result": item,
        "input": event,
        "origin":origin
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
