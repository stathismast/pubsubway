python broker.py -s 9000 -p 8000 & sleep 0.5;
python subscriber.py -i s1 -r 9100 -h 127.0.0.1 -p 9000 -f command-files/subscriber-commands.txt & sleep 0.5;
python subscriber.py -i s2 -r 9200 -h 127.0.0.1 -p 9000 -f command-files/subscriber-commands.txt & sleep 0.5;
python subscriber.py -i s3 -r 9300 -h 127.0.0.1 -p 9000 -f command-files/subscriber-commands.txt & sleep 0.5;
python subscriber.py -i s4 -r 9400 -h 127.0.0.1 -p 9000 -f command-files/subscriber-commands.txt & sleep 0.5;
python subscriber.py -i s5 -r 9500 -h 127.0.0.1 -p 9000 -f command-files/subscriber-commands.txt & sleep 0.5;
python publisher.py -i p1 -r 8100 -h 127.0.0.1 -p 8000 -f command-files/publisher-commands-p1.txt & sleep 0.5;
python publisher.py -i p2 -r 8200 -h 127.0.0.1 -p 8000 -f command-files/publisher-commands-p1.txt & sleep 0.5;
python publisher.py -i p3 -r 8300 -h 127.0.0.1 -p 8000 -f command-files/publisher-commands-p1.txt & sleep 0.5;
python publisher.py -i p4 -r 8400 -h 127.0.0.1 -p 8000 -f command-files/publisher-commands-p1.txt & sleep 0.5;
python publisher.py -i p5 -r 8500 -h 127.0.0.1 -p 8000 -f command-files/publisher-commands-p1.txt;
