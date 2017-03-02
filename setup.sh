#!/bin/bash
# Prepare environment for DEVNET2449 Lab

vagrant up rtr1
docker run -it --rm -p58888:58888 -v$(pwd):/home/docker/ kuhlskev/ansible_ydk_jupyter
