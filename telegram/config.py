import json

class Config():
    def __init__(self, json_file):
        with open(json_file) as f:
            self.data = json.load(f)