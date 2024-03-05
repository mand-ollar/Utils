import random
import time
import os
import json
from pathlib import Path

import h5py
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import StratifiedGroupKFold


'''
0. Silence
1. Gunshot
    - UrbanSound8K, AIhub_Nonverbal, Tropical_gunshot, VGGSound: original dataset split = set
    - TUTRare: only for TRAIN set
    - Kaggle, Forensic, BGGSound: GroupStratified K-Fold (TRAIN / VALID / TEST)
2. Noise
3. Human Speech
4. Others

Apply random split to the rest (8:2)
VocalSound, FSD50K: originally split by TRAIN / VALID / TEST, which means set can include 0, 1, 2. -> "CAUTION for indexing"
'''


def _check_file(file_pth: str,
                ):
    file_pth = Path(file_pth)
    extension = file_pth.suffix

    if extension == ".h5":
        valid = h5py.is_hdf5(file_pth)
    else:
        valid = file_pth.is_file()

    return valid

def _h5_status(h5_file: h5py.File,
               ):
    keys_list = list(h5_file.keys())
    data_length = str(len(h5_file[keys_list[0]]))
    keys_list = "  ".join(keys_list)

    # Formatting
    title_len = len("[H5 FILE INFO]") # 14
    keys_len = len(f"       Keys:\t{keys_list}")
    data_len = len(f"Data length:\t{data_length}")
    orig_max_len = max(title_len, keys_len, data_len) + 1

    is_max_len_odd = orig_max_len % 2    # 0 or 1
    max_len = orig_max_len + is_max_len_odd

    print()
    print(" -" + "-" * (max_len // 2 - 7) + " [H5 FILE INFO] " + "-" * (max_len // 2 - 7) + "- ")
    print("| " + " " * (max_len + 2) + " |")
    print("| " + f"       Keys:\t{keys_list}" + " " * (max_len - keys_len + 1) + " |")
    print("| " + f"Data length:\t{data_length}" + " " * (max_len - data_len + 1) + " |")
    print(" -" + "-" * (max_len + 2) + "- ")
    print()

def _check_spell(pth: Path,
                 ):
    with open(pth, "r+") as f:
        text = f.read().split("\n")
        f.close()

    c = 0

    for i, t in enumerate(text):
        split_it = ": " in t

        orig, t = t.split(": ") if split_it else (None, t)
        gone_through = False

        temp = t[:-1] if t.endswith(",") else t
        if temp == "true" or temp == "false":
                continue

        if t.endswith(","):
            if t.startswith('"') and t[:-1].endswith('"'):
                print(t)
                continue
        else:
            if t.startswith('"') and t.endswith('"'):
                print(t)
                continue

        true_error = ["True", "ture", "treu", "Treu", "Ture", "Teru", "Tuer"]
        for error in true_error:
            if error in t:
                c += 1

                print(f"[Error{c}]")
                print(f"Line {i + 1}: {orig + ': ' + t + ','}")

                replace = "true"
                text[i] = orig + ": " + replace + ","
                print("Corrected: ", text[i])
                print()

                gone_through = True

        false_error = ["False", "fale", "flase", "flsae", "Flase", "Fales", "Fasle"]
        for error in false_error:
            if error in t:
                c += 1

                print(f"[Error{c}]")
                print(f"Line {i + 1}: {orig + ': ' + t + ','}")

                replace = "false"
                text[i] = orig + ": " + replace + ","
                print("Corrected: ", text[i])
                print()

                gone_through = True

        if not gone_through:
            if len(t) == 0:
                pass
            elif t[-1] == ",":
                text[i] = orig + ": " + f'"{t[:-1]}",' if split_it else t
            else:
                text[i] = orig + ": " + f'"{t}"' if split_it else t

    text = "\n".join(text)

    with open(pth, "w") as f:
        f.write(text)
        f.close()

    print("\n.")
    time.sleep(0.3)
    print("\n.")
    time.sleep(0.3)
    print("\n.\n\n")
    time.sleep(0.3)

    print("Press enter to continue...")
    input()


class splitData:
    def __init__(self,
                 file_pth: str = None,
                 ) -> None:
        self.current_dir = Path(__file__).parent

        check_file = False

        # Get h5 file path if not given
        while not check_file:
            if file_pth is None:
                print("Enter the path of the h5 file: ")
                file_pth = input(": ")
                check_file = _check_file(file_pth)
                print()

                if not check_file:
                    print("File path is not valid. Please enter a valid path.")
                    file_pth = None
                    print()

            else:
                answer = None
                while not answer:
                    print(f"Your h5 file path is {file_pth}. [y/n]?")
                    answer = input(": ")
                    print()

                    if answer.lower() == "y":
                        check_file = _check_file(file_pth)
                        if not check_file:
                            print("File path is not valid. Please enter a valid path.")
                            file_pth = None
                            print()

                    elif answer.lower() == "n":
                        file_pth = None

                    else:
                        print("Please input 'y' or 'n'.")
                        print()
                        answer = None

        self.file_pth = Path(file_pth)

        # Load h5 file
        self.h5_file = h5py.File(file_pth)
        self.h5_len = len(self.h5_file["label"])
        self.h5_labels = self.h5_file["label"]
        self.h5_sources = self.h5_file["source"]

        # Check h5 file status
        os.system("clear")
        print()
        print(file_pth)
        _h5_status(self.h5_file)

        print("\n.")
        time.sleep(0.3)
        print("\n.")
        time.sleep(0.3)
        print("\n.\n\n")
        time.sleep(0.3)

        print("Press enter to continue...")
        input()

    def define_types(self,
                     ) -> None:
        source_list = []
        for source in self.h5_sources:
            source = source.decode("utf-8")
            if "-" in source:
                source = source.split("-")[0]
                if source not in source_list:
                    source_list.append(source)
            else:
                if source not in source_list:
                    source_list.append(source)

        source_dict = dict.fromkeys(source_list)

        # Save as json file
        cache_folder = self.current_dir / ".cache"
        cache_folder.mkdir(exist_ok=True, parents=True)
        with open(cache_folder / "source_dict.json", "w") as f:
            json.dump(source_dict, f, indent=4)
            f.close()

        # Editing json file
        os.system("clear")
        print()
        print("You're gonna see the contents of 'json' file.\n")
        print(">>> If a source needs GroupStratified K-Fold, write True.")
        print(">>> If it doesn't, write False.")
        print()
        print(
'''Example:\n
{
    "UrbanSound8K": True,
    "AIhub_Nonverbal": True,
    "VGGSound": False,
    "Kaggle_gunshot": True,
    "BGGSound": False
}
''')
        is_bool = False
        while not is_bool:
            print("\n.")
            time.sleep(0.3)
            print("\n.")
            time.sleep(0.3)
            print("\n.\n\n")
            time.sleep(0.3)

            print("Press enter to continue...")
            input()

            os.system(f"nano {cache_folder}/source_dict.json")
            os.system("clear")
            print()

            _check_spell(cache_folder/"source_dict.json")
            os.system("clear")

            # Done editing
            with open(cache_folder/"source_dict.json", "r") as f:
                source_dict = json.load(f)
                f.close()

            # Verify if all values are boolean
            values = list(source_dict.values())
            for value in values:
                is_bool = value.__class__ == bool
                if is_bool:
                    pass
                else:
                    break

            if not is_bool:
                print("All values should be boolean. Please check the json file.\n")
                with open(cache_folder/"source_dict.json", "w") as f:
                    json.dump(source_dict, f, indent=4)
                    f.close()

                print()
                continue

        # Remove the json file and .cache folder
            (cache_folder/"source_dict.json").unlink()
            cache_folder.rmdir()

    def index_split_by_label(self,
                    ) -> None:
        # Clear the terminal
        os.system("clear")

        # Set json folder path
        json_folder = self.current_dir/"json"
        json_folder.mkdir(exist_ok=True, parents=True)
        idx_pth = json_folder/f"idx_by_label--{self.file_pth.name}.json"

        # Get unique labels
        self.labels_list = np.unique(np.array(self.h5_labels)).astype("str")
        idx_by_label = dict.fromkeys(self.labels_list)

        # If there's json file, load it. Otherwise, create one.
        # It doesn't take that long.
        if not idx_pth.is_file():
            for label in self.labels_list:
                print(f"Loop for {label}...")
                temp_list = []

                for i in tqdm(range(self.h5_len)):

                    if label == str(self.h5_labels[i]):
                        temp_list.append(i)

                print()
                idx_by_label[label] = temp_list

            with open(idx_pth, "w") as f:
                json.dump(idx_by_label, f, indent=4)
                f.close()

        else:
            with open(idx_pth, "r") as f:
                idx_by_label = json.load(f)
                f.close()

        keys_list = idx_by_label.keys()
        keys_list = [int(k) for k in keys_list]

        idx_by_label_copy = idx_by_label.copy()
        idx_by_label = dict.fromkeys(keys_list)
        for k in keys_list:
            idx_by_label[k] = idx_by_label_copy[str(k)]

        self.idx_by_label = idx_by_label

    def index_split_by_source(self,
                              ) -> None:
        for label in self.labels_list:
            
            pass


if __name__ == "__main__":
    split_data = splitData("/data/ListenCity/gunshot_train_v_0.1.6.h5")
    split_data.index_split_by_label()
