import logging
import os
import time
import requests
import ast
from DataLogger import datalogger
from OccupancyDetection import occupancydetection
from ControlRecorder import controlrecorder

from pykafka import KafkaClient

logging.basicConfig(level=logging.INFO)

global kafka_client, device_url, portal_url

def publish_records(kafka_topic, agent_type):
    logging.info(f"Publishing records of a device type to topic {kafka_topic}.")

    topic = kafka_client.topics[kafka_topic]
    with topic.get_sync_producer() as producer:
        while True:
            if agent_type == "controller":
                # Get control record from occupancy detection module
                logging.info(f"Retrieving control record from portal")
                cr = controlrecorder.ControlRecorder(portal_url)
                record = cr.get_control_record()
                
            else:
                # Get device data from device
                logging.info(f"Retrieving data record from device url {device_url}.")
                response = requests.get(device_url + "/" + agent_type + "/data")
                if response.status_code == 200:
                    record = response.json()

            if record:
                 # Publish it to the kafka topic
                logging.info(f"Publishing message {record} to {topic}.")
                producer.produce(str(record).encode())
                logging.info(f"Message published.")

            time.sleep(5)

def consume_records(kafka_topic, agent_type):
    logging.info(f"Consuming records of a kafka topic {kafka_topic} for the agent of type {agent_type}.")
    
    topic = kafka_client.topics[kafka_topic]
    consumer = topic.get_simple_consumer()
    while True:
        for message in consumer:
            if message is not None:
                record = ast.literal_eval(message.value.decode())
                print(record)
                if agent_type == "data_logger":
                    if record.get('datapoint') != '':
                        # Log the consumed device data record to the portal
                        logging.info(f"Logging data record of device.")
                        dl = datalogger.DataLogger(portal_url)
                        dl.log(record)
                        print((message.offset, record))

                if agent_type == "controller":
                    # Send the consumed device control record to the device
                    logging.info(f"Posting control record to the device.")
                    url = device_url + "/control"
                    requests.post(url, json=record)
                    print((message.offset, record))


if __name__ == "__main__":

    # agent info
    agent_action = os.getenv("AGENT_ACTION")
    agent_type = os.getenv("AGENT_TYPE")  

    if agent_type == "data_logger" or agent_type == "controller" or agent_action == "occupancy_detection":

        # portal info
        portal_host = os.getenv("PORTAL_HOST")

        if (portal_host ) is None:
            raise Exception("Please make sure to provide all portal host info")

        portal_url = "http://" + portal_host + "/rooms"

    if agent_action == "produce" or agent_action == "consume":

        # device info
        # TODO: accepts list of devices
        device_host = os.getenv("DEVICE_HOST")

        if (device_host) is None:
            raise Exception("Please make sure to provide all device host info")

        device_url = "http://" + device_host

        # kafka info
        kafka_host = os.getenv("KAFKA_HOST")

        if (kafka_host) is None:
            raise Exception("Please make sure to provide all kafka host")

        kafka_client = KafkaClient(hosts=kafka_host)
        kafka_topic = "control_pipeline" if agent_type == "controller" else "data_pipeline"

        if agent_action == "produce":
            publish_records(kafka_topic, agent_type)

        if agent_action == "consume":
            consume_records(kafka_topic, agent_type)

    elif agent_action == "occupancy_detection":
        while True:
            od = occupancydetection.OccupancyDetection(portal_url)
            od.run_occupancy_detection()
            time.sleep(60)
    else:
        raise Exception("Please make sure to provide a valid agent action type produce/consume/occupancy_detection")
