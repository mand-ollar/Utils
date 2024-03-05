import h5py
import numpy as np
import soundfile as sf

from pathlib import Path
import shutil
import time
import argparse

class openh5:
    def __init__(self):
        parser = argparse.ArgumentParser(description="filepath")
        parser.add_argument("--pth", dest="filepath", type=str, help="filepath")
        args = parser.parse_args()

        if args.filepath is None:
            print("Please input the filepath.")
            filepath = input(": ")
            print()
        else:
            filepath = args.filepath

        self.filepath = filepath
        self.file = h5py.File(filepath, 'r')

    def _list_keys(self, print_=True):
        if print_:
            print(list(self.file.keys()))
        return list(self.file.keys())

    def do_sth(self):
        print("What do you want to do?")
        print("1. View keys list.")
        print("2. View keys list and the contents.")
        choice = input(": ")
        print()

        if choice == "1":
            self._list_keys()
        elif choice == "2":

            change_keys = True
            while change_keys:
                change_keys = False

                key_list = self._list_keys()
                print("Which key do you want to see?")
                print()

                key = "thisisnotakey"
                while key not in key_list:
                    if key == "thisisnotakey":
                        print("Please input the key name.")
                    else:
                        print("Please enter the right key name.")

                    key = input(": ")
                    print()

                length = len(self.file[key])
                unique_values = np.unique(np.array(self.file[key])).astype(str)
                print(f"{list(unique_values)} in [{key}].")
                print(f"Which index do you want from {length} indexes?")
                print("Enter exit() to exit, changekeys() to change keys.")
                
                idx = "thisisnotanindex"
                while idx != "exit()" and idx != "e":
                    idx = input(": ")
                    print()

                    if idx == "exit()" or idx == "e":
                        break
                    elif idx == "changekeys()" or idx == "c":
                        change_keys = True
                        break
                    elif idx.isdigit() and int(idx) >= length:
                        print("Index out of range.")
                        pass
                    elif not idx.isdigit():
                        print("Please enter the index number.")
                        pass
                    else:
                        print(self.file[key][int(idx)])
                        print()
                        if key == "wav":
                            print("Do you want to play the audio?")

                            choice = "thisisnotachoice"
                            while choice not in ["y", "n"]:
                                print("Please enter y or n.")
                                choice = input("[y/n]: ")
                                print()

                            if choice == "y":
                                sr = "thisisnotasr"
                                while not sr.isdigit():
                                    if sr == "thisisnotasr":
                                        print("Please enter the sample rate.")
                                    else:
                                        print("Please enter an integer.")

                                    sr = input(": ")
                                    print()
                                
                                cache_pth = Path(__file__).parent/".cache"
                                cache_pth.mkdir(parents=True, exist_ok=True)

                                sf.write(cache_pth/"temp.wav", self.file[key][int(idx)], int(sr))
                                time.sleep(1)
                                print(f"Wav file saved to {str(cache_pth/'temp.wav')}!")

                                done_sign = input("Enter done() if you're done listening: ")
                                print()
                                
                                if done_sign == "done()" or done_sign == "d":
                                    print("Deleting file...")
                                    print()
                                    shutil.rmtree(cache_pth)

                            else:
                                pass

                        print("Enter 'exit()' to exit, 'changekeys()' to change keys.")
                        print("If you want to continue, enter the index number.")
                        print()


if __name__ == "__main__":
    open_h5 = openh5()
    open_h5.do_sth()
