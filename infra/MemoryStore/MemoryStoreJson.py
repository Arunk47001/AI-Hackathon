import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MemoryDBConnect:
    def __init__(self):
        self.file = "infra/MemoryStore/memory.json"

    def get_history(self, keys:dict)->list:
        try:
            print("keys")
            file_r = open(self.file,'r')
            self.data = json.loads(file_r.read())
            print("test", self.data)
            if self.data.get(keys['session_id']) == None:
                return []
            else:
                return self.data.get(keys['session_id'])['history']
        except Exception as err:
            print(err)
            logger.error(err)
            raise ValueError("Error in get_history")

    def put_history(self, keys: dict):
        try:
            print("put")
            hist=self.get_history(keys)
            print("test111", hist)
            if hist:
                hist.append({'HU':keys['question'], 'AI':keys['response']})
                self.data[keys['session_id']]['history'] = hist
            else:
                self.data[keys['session_id']]= {'history':[{'HU':keys['question'], 'AI':keys['response']}]}
            file_w = open(self.file, 'w')
            file_w.write(json.dumps(self.data)+"\n")
            file_w.close()
        except Exception as err:
            logger.error(err)
            raise ValueError("Error in put_history")
