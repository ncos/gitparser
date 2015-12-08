#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys

def execute(command, critical=True):
    s = "Executing '"+command+"'... "
    if os.system(command) == 0:
        print s + "Success."
        return
    print s + "FAILED!"
    if critical:
        sys.exit(0)

execute("git status")
execute("git checkout master")
#execute("git branch -v")


PATTERN = " --"
REPLACEMENT = "~---"
HASH = "a_t_"

def commit(fname, text, branch, message):
    execute("git checkout -b " + branch)
    f = open(fname, 'w')
    f.write(text)
    f.close()
    execute("git commit -a -m \"" + message + "\"")
    execute("git push origin " + branch)
    execute("git checkout master")
    execute("git reset --hard HEAD", False)


def replace_entry(text, number):
    return text.replace(PATTERN, "FOOBAR", number).replace("FOOBAR", PATTERN, number - 1).replace("FOOBAR", REPLACEMENT)


def apply_pattern(file_list):
    CURRENT_ID = 0
    for name in file_list:
        f = open(name, 'r')
        base_text = f.read()
        f.close()
    
        number = 1
        while(1):
            text = replace_entry(base_text, number)
            if (base_text == text):
                break
            
            commit(name, text, HASH + str(CURRENT_ID), "Update " + name)      

            number = number + 1
            CURRENT_ID = CURRENT_ID + 1


def reset_branches(id_min, id_max):
    for i in range (id_min, id_max + 1, 1):
        branch = HASH + str(i)
        execute("git checkout " + branch)
        execute("git reset --hard origin/master")
        execute("git pull origin master")
    execute("git checkout master")

def delete_branches(id_min, id_max):
    execute("git checkout master")
    for i in range (id_min, id_max + 1, 1):
        branch = HASH + str(i)
        execute("git push origin --delete " + branch, False)
        execute("git branch -D " + branch, False)


filenames = os.listdir("./")
texfiles = []
for f in filenames:
    if ".tex" in f:
        texfiles.append(f)

apply_pattern(texfiles)
#reset_branches(0, 34)
#delete_branches(7, 42)




