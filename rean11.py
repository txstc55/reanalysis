#!/usr/bin/env python

import sys
import re
import string

f = open(sys.argv[1])        # or, f = open('dog')

wordpos = [0.0 for x in range(200)]
dep_h = [0 for x in range(200)]
dep_d = [0 for x in range(200)]
dep_length = [0 for x in range(200)]
word_done = [0 for x in range(200)]

d = 0
starting_d = 0
numdeps = 0

def set_dep_positions(word):

    p = -1
    for x in range(0, len(word)):
        w = word[x]
        if len(w) % 2 == 1:
            z = len(w)
        else:
            z = len(w)-1
        p += (z-1)/2
        p = p+1
        wordpos[x] = p
        p += (z-1)/2
        if len(w) % 2 == 0:
            p = p+1
        p = p+1


def print_sentence(word, w2):

    global numdeps

    dheight = [0 for x in range(200)]
    pos_done = [0 for x in range(1000)]
    word_here = [0 for x in range(1000)]

    # w2 is the index number of the last word to be printed out
    lastpos = wordpos[w2]

    maxheight = 0

    for d in range(0, numdeps):
        dep_length[d] = abs(dep_h[d] - dep_d[d])

    for d in range(0, numdeps):
        dheight[d] = 1

    for z in range(2, w2+1):
        for d in range(0, numdeps):
            if dep_length[d] == z:
                for d2 in range(0, numdeps):
                    if ((dep_h[d2] >= dep_h[d] and dep_d[d2] <= dep_d[d]) or (dep_d[d2] >= dep_d[d] and dep_h[d2] <= dep_h[d])) and dep_length[d2] < dep_length[d]:
                        if dheight[d] <= dheight[d2]:
                            dheight[d] = dheight[d2] + 1

    maxheight = max(dheight)

    for p in range(0, lastpos+1):
        pos_done[p] = 0

    for h in range(maxheight, 0, -1):
        pos = [" " for x in range(1000)]
        for p in range(0, lastpos+1):
            if pos_done[p] == 1:
                pos[p] = '|'
            else:
                pos[p] = ' '
        for d in range(0, numdeps):        
            if dheight[d] == h:
                if dep_h[d] < dep_d[d]:
                    for p in range(wordpos[dep_h[d]]+1, wordpos[dep_d[d]]):
                        pos[p] = '-'
                    pos[int((wordpos[dep_h[d]] + wordpos[dep_d[d]]) / 2)] = '>'
                else:
                    for p in range(wordpos[dep_d[d]]+1, wordpos[dep_h[d]]):
                        pos[p] = '-'
                    pos[int((wordpos[dep_h[d]] + wordpos[dep_d[d]]) / 2)] = '<'
                pos[wordpos[dep_h[d]]] = '+'
                pos_done[wordpos[dep_h[d]]] = 1
                pos[wordpos[dep_d[d]]] = '+'
                pos_done[wordpos[dep_d[d]]] = 1
        for p in range(0, lastpos+1):
            sys.stdout.write(pos[p])
        sys.stdout.write('\n')

    for p in range(0, lastpos+1):
        word_here[p] = 0
        for x in range(0, w2+1):
            if wordpos[x] == p:
                word_here[p] = 1
                if word_done[x] == 1:
                    word_here[p] = 2

    if numdeps > 0:
        for p in range(0, lastpos+1):
            if word_here[p] == 2:
                sys.stdout.write('|')
            else:
                sys.stdout.write(' ')                    
        sys.stdout.write('\n')
                                
    for x in range(0, w2+1):
        print word[x],
    sys.stdout.write('\n')        

    w3 = 0
    first_space = 0
    for p in range(0, lastpos+1):
        if word_here[p] > 0:
            sys.stdout.write(str(w3))
            w3 = w3+1
            first_space = 1
        else:
            if first_space == 1:
                first_space = 0
                if w3 <= 10:
                    sys.stdout.write(' ')
            else:
                sys.stdout.write(' ')
    sys.stdout.write('\n\n')

def parse_input(instring, w):

    global d, total_reanalyses

    starting_d = d
    in_error = 0

    if instring == "-":
        return w
    elif(instring == "n"):
        return -1
    elif(instring == "q"):
        return -2
    elif(re.search('r[0-9]+', instring)):
        restart_point = int(string.replace(instring, "r", ""))
        if restart_point >= w:
            print "You can't start reanalyzing at the current word or later (nothing to reanalyze) - try another response."
            in_error = 1
        elif restart_point == 0:
            print "You can't reanalyze at word 0 (nothing was analyzed at word 0) - try another response."
            in_error = 1
        else:
            print "You have chosen to reanalyze starting at word", restart_point, ". All dependencies from this word onward will be removed."
            # We want d2 to be the number of the next dependency to be assigned. This means it should be the number of the first non-valid
            # dependency (the first one to be wiped out by reanalysis
            d = numdeps                    # First assume that there are no non-valid dependencies
            for d2 in range(0, numdeps):   # Now scan through the dependencies, assign d2 to the first nonvalid dependency found (if any)
                if dep_h[d2] == restart_point or dep_d[d2] == restart_point:
                    d = d2
                    break
            for x in range(0, 200):
                word_done[x] = 0
            for d3 in range(0, d):
                word_done[dep_h[d3]] = 1
                word_done[dep_d[d3]] = 1
            return restart_point-1      # this will get incremented to restart_point before going through the main loop
    else:
        indep = instring.split(' ')
        for i in range(0, len(indep)):
            if re.search('[0-9]+[\<\>]', indep[i]):
                if indep[i][len(indep[i])-1] == ">":
                    dir = 0
                else:
                    dir = 1
                indep[i] = string.replace(indep[i], ">", "")
                indep[i] = string.replace(indep[i], "<", "")
                if int(indep[i]) == w:
                    print "Error: a word can't connect to itself; try again (or press q to quit)"
                    in_error = 1
                    break
                if int(indep[i]) > w:
                    print "Error: you can't connect to an (unseen) word to the right; try again (or press q to quit)"
                    in_error = 1
                    break
                if dir == 0:
                    dep_h[d] = int(indep[i])
                    dep_d[d] = w
                    word_done[int(indep[i])] = 1
                    word_done[w] = 1
                else:
                    dep_d[d] = int(indep[i])
                    dep_h[d] = w
                    word_done[int(indep[i])] = 1
                    word_done[w] = 1
                d = d+1
            else:
                print "Invalid response '", indep[i], "': try again (or press q to quit)"
                in_error = 1
                break

    if in_error == 1:
        d = starting_d
        for x in range(0, 200):
            word_done[x] = 0
        for d2 in range(0, d):
            word_done[dep_h[d2]] = word_done[dep_d[d2]] = 1                
        instring = raw_input()
        instring = string.strip(instring)
        instring = re.sub(' +',' ', instring)
        w = parse_input(instring, w)
            
    return w

# Top-level routine

print "\n    This program is designed to explore how people process sentences. You will see a series of sentences presented\n    one word at a time: first word 0, then words 0-1, then words 0-2, and so on. At each point, you will indicate\n    how you think the newly added word connects to the previous words (in terms of syntactic dependencies). For\n    example, if word 2 is the current word and you think it is the head of word 1, type \"1<\". If you think it is\n    a dependent of word 0, type \"0>\". if you think it is the head of both previous words, type \"0< 1<\". If you think\n    the word is not connected to any previous words (meaning that it must connect to subsequent words), type \"-\".\n\n    If, at any point, you think your previous dependency choices are incorrect and you wish to change them, type\n    \"rN\" where N is the number of the word that you want to go back to. So \"r3\" will undo all the dependencies added\n    from word 3 onwards, and you will start again at word 3.\n\n    Type \"q\" to quit the program, or \"n\" to quit this sentence and go on to the next sentence. Let's begin!\n"

total_words = 0
total_reanalyses = 0
total_sentences = 0

for line in f:

    numdeps = 0
    d = 0
    quit_sentence = 0
    sentence_reanalyses = 0

    for x in range(0, 200):
        word_done[x] = 0

    line = line.rstrip('\n')
    line = string.strip(line)
    line = re.sub(' +',' ', line)

    if len(line) == 0:
        continue;

    print "----------------------"
    print "Starting new sentence:"
    print ""

    word = line.split(' ')

    set_dep_positions(word)

    w2 = 1

    while True:
        print("fdsafd")
        print(numdeps)
        print(dep_h)
        print(dep_d)
        print_sentence(word, w2)
        print("cxvvcxvz")
        print 'Connect word', w2, 'to the previous context:',

        instring = raw_input()
        instring = string.strip(instring)
        instring = re.sub(' +',' ', instring)
        print("abc")
        w3 = parse_input(instring, w2)
        print("w3 is "+str(w3))
        # Normally w3 will equal w2 - the index number of the word just analyzed. If there was a reanalysis, 
        # it will be the word preceding the word to start at in the reanalysis.

        if w3 < w2:
            sentence_reanalyses += 1

        if(w3 < 0):
            if w3 == -1:
                quit_sentence = 1
            if w3 == -2:
                quit_sentence = 2
            print ""
            break

        w2 = w3

        numdeps = d

        print ""

        if w2 == len(word) - 1:
            total_words += len(word)
            break

        w2 = w2+1
        print("something")

    if quit_sentence == 1:
        continue
    if quit_sentence == 2:
        break

    print_sentence(word, w2)
    print("bcd")
    total_reanalyses += sentence_reanalyses
    total_sentences += 1

    # for d in range(0, numdeps):
    #     print "[%d %d]" % (dep_h[d], dep_d[d])
    # print ""

if total_words > 0:
    proportion = float(total_reanalyses) / float(total_words)
else:
    proportion = 0.0
print "Congratulations! You reanalyzed", str(total_reanalyses), "times in", str(total_words), "words and", str(total_sentences), "completed sentences (%.3f reanalyses per word)" % proportion
