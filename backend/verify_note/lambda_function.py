import json
import boto3
import logging

# Initialize AWS resources
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

TABLE_NAME = 'SickNotes'
BUCKET_NAME = 'sicknote-vault-bucket'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        # Validate query parameter
        note_id = event.get('queryStringParameters', {}).get('note_id')
        if not note_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*'
                },
                'body': json.dumps({'message': 'Missing note_id'})
            }

        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={
            'note_id': note_id,
            'String': 'SickNote'  # your sort key
        })

        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*'
                },
                'body': json.dumps({'message': 'Note not found'})
            }

        s3_key = item['s3_key']
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=300
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({
                'message': 'Note found',
                'note_id': note_id,
                'patient_name': item.get('patient_name', 'Unknown'),
                'timestamp': item.get('timestamp', 'Unknown'),
                'note_url': presigned_url
            })
        }

    except Exception as e:
        logger.error(f"Error retrieving sick note: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
