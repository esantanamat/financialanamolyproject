import json
from decimal import Decimal
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FinancialExpenses')

def lambda_handler(event, context):
    body = json.loads(event['body'])

    transaction = {
        'user_id': body['user_id'],
        'amount': Decimal(str(body['amount'])),
        'date': body['date'],
        'category': body['category'],
        'merchant': body['merchant'],
        'transaction_id': body['transaction_id'],
        'flagged': body['flagged']
    }
    
    table.put_item(Item=transaction)


    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Transaction added successfully'})
    }