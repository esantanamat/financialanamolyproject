import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import joblib
from decimal import Decimal


data = [
    {'amount': 100.5, 'category': 'Food & drink', 'merchant': 'McDonalds', 'user_id': 'user1'},
    {'amount': 20.0, 'category': 'Food & drink', 'merchant': 'Burger King', 'user_id': 'user1'},
    {'amount': 300.0, 'category': 'Groceries', 'merchant': 'Walmart', 'user_id': 'user1'},
    {'amount': 1500.0, 'category': 'Shopping', 'merchant': 'Amazon', 'user_id': 'user1'},
    {'amount': 10.0, 'category': 'Entertainment', 'merchant': 'Netflix', 'user_id': 'user2'},
    {'amount': 2000.0, 'category': 'Shopping', 'merchant': 'BestBuy', 'user_id': 'user2'},
]


df = pd.DataFrame(data)


label_encoder = LabelEncoder()
df['category'] = label_encoder.fit_transform(df['category'])
df['merchant'] = label_encoder.fit_transform(df['merchant'])


features = df[['amount', 'category', 'merchant']]


model = IsolationForest(n_estimators=100, contamination=0.1)  


model.fit(features)


df['is_anomaly'] = model.predict(features)


df['is_anomaly'] = df['is_anomaly'] == -1


print(df)


#joblib.dump(model, 'suspicious_activity_model.pkl')
