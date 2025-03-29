import json
import unittest
from detect_anomalies import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    
    def test_lambda_handler(self):
        event = {
            "body": json.dumps({
                "user_id": "12345", 
                "date_transaction_id": "2023-03-28T12:34:56ZTX12345", 
                "name": "Sample Merchant",  
                "category": "Food", 
                "cost": 99999999.92,  
                "flagged": "False", 
                "date": "2023-03-28T12:34:56Z"
            })
        }

        context = {}  
        response = lambda_handler(event, context)
        
        
        self.assertEqual(response["statusCode"], 200) 
        body = json.loads(response["body"])
        self.assertIn("message", body)
        self.assertIn("anomalous", body)  

if __name__ == '__main__':
    unittest.main()
