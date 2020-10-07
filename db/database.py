from os.path import join
from uuid import uuid4
import boto3
import mysql.connector as mysql
import json



def get_credentials(cred_type):
    with open('./credentials.json') as f:
        credentials = json.load(f)

    return credentials[cred_type]

class S3:
    def __init__(self):
        self.bucket = 'samromur.is'
        self.credentials = get_credentials('s3')
        self.session = boto3.Session(**self.credentials)
        self.client = self.session.client('s3')

    def get_object(self, output_dir, path, ids):
        filename = str(uuid4()) + '.wav'
        filepath = join(output_dir, filename)
        with open(filepath, 'wb') as _file:
            self.client.download_fileobj(self.bucket, path, _file)
        return filename


class MySQL:
    def __init__(self, ids):
        self.credentials = get_credentials('db')
        self.db = mysql.connect(**self.credentials)
        self.cursor = self.db.cursor(dictionary=True)
        self.ids_path = ids

    def get_clips(self):
        ids = self.get_ids() 
        query = (f'SELECT Id, sentence, path, is_valid FROM clips WHERE id IN {*ids,}')
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_ids(self):
        return_list = []
        with open(self.ids_path) as f_in:
            for i in f_in:
                return_list.append(i)
        return return_list
