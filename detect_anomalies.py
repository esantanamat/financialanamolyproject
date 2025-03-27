import boto3
import pickle
import pandas as pd
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FinancialExpenses')

def load_model():
    with open("anomaly_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model



def preprocess_transaction(transaction):
    df = pd.DataFrame([transaction])
    df['cost'] = df['cost'].astype(float)
    return df[['cost']]


def detect_anomaly(transaction):
    model = load_model()
    test = preprocess_transaction(transaction)
    user_id = transaction['user_id']
    date_transaction_id = transaction['date_transaction_id']
    prediction = model.predict(test)
    is_anomalous = prediction[0] == -1

    response = table.update_item(
        Key={"user_id": user_id, "date_transaction_id": date_transaction_id},  # Composite key
        UpdateExpression="SET flagged = :flag",
        ExpressionAttributeValues={":flag": int(is_anomalous)},
        ReturnValues="UPDATED_NEW"
    )
    return {"anomaly" : is_anomalous, "updated": response['Attributes']}

def lambda_handler(event, context):
    try:
      
        transaction = json.loads(event['body'])
        result = detect_anomaly(transaction)

        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Transaction processed successfully',
                'anomalous': result["anomalous"],
                'updated': result["updated"]
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal Server Error',
                'error': str(e)
            })
        }