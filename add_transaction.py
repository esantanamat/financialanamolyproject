import json
from decimal import Decimal
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FinancialExpenses')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    body = json.loads(event['body'])

    transaction = {
        'user_id': body['user_id'],
        'amount': Decimal(str(body['amount'])),
        'date': body['date'],
        'category': body['category'],
        'merchant': body['merchant'],
        'transaction_id': body['transaction_id'],
        'flagged': body['flagged'],
        'date_transaction_id': event['date_transaction_id']
    }
    
    table.put_item(Item=transaction)
    lambda_client.invoke(
        FunctionName='',
        InvocationType='Event',
        Payload = json.dumps(transaction)
    )


    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Transaction added successfully'})
    }