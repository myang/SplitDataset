# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import os
from pathlib import Path


# Separate and move certain percentage of training data (categorized by subdirectories) to test data with same
# directory structure. Meanwhile normalize the file names if needed.
def normalize_dataset(percent, work_dir):
    print(f'{percent} data for test')
    print(f'current dir: {work_dir}')

    os.chdir(work_dir)
    dirs = os.listdir()
    min_file_num = get_min_category_file_num(dirs)
    train_file_num = int((1 - percent) * min_file_num)

    # walk through categories
    for subdir in dirs:
        i = 1
        for file_name in os.listdir(subdir):
            curr_path = Path(subdir)
            new_path = curr_path
            new_name = subdir + str(i) + os.path.splitext(file_name)[1]

            if i > train_file_num:
                new_path = Path('../test/' + subdir)

            os.renames(curr_path / file_name, new_path / new_name)
            i = i + 1
    return


# count file numbers of each category directories and return the minimum file number
def get_min_category_file_num(dirs):
    min_category_file_num = 9999
    for d in dirs:
        file_num = len(os.listdir(d))
        if file_num < min_category_file_num:
            min_category_file_num = file_num
    return min_category_file_num


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 2:
        wk_dir = sys.argv[2]
    else:
        wk_dir = Path('.')

    normalize_dataset(sys.argv[1], wk_dir)

