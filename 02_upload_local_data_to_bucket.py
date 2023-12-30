import boto3 
import os
from datetime import datetime
import time

#boto3 already consumes local variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in client
BUCKET_NAME = os.getenv('AWS_BUCKET_LANDZONE_NAME')

print(BUCKET_NAME)

def get_s3_client():
    s3_client = boto3.client(
        "s3"
    )
    print("Connected to AWS")
    return s3_client

def ensure_s3_bucket_exists(s3_client, BUCKET_NAME):
    try:
        try:
            s3_client.head_bucket(Bucket=BUCKET_NAME)
        except:
            s3_client.create_bucket(
                Bucket=BUCKET_NAME,
            )
            print(f'Bucket {BUCKET_NAME} created')
        else:
            print(f'bucket {BUCKET_NAME} already exists')
        
    except Exception as e:
        print(f'Failed to create bucket: {e}')

def send_folder_files_to_s3(s3_client, BUCKET_NAME, folder_path):
    files = os.listdir(folder_path)

    current_datetime = datetime.today().strftime("%Y%m%d%H%M%S")

    for file in files:
        file_path = os.path.join(folder_path, file)

        file_name = (file.replace('.csv','')).lower()
        s3_client.upload_file(file_path, BUCKET_NAME, f'ecommerce/{file_name}_{current_datetime}.csv')
        print(f'{file} uploaded to S3')
        time.sleep(10)
    
    print('All files were uploaded to S3')


s3_client = get_s3_client()
ensure_s3_bucket_exists(s3_client, BUCKET_NAME)
send_folder_files_to_s3(s3_client, BUCKET_NAME, 'original_data')