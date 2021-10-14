#!/bin/sh

sudo yum -y install git
sudo yum -y install docker
sudo service docker start
sudo usermod -aG docker ec2-user

# 재접속
git clone https://github.com/chainstock-project/server.git
cd server
docker build . -t stock-chain
docker run -d --name stock-docker -p 80:5000 -p 26656:26656 -p 26657:26657 -p 1337:1337 stock-chain:latest
docker logs -f stock-docker
