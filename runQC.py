from modules.MarosijoModule import MarosijoTask
from argparse import ArgumentParser
from modules.MarosijoGenGraphs import genGraphs
from db.extractor import Extractor
from os.path import join, exists
from os import mkdir
from json import dump
from config import conf
from modules.analysis import create_plot

def get_clips(ids_to_clips):
    bob = Extractor(ids_to_clips)
    return bob.run()

def create_graphs(tokens):
    genGraphs(tokens)   

def run_QC(recordings, name):
    marri = MarosijoTask(modelPath= 'modules/local', downsample=True)
    report = marri.processBatch(recordings)

    with open(join(conf['reports_path'],f'{name}.json'), 'w') as fout:
        dump(report, ensure_ascii=False, fp=fout, indent=4)

if __name__ == '__main__':
    parser = ArgumentParser(description="""
       lorem ipsum 
       """)

    parser.add_argument('--name', type=str, default='newDayNewDrama', help='Arbritary session name')
    parser.add_argument('--make_graphs', type=bool, default=False, help='Write True or False depending if you want to make the graphs')
    parser.add_argument('--ids', type=str, help='Path to file with ids to examine')
    parser.add_argument('--download', type=bool, default=False, help='If you have already downloaded the files and have the documents ready')
    parser.add_argument('--run_QC', type=bool, default=True, help='If for some reason you just want to create_graphs')

    args = parser.parse_args()
    
    if args.download:
        recordings_info = get_clips(args.ids)
    else:
        '''
        To do, it might not be a good idea to download the recordings from S3 
        '''
        pass

    if args.make_graphs:
        create_graphs(join(conf['archive'], 'tokens.txt'))
    else:
        '''
        To do, If we already have graphs. Maybe not need to do anything, if the graphs are in the right folder. 
        '''
        pass

    if not exists(conf['reports_path']):
        mkdir(conf['reports_path'])

    if args.run_QC:
        run_QC(recordings_info, args.name)

    
    #create_plot(args.name)
    #python3 runQC.py --download True --ids ids_to_test --make_graphs True --name newDayNewDrama
