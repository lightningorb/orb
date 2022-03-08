#!/bin/bash

./rln aws.create-keypair --name=lnd3
./rln create-aws-node --instance-type=t3.medium --availability-zone=ap-southeast-1a --name=lnd3 --disk-size=550 --mainnet --keypair-name lnd3
