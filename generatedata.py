import random
import boto3
import json
from datetime import datetime, timedelta
from decimal import Decimal


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FinancialExpenses')


merchant_map = {
    'Automotive': ['Tesla Supercharger', 'Jiffy Lube', 'Goodyear', 'Pep Boys', 'AutoZone'],
    'Bills & Utilities': ['Optimum', 'AT&T', 'Comcast', 'PSE&G', 'National Grid'],
    'Education': ['Udemy', 'Coursera', 'NJIT Tuition', 'Chegg', 'Khan Academy'],
    'Entertainment': ['Netflix', 'Spotify', 'AMC Theaters', 'Apple Music', 'GameStop', 'Hulu'],
    'Fees & adjustments': ['Banco Reservas Fee', 'Chase Overdraft Fee', 'PayPal Adjustment'],
    'Food & drink': ['McDonald’s', 'Starbucks', 'Chipotle', 'Burger King', 'Dunkin’'],
    'Gas': ['Shell Gas', 'ExxonMobil', 'BP', 'Costco Gas', 'Wawa Gas'],
    'Gifts & Donations': ['GoFundMe', 'Charity Water', 'Red Cross', 'St. Jude', 'Salvation Army'],
    'Groceries': ['Walmart', 'Trader Joe’s', 'Whole Foods', 'ShopRite', 'Costco'],
    'Health & wellness': ['CVS Pharmacy', 'Walgreens', 'GNC', 'Blink Fitness', 'Rite Aid'],
    'Home': ['Home Depot', 'Lowe’s', 'IKEA', 'Wayfair', 'Bed Bath & Beyond'],
    'Miscellaneous': ['eBay', 'Craigslist', 'Etsy', 'Amazon Marketplace'],
    'Personal': ['Sephora', 'Ulta Beauty', 'Nike Store', 'Adidas', 'Macy’s'],
    'Professional Services': ['TurboTax', 'LegalZoom', 'H&R Block', 'WeWork'],
    'Shopping': ['Amazon', 'Walmart', 'Target', 'Best Buy', 'eBay'],
    'Travel': ['United Airlines', 'Airbnb', 'Uber', 'Lyft', 'Riu Hotels']
}

user_ids = ['user123', 'user321', 'user222']

def generatemockdata():
    transactions = []

    for user_id in user_ids:
         for _ in range(10): 
            transaction_id = str(random.randint(100000, 999999))
            category = random.choice(list(merchant_map.keys()))
            merchant = random.choice(merchant_map[category])
            cost = Decimal(str(round(random.uniform(5, 500), 2)))  
            date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            
         
            transaction = {
                'transaction_id': transaction_id,
                'user_id': user_id,
                'name': merchant,
                'category': category,
                'cost': cost,
                'date': date,
                'flagged': False  
            }
            
            transactions.append(transaction)
    
    
    with table.batch_writer() as batch:
        for transaction in transactions:
            batch.put_item(Item=transaction)


generatemockdata()