import os
from collections import defaultdict

import humanize
import yaml


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
    with open('interceptions.txt', 'w', encoding='utf8') as out:
        for (d1, d2), size in sorted(interceptions.items(), key=lambda item: item[1], reverse=True):
            print('=' * 80, file=out)
            print(d1, file=out)
            print(d2, file=out)
            print('interception = ', humanize.naturalsize(size), file=out)


if __name__ == '__main__':
    with open('config.yaml', encoding='utf8') as inn:
        data = yaml.safe_load(inn)
    dirs = data['dirs']
    size_limit = data['size limit']
    find_duplicates(dirs, size_limit)
