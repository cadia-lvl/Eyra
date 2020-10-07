from os.path import join, exists
from os import mkdir
from shutil import rmtree
from tqdm import tqdm
from db.database import S3, MySQL
import json
from re import sub

def normalisation(token) -> str:
    token = sub('-', ' ', token).lower().rstrip()
    token = sub('[.|,|?|:|„|“|”|!||"|/|\'|(|)|;]','', token)
    return token

class Extractor:
    def __init__(self, path_to_ids):
        self.output_dir = './recordings'
        self.ensure_dirs(self.output_dir)
        self.s3 = S3()
        self.sql = MySQL(path_to_ids)
        self.clips = self.sql.get_clips()

    def ensure_dirs(self, root_dir):
        '''
        Create folders if necessary
        '''
        if exists(root_dir):
            input('The folder output will be overwritten, click to proceed')
            rmtree(root_dir)
        mkdir(root_dir)
        mkdir(join(root_dir, 'audio'))


    def run(self):
        recording_info = []
        with open(join(self.output_dir, 'tokens.txt'), 'w') as t_out:
            for line in tqdm(self.clips):
                filename = self.s3.get_object(join(self.output_dir, 'audio'), line['path'], line['Id']) 

                recording_info.append({
                    "tokenId": line['Id'], 
                    "recPath": join(self.output_dir,'audio', filename),
                    "recId": line['Id'], 
                    "token": normalisation(line['sentence']),
                    "valid": line['is_valid'] 
                    })

                row = f"{line['Id']}\t{normalisation(line['sentence'])}"
                t_out.write(row+'\n')

        with open(join(self.output_dir, 'recordings_info.json'), 'w') as json_file:
            json.dump(recording_info, json_file, ensure_ascii=False, indent=4)

        return recording_info
