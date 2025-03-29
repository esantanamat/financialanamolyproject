import boto3
import pickle
import pandas as pd
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FinancialExpenses')

def load_model():
    print("Loading model...")  
    try:
        
        with open("anomaly_model.pkl", "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully.") 
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def preprocess_transaction(transaction):
    print(f"Preprocessing transaction: {transaction}")  
    try:
        df = pd.DataFrame([transaction])
        df['cost'] = df['cost'].astype(float)
        print(f"Processed transaction data: {df}")  
        return df[['cost']]
    except Exception as e:
        print(f"Error preprocessing transaction: {str(e)}")
        raise

def detect_anomaly(transaction):
    print(f"Detecting anomaly for transaction: {transaction}") 
    try:
        model = load_model()
        test = preprocess_transaction(transaction)
        user_id = transaction['user_id']
        date_transaction_id = transaction['date_transaction_id']
        print(f"Predicting anomaly for user_id: {user_id}, date_transaction_id: {date_transaction_id}") 
        prediction = model.predict(test)
        is_anomalous = bool(prediction[0] == -1)
        print(f"Prediction result: {is_anomalous}")  
     
        response = table.update_item(
            Key={"user_id": user_id, "date_transaction_id": date_transaction_id}, 
            UpdateExpression="SET flagged = :flag",
            ExpressionAttributeValues={":flag": str(is_anomalous).lower()},
            ReturnValues="UPDATED_NEW"
        )
        print(f"DynamoDB update response: {response}")  
        return {"anomaly": is_anomalous, "updated": response['Attributes']}
    except Exception as e:
        print(f"Error detecting anomaly: {str(e)}")
        raise

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")  
    try:
       
        transaction = json.loads(event['body'])
        print(f"Transaction to process: {transaction}")  

        result = detect_anomaly(transaction)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Transaction processed successfully',
                'anomalous': result["anomaly"],
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
