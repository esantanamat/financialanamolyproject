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


inserted_keys = set()

def generate_cost(category):
    if category == 'Automotive':
        return Decimal(str(round(random.uniform(100, 1000), 2)))
    elif category == 'Bills & Utilities':
        return Decimal(str(round(random.uniform(50, 200), 2)))
    elif category == 'Education':
        return Decimal(str(round(random.uniform(100, 500), 2)))
    elif category == 'Entertainment':
        return Decimal(str(round(random.uniform(20, 100), 2)))
    elif category == 'Fees & adjustments':
        return Decimal(str(round(random.uniform(10, 50), 2)))
    elif category == 'Food & drink':
        return Decimal(str(round(random.uniform(10, 50), 2)))
    elif category == 'Gas':
        return Decimal(str(round(random.uniform(30, 100), 2)))
    elif category == 'Gifts & Donations':
        return Decimal(str(round(random.uniform(5, 20), 2)))
    elif category == 'Groceries':
        return Decimal(str(round(random.uniform(20, 100), 2)))
    elif category == 'Health & wellness':
        return Decimal(str(round(random.uniform(10, 50), 2)))
    elif category == 'Home':
        return Decimal(str(round(random.uniform(100, 500), 2)))
    elif category == 'Miscellaneous':
        return Decimal(str(round(random.uniform(5, 20), 2)))
    elif category == 'Personal':
        return Decimal(str(round(random.uniform(20, 100), 2)))
    elif category == 'Professional Services':
        return Decimal(str(round(random.uniform(50, 200), 2)))
    elif category == 'Shopping':
        return Decimal(str(round(random.uniform(50, 200), 2)))
    elif category == 'Travel':
        return Decimal(str(round(random.uniform(100, 500), 2)))

def generatemockdata():
    transactions = []

    for user_id in user_ids:
         for _ in range(10): 
           
            transaction_id = str(random.randint(100000, 999999))
            category = random.choice(list(merchant_map.keys()))
            merchant = random.choice(merchant_map[category])
            cost = generate_cost(category)
            date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')

            
            range_key = date + "#" + transaction_id #set because I was having issues with inputting things into the dynamodb with the previous user hash and date range key

            transaction = {
                'user_id': user_id,
                'date_transaction_id': range_key,
                'name': merchant,
                'category': category,
                'cost': cost,
                'date': date,
                'flagged': str(False),
            }

            transactions.append(transaction)

    # Batch the write into smaller chunks to avoid DynamoDB limits
    for i in range(0, len(transactions), 25):
        with table.batch_writer() as batch:
            for transaction in transactions[i:i+25]:
                batch.put_item(Item=transaction)


generatemockdata()