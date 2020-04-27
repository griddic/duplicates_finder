import os
from collections import defaultdict
from pprint import pprint

import yaml


def find_duplicates(dirs, size_limit):
    dirs_map = defaultdict(list)
    for dir in dirs:
        for subdir, dirs, files in os.walk(dir):
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
                for j in range(i + 1,len(folders)):
                    interceptions[(folders[i], folders[j])] += size
    # sorted(interceptions.items(), key=lambda item: item[1])
    pprint(sorted(interceptions.items(), key=lambda item: item[1], reverse=True))

if __name__ == '__main__':
    with open('config.yaml') as inn:
        data = yaml.safe_load(inn)
    dirs = data['dirs']
    size_limit = data['size limit']
    find_duplicates(dirs, size_limit)