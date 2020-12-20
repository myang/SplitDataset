# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import os
import shutil
from pathlib import Path


# Separate and move certain percentage of training data (categorized by subdirectories) to test data with same
# directory structure. Meanwhile normalize the file names if needed.
def normalize_dataset(amount, work_dir):
    print(f'current dir:{os.getcwd()}')
    print(f'change to: {work_dir}')
    os.chdir(work_dir)

    if amount[0] == '0':
        amount = float(amount)
        print(f'{amount * 100}% data split for test')

        min_file_num = get_min_category_file_num()
        train_file_num = int((1.0 - amount) * min_file_num)
        create_test_set(train_file_num)
    else:
        create_subset(int(amount))

    return


def create_subset(file_num):
    temp_dir = 'temp'
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)

    sets = {
        'Train': 1.0,
        'Test': 0.2
    }

    for dataset in sets.keys():
        os.chdir(dataset)
        file_num = int(file_num * sets[dataset])
        print(f'create {dataset} folder with {file_num} files per category')

        dirs = next(os.walk('.'))[1]
        for subdir in dirs:
            print(f'{subdir}:', end='')
            curr_path = Path(subdir)
            temp_path = Path('../') / temp_dir / dataset / subdir
            os.makedirs(temp_path)

            i = 1
            for file_name in sorted(os.listdir(subdir)):
                shutil.copy(curr_path / file_name, temp_path / file_name)
                print('.', end='')
                i = i + 1
                if i > file_num:
                    print()
                    break

        os.chdir('..')
    return


def create_test_set(file_num):
    # walk through categories, rename and move the amount of files to subdirectories under 'test' folder
    dirs = next(os.walk('.'))[1]
    for subdir in dirs:
        print()
        print(f'{subdir}:')
        i = 1
        padding = len(str(len(os.listdir(subdir))))

        for file_name in os.listdir(subdir):
            curr_path = Path(subdir)
            new_path = curr_path
            new_name = subdir + str(i).zfill(padding) + os.path.splitext(file_name)[1]

            if i > file_num:
                new_path = Path('../test/' + subdir)

            os.renames(curr_path / file_name, new_path / new_name)
            print('.', end='')
            i = i + 1
    return


# count file numbers of each category directories and return the minimum file number
def get_min_category_file_num():
    min_category_file_num = 9999
    dirs = next(os.walk('.'))[1]
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
