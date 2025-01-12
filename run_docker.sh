#!/bin/bash

docker run \
       --rm \
       -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
       -v /home/duke/sawyer_comp/mjkey/mjkey.txt:/root/.mujoco/mjkey.txt \
       -v /home/duke/sawyer_comp/code/:/root/code/ \
       -v /home/duke/sawyer_comp/robosuite/:/root/robosuite/ \
       -v /home/duke/sawyer_comp/stable-baselines/:/root/stable-baselines/ \
       --env DISPLAY=$DISPLAY \
       --env CUDA_VISIBLE_DEVICES=2 \
       --runtime nvidia \
       crl_sawyer 
