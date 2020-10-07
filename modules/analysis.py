import matplotlib.pyplot as plt
import json
from os.path import join



def open_json_report(name):
    with open(join('reports', name+'.json')) as f_in:
        data = json.load(f_in)
    
    valid_status=[]
    accuracy=[]
    for row in data['perRecordingStats']:
        valid_status.append(row['is valid?'])
        accuracy.append(row['stats']['accuracy'])
        
    return valid_status, accuracy

def create_plot(name):
    valid_status, accuracy = open_json_report(name)

    for i in range(len(valid_status)):
        print(valid_status[i],'\t',accuracy[i])
    fig = plt.figure() 
    plt.bar(valid_status, accuracy) 
    plt.xlabel(" ") 
    plt.ylabel("") 
    plt.title(" ") 
    plt.show() 
    