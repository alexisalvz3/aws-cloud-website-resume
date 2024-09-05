import json
import boto3
# creating instance of dynamodb 
dynamodb = boto3.resource('dynamodb')
# setting table var to our chosen dynamodb table 'resume-challenge'
table = dynamodb.Table('resume-challenge')

def lambda_handler(event, context):
    # calling specific item in our table and setting it to 'response'
    response = table.get_item(Key={
        'id': '0'
    })
    # calling views value from our table in order to change it
    views = response['Item']['views']
    # updating views
    views = views + 1
    print(views)
    # placing views value back into table
    response = table.put_item(Item={
        'id': '0',
        'views': views
    })
    
    return views