# pubsubway
A Publish-Subscribe (Pub/Sub) system written in Python

## Execution
* This project is entirely built with python - specifically version 3.8.10 on Ubuntu 20.04.
* I would recommend running this in a unix system, as there may be some differences with the way ports are handled in Windows vs Unix. I haven't tested the functionality on Windows.

To run the broker:
```
python broker.py -s sub_port -p pub_port [-o port_offset -v]
```
* The `-o port_offset` argument is optional and will be described below.

To run the subscriber:
```
python subscriber.py -i ID -r sub_port -h broker_IP -p port [-f command_file -o port_offset -v]
```
* The `-v` argument is for a more verbose output.
* The `-o port_offset` argument is optional and will be described below.

To run the publisher:
```
python publisher.py -i ID -r pub_port -h broker_IP -p port [-f command_file -o -v]
```
* The `-v` argument is for a more verbose output.


## Port offset argument
* The port offset argument has a default value of 1 and is used in the broker and subscriber processes.
* These two processes use two different ports to communicate with each other. One to send messages and one to receive.
* When the processes are executed with the commands given above, the user only needs to define the first of these two ports for each process.
* The other is defined by adding the port_offset value to the user defined port.
* So if the user specifies 9000 as the sub port for the broker, then 9001 will be used (by default) for the bi-directional communication with the subscribers.
* This means that if you'd like to create multiple subsribers processes, you need to be mindful of their ports, so that they don't overlap.

## All-in-one Execution
* Included in the directory, is a script which launches a broker and several publisher and subscriber processes at the same time.
```
sh run.sh
```

* You can also take advantage of ready-made scripts that launch individual publishers and subscribers (in the run-scripts directory) and various command files for publsihers and subscribers (in the command-files directory).
