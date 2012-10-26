__author__ = 'Mike Gavrilov'

from pymongo import Connection
from config import *
import time
import logging

### MAIN SECTION ###

MONGO_CONN = Connection(MONGO_HOST)

# Generate the next queue ID
def gen_next_queue(p_current_queue):
    if p_current_queue == QUEUE_COUNT:
        return 1
    else:
        return p_current_queue + 1

# Queue settings class
# Settings data row
#   { '_id' : 'queue', 'queueData' : { 'queueId' : 1 } }
class QueueSettings:
    COLL = None

    def __init__(self):
        self.COLL = MONGO_CONN[MONGO_DB][MONGO_SETTINGS_COLL]

    def get_settings(self):
        data = self.COLL.find({ '_id' : 'queue' })
        return data[0]['queueData']

    def set_settings(self,p_settings):
        self.COLL.save({ '_id' : 'queue', 'queueData' : p_settings })

    def set_nexQueue(self,p_next_queue):
        self.COLL.save({ '_id' : 'queue', 'queueData' : { 'queueId' : p_next_queue } })

    def __del__(self):
        pass


class QueueReader:
    MONGO_COLL = None
    row_count = 0

    def __init__(self,p_qId):
        queueNumber = ('%s_%s') % (MONGO_QUEUE_COLL,p_qId)
        self.MONGO_COLL = MONGO_CONN[MONGO_DB][queueNumber]

    def prepare_query(self):
        data = self.MONGO_COLL.find()
        for row in data:
            self.MONGO_COLL.remove({ '_id' : row['_id'] })
            self.row_count += 1

    def __del__(self):
        pass


class QueueWriter:
    pass




if __name__ == '__main__':
    q = QueueSettings()
    qId = q.get_settings()['queueId']
#    print('current',qId)
    q.set_nexQueue(gen_next_queue(qId))

    qr = QueueReader(qId)
    qr.prepare_query()

    file = open('/home/miha/queue/cron.log','a')
#    file = open('/tmp/log','a')
    file.write('removed: %s from QUEUE: %s \n' % (qr.row_count,qId))
#    print('next',q.get_settings()['queueId'])
#    time.sleep(6)

