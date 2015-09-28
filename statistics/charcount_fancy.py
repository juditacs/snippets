#!/usr/bin/env python2.7
# this is called the shebang line

from sys import argv, stderr, stdin
from collections import defaultdict


def main():
    # skip characters that appear less than <cutoff> times
    if len(argv) > 1:
        cutoff = int(argv[1])
    else:
        cutoff = 0
    # or in one line:
    # cutoff = int(argv[1]) if len(argv) > 1 else 0

    # defaultdict is a dictionary which initializes values
    # automatically to the default of its type,
    # 0 in the case of int or float
    counter = defaultdict(int)

    # let's give some idea about the progress of the script
    # print a counter every 100000 lines
    # we shouldn't print this to STDOUT, it would mix in
    # with our real output
    # STDERR (or some more sophisticated logging mechanism)
    # should be used in these cases
    line_cnt = 0

    for l in stdin:  # every line in the input

        # increment at every line but only print after 1M lines
        line_cnt += 1
        if line_cnt % 100000 == 0:
            # NOTE unlike print, the function write does not print a
            # newline at the end.
            # This can be prevented in the case of print too, just put
            # a comma at the end:
            # print "spare me of your newlines",
            stderr.write('{0} lines read\n'.format(line_cnt))

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
        if count >= cutoff:
            print(u'{0}\t{1}'.format(character, count).encode('utf8'))

# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()
