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

    Its only public method is :meth:`getReport`. See its docstring for
    details.

    Use the config.py file to adjust which modules you want to be active
    in the QC.

    Usage:

    >>> qc = QcHandler(app)
    >>> qc.getReport(1)
    {'sessionId': 1, 'status': 'started', 'modules':{}}
    ... wait ...
    >>> qc.getReport(1)
    {"sessionId": 1,
     "status": "processing",
     "modules"  {
        "marosijo" :  {
                        "totalStats": {"accuracy": [0.0;1.0]"},
                        "perRecordingStats": [{"recordingId": ...,
                            "stats": {"accuracy": [0.0;1.0]}}]}
                      }, 
                      ...
                }
    }

    """

    def __init__(self, app, dbHandler):
        self.dbHandler = dbHandler # grab database handler from app to handle MySQL database operations

        
    def sortReports(self,reports):
  
        if reports:
            data = json.loads(reports[0])
            #print('xxxxxxxxxxxxxxxxxxxxxx')
            perRecording = data['perRecordingStats']

            for i in perRecording:
                acc = i['stats']['accuracy'] 
                grade = int(floor(acc*100))
                recId = i['recordingId']
                if grade & recId:
                    status = self.dbHandler.processQcData(recId, grade)
                    print(status)

    
  