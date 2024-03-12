from pathlib import Path
global working_dir
working_dir = Path.home()/"Developer"

import h5py
import numpy as np
from tqdm import tqdm

from utils import get_evaluation_data
from utils import check_by_make_wav
import check_stat

def make_h5():
    # class dictionary
    folders = list((working_dir/"Utils/deeply_evaluation_set/src").iterdir())
    classes_list = sorted([f.name for f in folders if f.is_dir()])
    classes = {k: i for i, k in enumerate(classes_list)}
    reverse_classes = {v: k for k, v in classes.items()}

    # sort folder list by order of classes dictionary
    current_dir = Path(__file__).parent
    src_folder = current_dir/'src'
    class_folder = sorted([f.name for f in Path(src_folder).iterdir() if f.is_dir()],
                        key = lambda x: classes.get(x),
                        )

    final_data = []

    for i in range(len(classes)):
        label = i
        data = get_evaluation_data(src_folder, class_folder, resample = 16000, label = i)
        check_by_make_wav(data, reverse_classes[label], sr = 16000)
        final_data += data

    total_len = len(final_data)
    h5 = h5py.File(current_dir/"Deeply_evaluation.h5", "w")
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
    print("Evaluation dataset is saved at .../deeply_evaluation_set/Deeply_evaluation.h5")
    print()

    print("EVALUATION SET STATUS")
    check_stat.check_stat(classes_list)


if __name__ == "__main__":
    make_h5()
