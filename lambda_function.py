import json

def lambda_handler(event, context):
    print("Event:", json.dumps(event, indent=2))
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    print(f"New CSV file {file_key} added to {bucket_name}.")
    return {
        'statusCode': 200,
        'body': json.dumps('CSV processing initiated!')
    }
