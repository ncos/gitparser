#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator

labels = {}

def safe_add(user, label):
    if label not in labels.keys():
        labels[label] = {}

    if user not in labels[label].keys():
        labels[label][user] = 1
        return

    labels[label][user] += 1

    

f = open('log.txt', 'r')
for line in f.readlines():
    s = line.strip().split('| ')
    name = s[0].split(' ')[0].strip()

    if len(s) != 2:
        safe_add(name, 'other')
        continue

    lbls = s[1].strip().split(';')

    for label in lbls:
        if len(label) < 1:
            continue
        safe_add(name, label.strip())

f.close()

for label in labels.keys():
    print "\n" + label
    for name, num in sorted(labels[label].items(), key=operator.itemgetter(1), reverse=True):
        print "\t" + name + ": " + str(num)



