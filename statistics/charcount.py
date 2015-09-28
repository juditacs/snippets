#!/usr/bin/env python2.7
# this is called the shebang line

from sys import stdin
from collections import defaultdict


def main():
    # defaultdict is a dictionary which initializes values
    # automatically to the default of its type,
    # 0 in the case of int or float
    counter = defaultdict(int)

    for l in stdin:  # every line in the input
        text = l.decode('utf8')  # decode from utf-8 encoded string
        text = text.rstrip('\n')  # strip newline from the end of the line
        for character in text:
            counter[character] += 1

    # print counts in decreasing order

    # counter.iteritems yields tuples of (key, value) pairs
    # from the dictionary, we sort it by -value
    for character, count in sorted(counter.iteritems(),
                                   key=lambda x: -x[1]):
        # notice the unicode format string, which is encoded before
        # printing
        print(u'{0}\t{1}'.format(character, count).encode('utf8'))

# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()
