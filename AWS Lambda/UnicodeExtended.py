import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        if key.endswith('.html'):
            response = s3.head_object(Bucket=bucket, Key=key)
            content_type = response.get('ContentType', '')

            if content_type != 'text/html; charset=UTF-8':
                s3.copy_object(
                    Bucket=bucket,
                    CopySource={'Bucket': bucket, 'Key': key},
                    Key=key,
                    MetadataDirective='REPLACE',
                    ContentType='text/html; charset=UTF-8'
                )

    return {
        'statusCode': 200,
        'body': 'Content type updated successfully'
    }
