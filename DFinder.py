import os
import shutil
from collections import defaultdict
from os import listdir
from os.path import isfile, join

import humanize
import yaml


def listfiles(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def delete_from_left(left, right):
    right_files = listfiles(right)
    for file in listfiles(left):
        if file in right_files:

            size_left = os.stat(os.path.join(left, file)).st_size
            size_right = os.stat(os.path.join(right, file)).st_size
            if size_left != size_right:
                print(f'File {file} has different sizes. {size_left=} {size_right=} ')
                continue
            os.remove(os.path.join(left, file))
    if len(os.listdir(left)) == 0:
        print(f"{left} will be deleted")
        shutil.rmtree(left)


def delete_from_right(left, right):
    return delete_from_left(right, left)


def merge_to_left(left, right):
    left_files = listfiles(left)
    for file in listfiles(right):
        if file not in left_files:
            shutil.move(os.path.join(right, file), os.path.join(left, file))
        else:
            os.remove(os.path.join(right, file))
    if len(os.listdir(right)) == 0:
        print(f"{right} will be deleted")
        shutil.rmtree(right)


def merge_to_right(left, right):
    return merge_to_left(right, left)


COMMANDS = {
    'delete from left': delete_from_left,
    'dl': delete_from_left,
    'delete from right': delete_from_right,
    'dr': delete_from_right,
    'merge to left': merge_to_left,
    'mtl': merge_to_left,
    'merge to right': merge_to_right,
    'mtr': merge_to_right,
}


def operate(left, right):
    print(f"options are: {COMMANDS.keys()}")
    while (command := input()):
        if command in COMMANDS:
            print(f'I am going to {command}')
            COMMANDS[command](left, right)
            print(f"{command} done.")
            print()
            break
        else:
            print(f"options are: {COMMANDS.keys()}")


def find_duplicates(dirs, size_limit):
    dirs_map = defaultdict(list)
    for dir in dirs:
        for subdir, _, files in os.walk(dir):
            for file in files:
                size = os.stat(os.path.join(subdir, file)).st_size
                if size < size_limit:
                    continue
                dirs_map[(file, size)].append(subdir)
    # pprint(dirs_map)
    interceptions = defaultdict(int)
    for (file, size), folders in dirs_map.items():
        if len(folders) > 1:
            for i in range(len(folders)):
                for j in range(i + 1, len(folders)):
                    interceptions[(folders[i], folders[j])] += size
    # sorted(interceptions.items(), key=lambda item: item[1])
    sorted_interceptions = sorted(interceptions.items(), key=lambda item: item[1], reverse=True)
    with open('interceptions.txt', 'w', encoding='utf8') as out:
        for (d1, d2), size in sorted_interceptions:
            print('=' * 80, file=out)
            print(d1, file=out)
            print(d2, file=out)
            print('interception = ', humanize.naturalsize(size), file=out)
    for (d1, d2), size in sorted_interceptions:
        print(d1)
        print(d2)
        print(humanize.naturalsize(size))

        operate(d1, d2)


if __name__ == '__main__':
    with open('config.yaml', encoding='utf8') as inn:
        data = yaml.safe_load(inn)
    dirs = data['dirs']
    size_limit = data['size limit']
    find_duplicates(dirs, size_limit)
