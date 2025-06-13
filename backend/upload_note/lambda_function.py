import json
import boto3
import base64
import uuid
from datetime import datetime
import traceback

s3 = boto3.client('s3')
ses = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')
table_name = 'SickNotes'
table = dynamodb.Table(table_name)

BUCKET_NAME = 'sicknote-vault-bucket'
FROM_EMAIL = 'ukeme@example.com'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        patient_name = body.get('patient_name', 'Unknown')
        patient_email = body['patient_email']
        note_file = body['note_file']
        file_name = f"{uuid.uuid4()}.pdf"

        # Decode and upload to S3
        file_data = base64.b64decode(note_file)
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_data)

        # Prepare metadata
        note_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        # Put item in DynamoDB
        table.put_item(Item={
            'note_id': note_id,
            'String': 'SickNote',
            'patient_name': patient_name,
            'patient_email': patient_email,
            's3_key': file_name,
            'timestamp': timestamp
        })

        # Send confirmation email
        email_subject = "Sick Note Submission Confirmation"
        email_body = (
            f"Hello {patient_name},\n\n"
            f"Your sick note has been securely submitted.\n"
            f"Use this Note ID for future verification: {note_id}\n\n"
            f"Thank you."
        )

        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [patient_email]},
            Message={
                'Subject': {'Data': email_subject},
                'Body': {'Text': {'Data': email_body}}
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Or use your Amplify domain
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "message": "Note uploaded successfully!",
                "note_id": note_id
            })
        }

    except Exception as e:
        print("ERROR TRACEBACK:\n", traceback.format_exc())
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({'error': str(e)})
        }
