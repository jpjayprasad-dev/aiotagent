# AIOT Agents
The python agent does the following based on running configuration

1. Sensor Agent: The agent fetch data from the IoT device every 5 seconds via HTTP GET request  and push it to the even streaming bus Apache Kafka Queue
2. Control Agent: The agent consumes device controls from the even streaming bus Apache Kafka Queue and push it to device controller via HTTP POST.
3. Data Logger: The agent consumes sensor data from the even streaming bus Apache Kafka Queue and send data points to the persistant DB through AIOT Portal APIs.
4. Occupancy Detection Agents: Agent determines device control decisions and send control points to the persistant DB through AIOT Portal APIs.
5. Control Retriever: The agent checks for newly created control points for the devices every 5 seconds and push it to the even streaming bus Apache Kafka Queue. 

## Setup

1. Install docker
2. Clone this git repo.
```
git clone https://github.com/jpjayprasad-dev/aiotagent/ .
```

## Build Image
```
docker build -t aiotagent:latest .
```

## Application Specs

The following environment variables determines the running configuration of agents
```
PORTAL_HOST = AIOT portal host:port
KAFKA_HOST = Apache Kafka Queue host:port
DEVICE_HOST = IoT sensors/device host:port
AGENT_ACTION = Event streaming type (produce/consume>
AGENT_TYPE = The identity of agent (life_being/iaq/controller/data_logger/occupancy_detection)
```

## Run Service
```
docker run --rm -d -e PORTAL_HOST=<aiot_portal_host:port> -e KAFKA_HOST=<kafka_host:port> -e DEVICE_HOST=<iot_device_host:port> -e AGENT_ACTION=<produce/consume> -e AGENT_TYPE=<agent_type> --name <agent_name> aiotagent:latest

```

## Examples [Screenshots]
To run life_being agent
<img width="1012" alt="image" src="https://github.com/jpjayprasad-dev/aiotagent/assets/73153441/085e2aa9-6ccb-42d6-9aeb-529372605b92">

To run data logger agent
<img width="1007" alt="image" src="https://github.com/jpjayprasad-dev/aiotagent/assets/73153441/0628bdc8-046f-42f2-980a-8483c3f0f930">





