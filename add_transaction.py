import json
from decimal import Decimal
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FinancialExpenses')
lambda_client = boto3.client('lambda')

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)  
    return obj

def lambda_handler(event, context):
    body = json.loads(event['body'])


    print("Received date_transaction_id:", body.get('date_transaction_id'))

    
    if 'date_transaction_id' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing required field: date_transaction_id'})
        }

    transaction = {
        'user_id': body['user_id'],
        'cost': Decimal(str(body['amount'])),  
        'date': body['date'],
        'category': body['category'],
        'merchant': body['merchant'],
        'transaction_id': body['transaction_id'],
        'flagged': body['flagged'],
        'date_transaction_id': body['date_transaction_id']
    }

   
    try:
        table.put_item(Item=transaction)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error adding transaction', 'error': str(e)})
        }

    
    transaction_serializable = json.dumps(transaction, default=decimal_to_float)
    
    
    try:
        lambda_client.invoke(
            FunctionName='detect_anomalies_function',
            InvocationType='Event',
            Payload=transaction_serializable.encode('utf-8')
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error invoking anomaly detection function', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Transaction added successfully'})
    }