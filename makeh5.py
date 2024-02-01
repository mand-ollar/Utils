import h5py
import numpy as np

from pathlib import Path
import sys

import openh5

class make_h5:
    def __init__(self):
        print("Enter the keys you want to make an .h5 file with.")
        self.key_list = list(sys.stdin.readline().split())
        print()

        print("Enter the length of the data.")
        self.data_length = int(input(": "))
        print()

        print("Where do you want to save this .h5 file? Enter the dir.")
        self.save_pth = input(": ")
        print()

        while self.save_pth.endswith(".h5"):
            print("Dir must not include FILE NAME.!")
            self.save_pth = input("Try again: ")
            print()

        print("What do you want for your file name?")
        self.file_name = input(": ")
        print()
        self.save_pth += f"/{self.file_name}.h5"

        while True:
            if Path(self.save_pth).exists():
                print(f"This file [{self.save_pth}] already exists.!")
                print("What do you want to do with it?")
                print()
                print("0] Overwrite")
                print("1] View h5 file")
                print()

                selection = "thisisnotaselection"
                while selection != "0" and selection != "1":
                    selection = input("Choose the numeber: ")
                selection = int(selection)

                if selection == 1:
                    o5 = openh5.openh5()
                    o5.do_sth()
                else:
                    self.h5_file = h5py.File(self.save_pth, "w")
                break

            else:
                print(f"No such directory: [{self.save_pth}]")
                print("Do you wanna make a new path? [y/n]")
                ans = input()
                print()

                while ans != "y" and ans != "n":
                    print("Enter either y or n.!")
                    ans = input()
                    print()

                if ans == "y":
                    Path(self.save_pth).parent.mkdir(exist_ok=True, parents=True)
                    self.h5_file = h5py.File(self.save_pth, "w")
                    if not Path(self.save_pth).is_file():
                        print("Your file path is not an .h5 file.!")
                        Path(self.save_pth).rmdir()
                        ans = "n"
                    else:
                        break

                if ans == "n":
                    print("Enter a new path.")
                    self.save_pth = input(": ")
                    print()

        print(f"Your file will be in [{self.save_pth}].!")
        print()

        for key in self.key_list:
            if key == "wav":
                self.h5_file.create_dataset(name=key,
                                            shape=(self.data_length, ),
                                            dtype=h5py.special_dtype(vlen=np.dtype('float32')),
                                            )
            elif key == "set" or key == "label":
                self.h5_file.create_dataset(name=key,
                                            shape=(self.data_length, ),
                                            dtype=np.int8,
                                            )
            elif key == "source" or key == "meta":
                self.h5_file.create_dataset(name=key,
                                            shape=(self.data_length, ),
                                            dtype=h5py.string_dtype(encoding='utf-8'),
                                            )
            else:
                print(f"Enter the data type you want for {key}.")
                d_type = input()
                self.h5_file.create_dataset(name=key,
                                            shape=(self.data_length, ),
                                            dtype=d_type,
                                            )

        print("Initial settings are done for you .h5.!")
        print()


if __name__ == "__main__":
    m5 = make_h5()
