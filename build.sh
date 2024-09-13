#!/bin/sh

docker build . -t ${accountNo}.dkr.ecr.${region}.amazonaws.com/${repoName}:latest
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${accountNo}.dkr.ecr.${region}.amazonaws.com
docker push ${accountNo}.dkr.ecr.${region}.amazonaws.com/i${repoName}:latest
