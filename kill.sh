#!/bin/bash

# Define an array of container names
containers=("projeto_rsa-node4-1" "projeto_rsa-node5-1" "projeto_rsa-node6-1" "projeto_rsa-node7-1" "projeto_rsa-node8-1" "projeto_rsa-node9-1" "projeto_rsa-node10-1"
            "projeto_rsa-node1-1" "projeto_rsa-node2-1" "projeto_rsa-node3-1")

# Loop through the array and stop each container
for container in "${containers[@]}"; do
    echo "Stopping container: $container"
    docker stop $container
done

echo "All specified containers have been stopped."