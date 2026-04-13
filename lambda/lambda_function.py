import json
import boto3
import urllib.parse
from datetime import datetime
from PIL import Image
import io

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('ProcessedFiles')

MAX_FILE_SIZE = 10000

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        try:
            print(f"Processing: {key}")

            response = s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read()

            file_type = "TEXT"
            json_valid = False

            # TEXT FILE
            if key.endswith('.txt'):
                text = content.decode('utf-8')

                word_count = len(text.split())
                line_count = len(text.splitlines())

            # JSON FILE
            elif key.endswith('.json'):
                file_type = "JSON"
                text = content.decode('utf-8')
                json.loads(text)
                json_valid = True

                word_count = len(text.split())
                line_count = len(text.splitlines())

            # IMAGE FILE
            elif key.endswith(('.jpg', '.jpeg', '.png')):
                file_type = "IMAGE"

                image = Image.open(io.BytesIO(content))
                image = image.resize((200, 200))

                buffer = io.BytesIO()
                image.save(buffer, format="JPEG")

                new_key = key.replace("uploads/", "processed/resized-")

                s3.put_object(
                    Bucket=bucket,
                    Key=new_key,
                    Body=buffer.getvalue()
                )

                word_count = 0
                line_count = 0

            else:
                raise Exception("Unsupported file type")

            # Store in DB
            table.put_item(
                Item={
                    'fileName': key,
                    'timestamp': str(datetime.now()),
                    'fileType': file_type,
                    'wordCount': word_count,
                    'lineCount': line_count,
                    'jsonValid': json_valid,
                    'status': 'PROCESSED'
                }
            )

            move_file(bucket, key, "processed/")

        except Exception as e:
            print("Error:", str(e))

            table.put_item(
                Item={
                    'fileName': key,
                    'timestamp': str(datetime.now()),
                    'status': 'FAILED',
                    'error': str(e)
                }
            )

            move_file(bucket, key, "failed/")

    return {"status": "done"}


def move_file(bucket, key, folder):
    new_key = key.replace("uploads/", folder)

    s3.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': key},
        Key=new_key
    )

    s3.delete_object(Bucket=bucket, Key=key)