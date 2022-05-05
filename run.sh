python broker.py -s 9000 -p 8000 & sleep 0.5;
sh run-scripts/run-sub-1.sh & sleep 0.5;
sh run-scripts/run-sub-2.sh & sleep 0.5;
sh run-scripts/run-pub-1.sh & sleep 0.5;
sh run-scripts/run-pub-2.sh;
