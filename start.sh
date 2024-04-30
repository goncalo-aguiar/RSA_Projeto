xterm -T "Boia 1 " -e "bash -c 'docker exec -it projeto_rsa-node4-1 python3 script_boia.py 192.168.1.6 6; bash'" &
xterm -T "Boia 2 " -e "bash -c 'docker exec -it projeto_rsa-node5-1 python3 script_boia.py 192.168.1.7 7; bash'" &
xterm -T "Barco 1 " -e "bash -c 'docker exec -it projeto_rsa-node1-1 python3 script_boat.py 192.168.1.3 3; bash'" &
xterm -T "Barco 2 " -e "bash -c 'docker exec -it projeto_rsa-node2-1 python3 script_boat.py 192.168.1.4 4; bash'" &
xterm -T "Barco 3 " -e "bash -c 'docker exec -it projeto_rsa-node3-1 python3 script_boat.py 192.168.1.5 5; bash'" &

