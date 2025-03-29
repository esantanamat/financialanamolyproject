# **AWS Financial Anomaly Detection**

This project is an **AI-powered expense tracker** that detects suspicious transactions using AWS services. It leverages **Terraform** for infrastructure as code, **AWS Lambda** for serverless execution, and **Machine Learning (Isolation Forest)** to flag anomalies in financial transactions.

---

## **Architecture Overview**
1. **Infrastructure Deployment (Terraform)**
   - Sets up **DynamoDB** for transaction storage  
   - Deploys two **AWS Lambda functions**  
   - Configures necessary IAM roles and permissions  

2. **Data Collection & Model Training**
   - Transactions are stored in **DynamoDB**  
   - Data is extracted and preprocessed  
   - The anomaly detection model is trained using **Isolation Forest**  
   - The trained model is serialized and stored for future inference  

3. **Transaction Processing (AWS Lambda)**
   - **Lambda Function 1**: Adds new transactions to DynamoDB  
   - **Lambda Function 2**: Detects anomalies when invoked, checking for outliers based on past transactions  

---

## **Deployment Steps**

### **1. Deploy Infrastructure**
Ensure you have **Terraform** installed and run:
```bash
terraform init
terraform apply   
python train_model.py
zip -r lambda_function.zip detect_anomalies.py
aws lambda update-function-code --function-name detectAnomalyFunction --zip-file fileb://lambda_function.zip
```   
## Future Improvements
1. Frontend Dashboard - A UI to visualize transactions that are flagged anomalies
2. Realtime alerts - Email/SMS for suspicious transactions (mimicking real banks)
3. Model optimization - Used about 100 transactions to train the model, the more the better
   
