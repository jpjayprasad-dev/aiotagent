import requests
from datetime import datetime, timedelta

class ControlRecorder:
    def __init__(self, portal_url):
        self._portal_url = portal_url

    def get_control_record(self):
        ret = {}
        url = self._portal_url + "/all/control"
        response = requests.request('GET', url, json={"timespan" : "5"})
        if response.status_code == 200:
            records = response.json().get('data')
            if records:
                # Retrieve the most recent control record
                control = records[-1]
                latest_timestamp = control["timestamp"]
                controlpoint = control["device_parameter_id"]["param"]
                device_id = control["device_parameter_id"]["device_id"]["name"]
                room_id = control["room_id"]["id"]
                value = control["value"]
                ret = {"controlpoint" : controlpoint,
                        "value" : value,
                        "datetime" : latest_timestamp,
                        "device_id" : device_id, 
                        "room_id" : room_id
                }
        return ret