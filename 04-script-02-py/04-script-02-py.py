#!/usr/bin/env python3

import os
import sys

path = "./"
if len(sys.argv) >= 2:
    path = sys.argv[1]
    if not os.path.isdir(path):
        sys.exit("Несуществующий путь: " + path)
bash_command = ["cd " + path, "git status 2>&1"]
git_command = ["git rev-parse --show-toplevel"]
result_os = os.popen(' && '.join(bash_command)).read()
if result_os.find('not a git') != -1:
    sys.exit("Не является репозиторием: " + path)
git_top_level = (os.popen(' && '.join(git_command)).read()).replace('\n', '/')
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
    elif result.find('new file') != -1:
        prepare_result = result.replace('\tnew file:   ', '')
        print(prepare_result)
