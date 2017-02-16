#!/bin/bash
# Prepare environment for DEVNET2449 Lab

vagrant suspend rtr1
docker rm -f `docker ps -a -q`
