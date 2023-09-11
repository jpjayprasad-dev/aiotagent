import requests
from datetime import datetime, timedelta
import yaml
import pandas as pd

class OccupancyDetection:
    def __init__(self, portal_url):
        f = open("rules.conf", "r")
        config = yaml.safe_load(f)
        self._portal_url = portal_url
        self._rules = config["rules"]

    def run_occupancy_detection(self):
        ret = {}
        data = []

        # Get data records created in last 5 minutes
        url = self._portal_url + "/all/data"
        response = requests.request('GET', url, json={"timespan" : "300"})
        if response.status_code == 200:
            records = response.json().get('data')
        
            for record in records:
                device_name = record["device_parameter_id"]["device_id"]["name"]
                param = record["device_parameter_id"]["param"]
                value = record["value"]
                room_id = record["room_id"]["id"]
                data.append({ "room_id" : room_id, "device_name" : device_name, "param" : param, "value": value })
        if data:
            print("data", data)
            # Run control determination function to determin whether we need
            # to create any controlpoint on any device
            controls = self._get_controls(data) 
            for control in controls:
                # post the control record to portal
                url = self._portal_url + "/" + str(control["room_id"]) +  "/control/" + control["device_name"]
                response = requests.post(url, {'param' : control["param"], 'value' : control["value"] })
                ret = response
        return ret

    def _get_controls(self, data):
        df = pd.DataFrame(data)
        controls = []
        rooms = df.room_id.unique()
        for room_id in rooms:
            for rule in self._rules:
                for control_device in rule.keys():
                    rulesets = rule[control_device]
                    datadevice = rulesets["datadevice"]
                    datapoint = rulesets["datapoint"]
                    state_value = df.loc[(df['room_id'] == room_id) 
                    & (df['device_name'] == datadevice) 
                    & (df['param'] == datapoint), 'value'].astype('int').mean()
                    if state_value:
                        threshold = rulesets["threshold"]
                        condition = rulesets["condition"]
                        if condition == "falls_below":
                            if state_value < threshold:
                                controlpoint = rulesets["controlpoint"]
                                value = rulesets["value"]
                                controls.append({"device_name" : control_device, 
                                "room_id" : room_id, 
                                "param" : controlpoint, 
                                "value" : value})


        return controls





        



