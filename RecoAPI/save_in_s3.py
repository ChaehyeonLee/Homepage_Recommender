import  settings
import boto3
import json


session = boto3.Session(
    aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
)

s3 = session.resource('s3').Bucket("history-bucket")
json.load_s3 = lambda f: json.load(s3.Object(key=f).get()["Body"].read().decode('utf-8'))
json.dump_s3 = lambda obj, f: s3.Object(key=f).put(Body=json.dumps(obj))
