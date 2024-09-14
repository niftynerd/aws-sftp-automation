import json
import paramiko
import boto3
from datetime import datetime
import pytz


s3_client = boto3.client('s3')
sm_client = boto3.client('secretsmanager')

# create ssh client 
ssh_client = paramiko.SSHClient()

# remote server credentials
secret_json = json.loads(sm_client.get_secret_value(SecretId='sftp-secret')['SecretString'])
host = secret_json['HOST']
username = secret_json['USERNAME']
password = secret_json['PASSWORD']
port = secret_json['PORT']
bucket = secret_json['BUCKET']

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host,port=port,username=username,password=password)

ftp = ssh_client.open_sftp()
files = ftp.listdir() # parameterize if path is different from root
now = datetime.now(pytz.timezone("Pacific/Auckland")) # change to region that you want to use for timestamp on your files
year = now.year
month = now.month
day = now.day
for c,f_name in enumerate(files):
    try:
        with ftp.open(f_name, "r") as f:
            f.prefetch()
            s3_client.put_object(Body=f.read(), Bucket=bucket, Key=f'{year}/{month}/{day}/{f_name}')
        # add the following line if you want to and have ftp user permissions to delete files on the server after downloading them
        # ftp.remove(f_name)
    except FileNotFoundError:
        continue

# close the connection
ftp.close()
ssh_client.close()
