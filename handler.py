import boto3 
import json

s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')


def lambda_handler(event, context):
    bucket = event.get("Records")[0].get("s3").get("bucket").get("name")
    filename = event.get("Records")[0].get("s3").get("object").get("key")
    print(f'Print bucket name: {bucket}')
    print(f'Print object name: {filename}')
    json_object = s3_client.get_object(Bucket=bucket, Key=filename)
    json_file_reader = json_object['Body'].read()
    print(json_file_reader)
    print(type(json_file_reader))
    json_dict = json.loads(json_file_reader)
    table = dynamodb_client.Table('Employees')
    table.put_item(Item=json_dict)
    
