import h5py
import numpy as np
import soundfile as sf
import paramiko
from tqdm import tqdm

import os
import shutil
import time
import argparse
import json
from pathlib import Path

class openh5:
    def __init__(self):
        print("""
                                ,--.     ,-----.
 ,---.  ,---.  ,---. ,--,--,    |  ,---. |  .--'
| .-. || .-. || .-. :|      \   |  .-.  |'--. `\\
' '-' '| '-' '\   --.|  ||  |   |  | |  |.--'  /
 `---' |  |-'  `----'`--''--'   `--' `--'`----' 
       `--'                                     
""")
        print("Welcome to openh5!\n")

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

        working_dir = Path.home()/"Developer"
        utils_dir = working_dir/"Utils"

        with open(utils_dir/"ssh_config.json", "r") as f:
            config = json.load(f)
            self.hostname = config["hostname"]
            self.port = config["port"]
            self.username = config["username"]
            self.password = config["password"]
            f.close()

    def _list_keys(self, print_=True):
        if print_:
            print(list(self.file.keys()))
        return list(self.file.keys())

    def do_sth(self):
        print("What do you want to do?")
        print("1. View keys list.")
        print("2. View keys list and the contents.")

        choice = "thisisnotachoice"
        while choice not in ["1", "2"]:
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
                        if key == "e" or key == "exit()":
                            return
                        elif key == "thisisnotakey":
                            print("Please input the key name.")
                        else:
                            print("Please enter the right key name.")

                        key = input(": ")
                        print()

                    length = len(self.file[key])
                    if key != "wav" and key != "meta":
                        values_array = np.array(self.file[key]).astype(str)
                        for i, value in enumerate(tqdm(values_array)):
                            if "-" in value:
                                values_array[i] = value.split("-")[0]
                        unique_values = np.unique(values_array).astype(str)
                        print(f"{list(unique_values)} in [{key}].")
                    print(f"Which index do you want from {length} indices?")
                    print("Enter exit() to exit, changekeys() to change keys.")
                    
                    idx = "thisisnotanindex"
                    while idx != "exit()" and idx != "e":
                        idx = input(": ")
                        print()

                        if idx == "exit()" or idx == "e":
                            return
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
                                    if choice in ["exit()", "e"]:
                                        return

                                    print("Please enter y or n.")
                                    choice = input("[y/n]: ")
                                    print()

                                if choice == "y":
                                    sr = "thisisnotasr"
                                    while not sr.isdigit():
                                        if sr in ["exit()", "e"]:
                                            return
                                        if sr == "thisisnotasr":
                                            print("Please enter the sample rate.")
                                        else:
                                            print("Please enter an integer.")

                                        sr_16K = "thisisnot16K"
                                        while sr_16K not in ["y", "n"]:
                                            sr_16K = input("Is the sample rate 16000? [y/n]: ")
                                            if sr_16K == "y":
                                                sr = "16000"
                                            elif sr_16K == "n":
                                                sr = input(": ")
                                            else:
                                                print("Please enter y or n.")
                                        print()

                                    cache_pth = Path(__file__).parent/".cache"
                                    cache_pth.mkdir(parents=True, exist_ok=True)

                                    sf.write(cache_pth/"temp.wav", self.file[key][int(idx)], int(sr))
                                    time.sleep(1)

                                    local_transfer = input("Do you want to transfer the audio to local? [y/n]: ")
                                    if local_transfer == "y":
                                        hostname = "172.30.1.56"; port = 22; username = "minseok"; password = "kl;'"

                                        os.system("rsync -Pr ~/Developer/Utils/.cache/temp.wav minseok@172.30.1.56:~/Developer/.cache/")

                                        command = "afplay ~/Developer/.cache/temp.wav"
                                        self._run_ssh_command(command=command,
                                                              )

                                    print(f"\nWav file {'also' if local_transfer else ''} saved to {str(cache_pth/'temp.wav')}!")

                                    done_sign = "thisisnotdone()"
                                    while done_sign not in ["done()", "d"]:
                                        if done_sign in ["exit()", "e"]:
                                            shutil.rmtree(cache_pth)
                                            command = "rm -r  ~/Developer/.cache"
                                            self._run_ssh_command(command=command,
                                                                  )
                                            return

                                        done_sign = input("Enter done() if you're done listening, or enter play() if you want to listen one more time: ")
                                        print()

                                        if done_sign == "done()" or done_sign == "d":
                                            print("Deleting file...")
                                            print()

                                            shutil.rmtree(cache_pth)
                                            command = "rm -r  ~/Developer/.cache"
                                            self._run_ssh_command(command=command,
                                                                  )
                                        elif done_sign == "done_sign()" or done_sign == "p":
                                            print("Playing the audio...")
                                            print()

                                            command = "afplay ~/Developer/.cache/temp.wav"
                                            self._run_ssh_command(command=command,
                                                                  )

                                else:
                                    pass

                            print("Enter 'exit()' to exit, 'changekeys()' to change keys.")
                            print(f"If you want to continue, enter the index number from {length} indices.")
                            print()
            else:
                print("Please enter the right number.")

    def _run_ssh_command(self,
                         command: str,
                         ) -> None:
        hostname = self.hostname
        port = self.port
        username = self.username
        password = self.password

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname, port, username, password)
            stdin, stdout, stderr = ssh.exec_command(command)
            stdout = stdout.read().decode("utf-8")
            stderr = stderr.read().decode("utf-8")

            print(f"STDOUT: {stdout}") if stdout else None
            print(f"STDERR: {stderr}") if stderr else None

        except paramiko.SSHException as e:
            print(f"Connection Failed: {str(e)}")

        finally:
            ssh.close()



if __name__ == "__main__":
    open_h5 = openh5()
    open_h5.do_sth()
