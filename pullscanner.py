#!/usr/bin/python
# -*- coding: utf-8 -*-

from github import Github
import urllib2, difflib, re, sets, sys

# better to improve this:
g = Github("my_nickname", "my_password")

infosec = g.get_user('vlsergey').get_repo('infosec')
print "Working with " + infosec.name + " (" + infosec.clone_url + ")"

pulls = infosec.get_pulls()

# scan for common regex changes.
# format: label name: [regex for old, regex for new]
REGEX = {"~---": [" -- ", "~---"],
         "~=~": [" = ", "~=~"],
         "т.~д": ["т.~д", "~т.~д"],
         }

PUNCTUATION = ['.', ',', ':']
           
def strregex(s1, s2):
    labels = sets.Set()
    for rid in REGEX.keys():
        if (re.search(REGEX[rid][0], s1) != None) and (re.search(REGEX[rid][1], s2) != None):
            labels.add(str(rid))
    return labels


def strdiff(s1, s2, block1, block2):
    labels = sets.Set()
    start1 = block1.a + block1.size
    start2 = block1.b + block1.size
    end1   = block2.a
    end2   = block2.b

    s_old = s1[start1:end1]
    s_new = s2[start2:end2]

    for letter in PUNCTUATION:
        if (letter in s_old) or (letter in s_new):
            labels.add('punctuation')

    if ('е' in s_old) and ('ё' in s_new):
        labels.add('yofication')

    return ([s_old, s_new], labels)

def analyze_changes(adds, dels):
    if len(adds) != len(dels):
        return [['', '']], sets.Set()

    labels = sets.Set()
    substs = []
    for i in xrange(len(adds)):
        a = dels[i]
        b = adds[i]
        #print a
        #print b

        labels |= strregex(a, b)

        blocks = difflib.SequenceMatcher(None, a, b).get_matching_blocks()

        #print blocks    
        if (len(blocks) - 1 < 2): 
            substs.append(['', ''])
            continue

        for i in range(1, len(blocks) - 1, 1):
            diff, l = strdiff(a, b, blocks[i-1], blocks[i])
            substs.append(diff)
            labels |= l
        
    return (substs, labels)


for pull in pulls:
    f = open("log.txt", 'a')

    print "(" + pull.user.login + ") " + pull.title + ": " + pull.state + "\t" + str(pull.diff_url)

    f.write(pull.user.login + " " + str(pull.diff_url))
    if pull.state != 'open':
        f.write("(!closed!)")
    f.write("| ")

    diff = urllib2.urlopen(pull.diff_url)

    additions = []
    deletions = []

    header_p = True
    header_m = True
    for line in diff:
        if line.startswith('---') and header_p:
            header_p = False
            continue
        if line.startswith('+++') and header_m:
            header_m = False
            continue

        if line.startswith('-'):
            header_p = True
            header_m = True
            deletions.append((line.strip())[1:]+"PADDLE")
        if line.startswith('+'):
            header_p = True
            header_m = True
            additions.append((line.strip())[1:]+"PADDLE")

    substs, labels = analyze_changes(additions, deletions)
    print "Labels = " + str(list(labels))

    for label in list(labels):
        f.write(label + "; ")

    for subst in substs:
        if subst[0] == '' and subst[1] == '':
            print 'NO CHANGES. ERROR IS POSSIBLE'
        print "\t\t'" + subst[0] + "' -> '" + subst[1] + "'"
   

    f.write("\n")
    f.close()



