from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import h5py
from tqdm import tqdm
from tabulate import tabulate

from make_h5 import make_h5

def check_stat(classes: list,
               ):

    ## arguements #####################################################
    current_pth = Path(__file__).parent

    path_dataset = current_pth/"Deeply_evaluation.h5"
    # classes = ['baby_crying', 'baby_laughter', 'breath', 'cat', 'cough', 'dog', 'doorbell', 'knock', 'sneeze', 'snoring', 
    #         'speech', 'throat_clearing', 'vaccum_cleaner', 'gunshot']
    ###################################################################

    dataset = h5py.File(path_dataset, 'r')

    stats = []
    times_list = []
    for i in tqdm(range(len(dataset['label']))):
        times = len(dataset['wav'][i]) / 16000
        label = dataset['label'][i].item()
        stats.append([times, label])
        times_list.append(times)

    # Define a function to calculate stats for each class
    def calculate_class_stats(class_index):
        filtered_stats = [item[0] for item in stats if item[1] == class_index]
        count = len(filtered_stats)
        total_time = sum(filtered_stats)
        mean_time = np.mean(filtered_stats)
        std_dev = np.std(filtered_stats)
        return [classes[class_index], count, total_time, mean_time, std_dev]

    # Create a list of stats for each class
    class_stats = [calculate_class_stats(i) for i in range(len(classes))]

    # Print table using tabulate
    table_headers = ["Class", "Count", "Total Time (seconds)", "Mean Time (seconds)", "Standard Deviation (seconds)"]
    print(tabulate(class_stats, headers=table_headers))
