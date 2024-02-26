import yaml
from pathlib import Path
import importlib.util as iu
import sys


class spellCheck:
    def __init__(self,
                 file_pth: str = "thisisnotapath"  # yaml file path: make sure the file is in DDM/config
                 ):
        # yaml file path: make sure the file is in DDM/config
        if file_pth == "thisisnotapath":
            file_pth = Path(input("Enter the yaml file path: "))
        else:
            file_pth = Path(file_pth)
        # DDM directory path
        ddm_dir = file_pth.parent.parent

        # Load as yaml -> Dictionary
        with open(file_pth, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            f.close()

        # Load as text -> List
        with open(file_pth, "r") as f:
            config_text = f.readlines()
            f.close()

        # Check datasets that are used
        dataset_dict = config["Dataset"]["h5_path"]
        dataset_name = list(dataset_dict.keys())

        # Load dataset_getter of which datasets are used
        dataset_dict = {}
        for dataset in dataset_name:
            spec = iu.spec_from_file_location(dataset, ddm_dir/f"data_getters/get_{dataset}.py")
            module = iu.module_from_spec(spec)
            sys.modules["module.name"] = module
            spec.loader.exec_module(module)

            dataset_dict[dataset] = module.classes

        '''
        Meta spell check:
        We rarely change the meta data part,
        so add the code if it's needed.
        '''

        class_dict = config["Classes"]
        class_name = list(class_dict.keys())
        class_contents = list(class_dict.values())

        num_error = 0
        for i, class_ in enumerate(class_contents):
            dataset_list = list(class_.keys())
            for dataset in dataset_list:
                in_class_list = class_[dataset]["class_name"]
                for in_class in in_class_list:
                    if in_class not in dataset_dict[dataset]:

                        target = [class_name[i], dataset, in_class]; j = 0
                        for line in config_text[config_text.index("Classes:\n")+1:]:
                            if target[j] in line:
                                j += 1
                                if j == 3:
                                    error_line = line.strip()
                                    error_line_num = config_text.index(line)
                                    break

                        print(f"[Error {num_error}] in line {error_line_num+1}")
                        print(f"'{in_class}' is not in {dataset}.")
                        print()
                        print(f"\t{error_line}")
                        print("\t" + "^" * (len(error_line)))
                        print()
                        print()

                        num_error += 1

        print(f"{num_error} errors found!")


if __name__ == "__main__":
    spellCheck("/Users/minseok/DEEPLY/DAL/DDM/config/test.yaml")
