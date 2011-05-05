#!/usr/bin/python

for source_file in ['farkle.c', 'farkle.clj', 'farkle.factor', 'farkle.hs', 'farkle.py']:
    f = open(source_file)
    character_count = 0
    line_count = 0
    token_count = 0
    for line in f:

        if line == "\n":
            continue

        if len(line.lstrip()) >= 2 and ((line.lstrip()[0] in ['#', ';']) or (line.lstrip()[0:2] in ['/*', '--', '! '])):
            continue

        token_count += len(line.split())
        character_count += len(line)
        line_count += 1
    f.close()

    print source_file
    print "Lines:", line_count
    print "Tokens:", token_count
    print "Average line length:", character_count / line_count
    print "Average token count:", token_count / line_count
    print

