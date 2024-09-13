FROM public.ecr.aws/amazonlinux/amazonlinux:latest

COPY ingest/. /ingest

RUN yum update -y && yum install -y python pip
RUN pip install paramiko boto3 botocore
