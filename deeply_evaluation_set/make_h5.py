import h5py
import numpy as np
from tqdm import tqdm
import os
import torchaudio
import torch
from utils import get_evaluation_data
from utils import check_by_make_wav

# class dictionary
classes = {'baby_crying': 0, 'baby_laughter': 1, 'breath': 2, 'cat': 3, 'cough': 4, 'dog': 5, 'doorbell': 6, 'knock': 7, 'sneeze': 8, 'snoring': 9, 
           'speech': 10, 'throat_clearing': 11, 'vaccum_cleaner': 12, 'gunshot': 13, 'scream': 14, 'glass_break': 15}
reverse_classes = {v: k for k, v in classes.items()}

# sort folder list by order of classes dictionary
folder = 'src'
class_folder = sorted(
                    [f for f in os.listdir(folder) if f != '.DS_Store'], 
                    key = lambda x: classes.get(x)
                    )


final_data = []

for i in range(len(classes.keys())):
    label = i
    data = get_evaluation_data(folder, class_folder, resample = 16000, label = i)
    check_by_make_wav(data, reverse_classes[label], sr = 16000)
    final_data += data



total_len = len(final_data)
h5 = h5py.File('Deeply_evaluation.h5', 'w')
dt1 = h5py.special_dtype(vlen=np.dtype('float32'))
dt2 = h5py.string_dtype(encoding='utf-8')
h5.create_dataset('wav', (total_len,), dtype = dt1)
h5.create_dataset('label', (total_len,), dtype = np.int32)
h5.create_dataset('meta', (total_len,), dtype = dt2)

print()
print("--make h5 file")
c = 0
for i in range(total_len):
    h5['wav'][c] = np.array(final_data[i][0].squeeze(0))
    h5['label'][c] = final_data[i][1]
    h5['meta'][c] = final_data[i][2]
    c += 1








#1. 각 폴더내 label.txt를 읽는다

#2. wav를 순회하며 label 정보를 이용해 truncate

#3. 해당 wav와 label을 중첩된 리스트 형태로 저장한다
