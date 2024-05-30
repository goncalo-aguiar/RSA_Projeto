#!/bin/bash

# List of container names or IDs
containers=(
  "projeto_rsa-node1-1"
  "projeto_rsa-node2-1"
  "projeto_rsa-node3-1"
  "projeto_rsa-node4-1"
  "projeto_rsa-node5-1"
  "projeto_rsa-node6-1"
  "projeto_rsa-node7-1"
  "projeto_rsa-node8-1"
  "projeto_rsa-node9-1"
  "projeto_rsa-node10-1"
  "projeto_rsa-node11-1"
  "projeto_rsa-node12-1"
  "projeto_rsa-node13-1"
  "projeto_rsa-node14-1"
  "projeto_rsa-node15-1"
  "projeto_rsa-node16-1"
  "projeto_rsa-node17-1"
  "projeto_rsa-node18-1"
  "projeto_rsa-node19-1"
  "projeto_rsa-node20-1"
  "projeto_rsa-node21-1"
  "projeto_rsa-node22-1"
)

# Iterate over each container and stop the running Python script
for container in "${containers[@]}"; do
  echo "Stopping Python script in container: $container"
  
  # Get the PID of the running Python script
  pids=$(docker exec $container ps aux | grep 'python3 script_boat.py\|python3 script_boia.py' | grep -v grep | awk '{print $2}')
  
  if [ -n "$pids" ]; then
    for pid in $pids; do
      echo "Killing process $pid in container $container"
      docker exec $container kill -SIGINT $pid
    done
    echo "Sent SIGINT to Python script in container: $container"
  else
    echo "No running Python script found in container: $container"
  fi
done