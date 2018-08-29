# Copyright 2016 The Eyra Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# File author/s:
#     Stefan Gunnlaugur Jonsson <stefangunnlaugur@gmail.com>




from db_handler import DbHandler
import json
import os
import random
from math import floor

from util import log, filename


class QcSorter(object):
    """QcSorter
    ============

    Class for handling quality control sorting to the right recording in db.

    """

    def __init__(self, app, dbHandler):
        self.dbHandler = dbHandler # grab database handler from app to handle MySQL database operations

        
    def sortReports(self,reports):
        #Locate the data and send it to be processed by the db handler
        if reports:
            try:
                data = reports['MarosijoModule']
            except:    
                data = json.loads(reports[0])
            try:
                perRecording = data['perRecordingStats']
                for i in perRecording:
                    acc = i['stats']['accuracy']
                    grade = int(floor(acc*100))
                    recId = i['recordingId']
                    if (grade and recId):
                        status = self.dbHandler.processQcData(recId, grade)
                        print(status)
            except:
                print("Invalid report")


  