from pathlib import Path

import torchaudio
import numpy as np
from tqdm import tqdm


def get_evaluation_data(folder: Path,
                        class_folder: list,
                        resample: int,
                        label: int,
                        ) -> list:

    data = []
    print(f'--processing for {class_folder[label]}')

    # 해당 class의 wav파일이 있는 폴더의 path
    path = folder/class_folder[label]
    file_list = list(path.glob("*"))
    file_list.remove(path/".DS_Store") if path/".DS_Store" in file_list else None
    index_list = []

    # txt 파일을 읽는다.
    if path/"label.txt" in file_list:
        with open(path/"label.txt") as f:
            info = [line.strip().split() for line in f]
            start_list = [float(item[0]) for item in info]
            end_list = [float(item[1]) for item in info]
            index_list = [int(item[2]) for item in info]


    for file in tqdm(file_list):
        if file == path/'label.txt':
            continue

        # 몇번째 wav인지 확인 및 meta 정보 확인
        if '_' in file.stem:
            meta = '_'.join(file.stem.split('_')[1:])
            index = int(file.stem.split('_')[0])
        else:
            meta = 'NA'
            index = int(file.stem)
        
        # load wav file
        y, sr = torchaudio.load(file)
        y = torchaudio.functional.resample(y, sr, resample)
        y = y[0:1, :] # channel이 여러개인 경우 첫번재 channel만 사용

        # txt에 해당 wav파일의 segmentation 정보가 있다면
        if index in np.unique(index_list):
            temp = [i for i, x in enumerate(index_list) if x == index] # segmentation index list
            for i in temp:
                start = int(start_list[i] * resample)
                end = int(end_list[i] * resample)
                wav = y[:,start:end]

                data.append([wav, label, meta])
        
        else:
            wav = y
            data.append([wav, label, meta])

    return data


def check_by_make_wav(data, save_folder, sr):
    current_dir = Path(__file__).parent
    check_wav = current_dir/"check_wav"

    for i in range(len(data)):
        if save_folder not in list(Path(check_wav).iterdir()):
            (check_wav/save_folder).mkdir(parents=True, exist_ok=True)

        torchaudio.save(f"{check_wav/save_folder}/{i}.wav", data[i][0], sr)
