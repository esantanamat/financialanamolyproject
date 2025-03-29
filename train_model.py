import boto3
import pandas as pd
from decimal import Decimal
from sklearn.ensemble import IsolationForest
import pickle 


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FinancialExpenses')

def get_transactions():

    response = table.scan() 
    data = response.get('Items', [])

    while 'LastEvaluatedKey' in response: #dynamodb only allows 1mb per scan, need to paginate
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response.get('Items', []))

    return data

def preprocess_data(transactions):

    df = pd.DataFrame(transactions) #pandas dataframe for preprocessing
    df['cost'] = df['cost'].astype(float) 
    return df[['cost']] 

def train_model():
    transactions = get_transactions()
    
    if not transactions:
        print("Error: No transactions")
        return

    X_train = preprocess_data(transactions)


    model = IsolationForest(n_estimators=150, contamination=0.05, random_state=42)
    model.fit(X_train)


    with open("anomaly_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model trained and saved as 'anomaly_model.pkl'")

if __name__ == "__main__":
    train_model()
