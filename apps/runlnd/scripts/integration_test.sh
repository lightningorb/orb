#!/bin/bash

./rln aws.create-keypair --name=integration
./rln create-aws-node --instance-type=c3.2xlarge --availability-zone=us-east-1a --name=integration --disk-size=10 --mainnet --keypair-name integration
./rln -- lncli --help
./rln -- bitcoin-cli --help
./rln aws.detach-blockchain-disk --disk-name=integration
./rln aws.delete-blockchain-disk --disk-name=integration
./rln aws.kill --node-name=integration --force
./rln aws.delete-keypair --name=integration
./rln prefs.remove --name integration
