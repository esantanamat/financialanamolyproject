import json
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("FinancialExpenses")

def lambda_handler(event, context):
    if "queryStringParameters" not in event or "user_id" not in event["queryStringParameters"]:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Missing user_id in query parameters"})
        }

    user_id = event["queryStringParameters"]["user_id"]

  
    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
        
    }
