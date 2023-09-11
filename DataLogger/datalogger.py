import requests

class DataLogger:
    def __init__(self, portal_url):
        self._portal_url = portal_url
        pass
        
    def log(self, record):
        device_id = record["device_id"]
        room_id = record["room_id"]
        url = self._portal_url + "/" + room_id + "/data/" + device_id
        data = { 'param' :  record["datapoint"] , 'value' : record["value"] }
        post_response = requests.post(url, json=data)
        return post_response
