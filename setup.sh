#!/bin/bash
# Prepare environment for DEVNET2449 Lab

vagrant up rtr1
docker run -it --rm -v$(pwd):/home/docker/ kuhlskev/ansible_ydk_jupyter /bin/sh
