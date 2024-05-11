#xterm -T "Boia 1 " -e "bash -c 'docker exec -it projeto_rsa-node4-1 python3 script_boia.py 192.168.1.6 6; bash'" &
#xterm -T "Boia 2 " -e "bash -c 'docker exec -it projeto_rsa-node5-1 python3 script_boia.py 192.168.1.7 7; bash'" &
#xterm -T "Boia 3 " -e "bash -c 'docker exec -it projeto_rsa-node6-1 python3 script_boia.py 192.168.1.8 8; bash'" &
#xterm -T "Boia 4 " -e "bash -c 'docker exec -it projeto_rsa-node7-1 python3 script_boia.py 192.168.1.9 9; bash'" &
#xterm -T "Boia 5 " -e "bash -c 'docker exec -it projeto_rsa-node8-1 python3 script_boia.py 192.168.1.10 10; bash'" &
#xterm -T "Boia 6 " -e "bash -c 'docker exec -it projeto_rsa-node9-1 python3 script_boia.py 192.168.1.11 11; bash'" &
#xterm -T "Boia 7 " -e "bash -c 'docker exec -it projeto_rsa-node10-1 python3 script_boia.py 192.168.1.12 12; bash'" &



xterm -T "Barco 1 " -e "bash -c 'docker exec -it projeto_rsa-node1-1 python3 script_boat.py 192.168.1.3 3; bash'" &
xterm -T "Barco 2 " -e "bash -c 'docker exec -it projeto_rsa-node2-1 python3 script_boat.py 192.168.1.4 4; bash'" &
xterm -T "Barco 3 " -e "bash -c 'docker exec -it projeto_rsa-node3-1 python3 script_boat.py 192.168.1.5 5; bash'" &
xterm -T "Boia 1 " -e "bash -c 'docker exec -it projeto_rsa-node4-1 python3 script_boia.py 192.168.1.6 6; bash'" &
xterm -T "Boia 2 " -e "bash -c 'docker exec -it projeto_rsa-node5-1 python3 script_boia.py 192.168.1.7 7; bash'" &
#!/bin/bash

#docker exec projeto_rsa-node4-1 python3 script_boia.py 192.168.1.6 6 &
#docker exec  projeto_rsa-node5-1 python3 script_boia.py 192.168.1.7 7 &
#docker exec projeto_rsa-node6-1 python3 script_boia.py 192.168.1.8 8 &
#docker exec  projeto_rsa-node7-1 python3 script_boia.py 192.168.1.9 9 &
#docker exec  projeto_rsa-node8-1 python3 script_boia.py 192.168.1.10 10 &
#docker exec  projeto_rsa-node9-1 python3 script_boia.py 192.168.1.11 11 &
#docker exec  projeto_rsa-node10-1 python3 script_boia.py 192.168.1.12 12 &

#docker exec  projeto_rsa-node1-1 python3 script_boat.py 192.168.1.3 3 &
#docker exec  projeto_rsa-node2-1 python3 script_boat.py 192.168.1.4 4 &
#docker exec  projeto_rsa-node3-1 python3 script_boat.py 192.168.1.5 5 & 