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
#     Matthias Petursson <oldschool01123@gmail.com>
#     Stef'an Gunnlaugur Jonsson <stefangunnlaugur@gmail.com>

import sh
import os
import sys
import json
import time
import redis

# mv out of qc/script directory and do relative imports from there.
parParDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(parParDir)
from qc.config import activeModules
import qc.celery_config as celery_config
from util import DbWork
sys.path.remove(parParDir)
del parParDir

from db_handler import DbHandler
from qc.qc_handler import QcHandler
from qc.qc_sorter import QcSorter

dbWork = DbWork()
_redis = redis.StrictRedis(
            host=celery_config.const['host'], 
            port=celery_config.const['port'], 
            db=celery_config.const['backend_db'])
verbose = False

class QcRunner(object):

    def __init__(self, app, dbHandler, qcHandler, qcSorter):
        """Initialise a QC runner

        config.activeModules should be a dict containing names : function pointers
        to the QC modules supposed to be used.

        app.config['CELERY_CLASS_POINTER'] should be a function pointer to
        the instance of the celery class created in app from celery_handler.py

        """

        self.dbHandler = dbHandler # grab database handler from app to handle MySQL database operations
        self.qcSorter = qcSorter
        self.qcHandler = qcHandler

    #def runQC(from_session, to_session, sleep_between, avoid_timeout):
    def runQC(self, from_session, to_session, sleep_between, avoid_timeout):
        """
        Runs QC on recordings which haven't been analyzed by QC yet.
        """

        if to_session is None:
            to_session = dbWork.highestSessionId()

        if to_session == 'stdin':
            sesRange = sys.stdin
            prevSes = []
        else:
            sesRange = range(from_session, min(to_session + 1, dbWork.highestSessionId()))

        start = time.time()
        totalDiff = 0
        for i in sesRange:
            # if in individual_sessions mode, strip newline
            if type(i) is str:
                i = i.strip()
            if to_session == 'stdin':
                prevSes.append(i)

            print('Processing session {}'.format(i))
            recsOnDisk = self.qcDumpRecCountBySession(i)
            recsInRedis = self.qcRedisRecCountBySession(i)
            recsInDb = dbWork.recCountBySession(i)
            recsDone = max(recsInRedis, recsOnDisk)
            if verbose:
                print('Recs done: {}'.format(recsDone))
                print('..in redis: {}'.format(recsInRedis))
                print('..on disk: {}'.format(recsOnDisk))
                print('..recs in db: {}'.format(recsInDb))
            if (recsDone < recsInDb):
                print('Querying QC for session {}'.format(i))
                qcReport = self.qcHandler.getReport(i)
                #sh.curl('-k', 'https://localhost/backend/qc/report/session/{}'.format(i))
                time.sleep(sleep_between)
                diff = dbWork.recCountBySession(i)-recsDone
                totalDiff+=diff
                print('Diff:',diff)
            else:
                qcReport = self.qcHandler.getReport(i)

        print('totalDiff:',totalDiff)
   

    def qcRedisRecCountBySession(self, sessionId):
        """
        Returns the minimum (of all active modules) number of recordings with a qc report in redis datastore by session.
        e.g. if there is no report for any active module, returns 0.

        Parameters:
            sessionId       id of session
        """
        minimum = sys.maxsize
        for key, module in activeModules.items():
            reportPath = 'report/{}/{}'.format(module['name'], sessionId)
            try:
                totalRecs = 0
                report = json.loads(_redis.get(reportPath).decode('utf-8'))
                try:
                    totalRecs += len(report['perRecordingStats'])
                except KeyError as e:
                    # probably a module which doesn't have perRecordingStats, allow it.
                    totalRecs = sys.maxsize if totalRecs == 0 else totalRecs
                minimum = min(minimum, totalRecs)
            except AttributeError as e:
                return 0

        return minimum if minimum != sys.maxsize else 0

    def qcDumpRecCountBySession(self, sessionId):
        """
        Returns the minimum (of all active modules) number of recordings with a qc report dumped on disk by session.
        e.g. if there is no report for any active module, returns 0.

        Parameters:
            sessionId       id of session
        """
        minimum = sys.maxsize
        for key, module in activeModules.items():
            dumpPath = '{}/report/{}/{}'.format(celery_config.const['qc_report_dump_path'],
                                                module['name'],
                                                sessionId)
            try:
                with open(dumpPath, 'r') as f:
                    reports = f.read().splitlines() # might be more than one, if a timeout occurred and recording was resumed
                    # sum the recordings of all the reports (usually only one)
                    totalRecs = 0
                    for report in reports:
                        if report == '':
                            # robustness to extra newlines
                            continue
                        report = json.loads(report)
                        try:
                            totalRecs += len(report['perRecordingStats'])
                        except KeyError as e:
                            # probably a module which doesn't have perRecordingStats, allow it.
                            totalRecs = sys.maxsize if totalRecs == 0 else totalRecs
                            break
                    minimum = min(minimum, totalRecs)
            except FileNotFoundError as e:
                return 0

        return minimum if minimum != sys.maxsize else 0

    def calcTotalQCDone():
        """
        Returns the number of recordings analysed by qc and dumped on disk.
        """
        dbWork = DbWork()
        numSessions = dbWork.highestSessionId()
        total = 0
        print('Session','NumRecs','QCAnalysed')
        for i in range(1, numSessions + 1):
            print('{}\t'.format(i),'{}\t'.format(dbWork.recCountBySession(i)),'{}\t'.format(qcDumpRecCountBySession(i)))
            total += qcDumpRecCountBySession(i)
        return total
