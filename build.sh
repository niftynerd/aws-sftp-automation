#!/bin/sh
accountNo=123456789012 # enter account number to use here
region=ap-southeast-2 # enter region of ecr repo created
ecrRepoName=ingest-sftp-to-s3 # enter name of ecr repo created

docker build . -t ${accountNo}.dkr.ecr.${region}.amazonaws.com/${ecrRepoName}:latest
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${accountNo}.dkr.ecr.${region}.amazonaws.com
docker push ${accountNo}.dkr.ecr.${region}.amazonaws.com/${ecrRepoName}:latest
