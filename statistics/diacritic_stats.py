#-*- coding: utf-8 -*-
#!/usr/bin/env python2.7
# this is called the shebang line

from sys import stderr, stdin
from collections import defaultdict
import re
from string import punctuation  # collection of punctuation marks


def main():
    # defaultdict is a dictionary which initializes values
    # automatically to the default of its type,
    # empty set in this case.
    # We are interested in the number of different words that
    # are the same when all diacritics are removed
    # e.g. kor -> kor, kór -> kor, kör -> kor, kőr -> kor
    # kor has 4 possible original forms including itself,
    # kor will be the <key> in this dictionary and the possible forms
    # observed in the input will be added to the <value>
    latinized_forms = defaultdict(set)

    # in linguistics the occurence of a single entity (typically a word)
    # is called _token_ and each unique entity is called _type_
    # the number of tokens and types will be accumulated in these variables,
    # the built-in set type is useful for collecting unique types
    word_types = set()
    token_num = 0

    # number of words with at least one diacritic
    dia_num = 0

    # Hungarian diacritics map
    # we want unicode NOT utf-8 encoded characters, so decode is necessary
    diacritics = {
            'á'.decode('utf8'): 'a',
            'é'.decode('utf8'): 'e',
            'í'.decode('utf8'): 'i',
            'ó'.decode('utf8'): 'o',
            'ö'.decode('utf8'): 'o',
            'ő'.decode('utf8'): 'o',
            'ú'.decode('utf8'): 'u',
            'ü'.decode('utf8'): 'u',
            'ű'.decode('utf8'): 'u',
    }
    dia_set = set(diacritics.keys())  # for convenience

    # filter punctuation with this regex
    # it matches every line that contains only puncutation
    # re.UNICODE is necessary for unicode strings
    punct_re = re.compile(r'^[{0}]+$'.format(re.escape(punctuation)), re.UNICODE)
    # one word per line is expected
    for l in stdin:  # every line in the input
        word = l.decode('utf8').strip()  # decode from utf-8 encoded string
        if punct_re.match(word):
            continue
        word_types.add(word)
        token_num += 1 # no ++ operator in Python

        if token_num % 1000000 == 0:
            stderr.write('{0} tokens read\n'.format(token_num))

        if set(word) & dia_set:  # the word has at least one diacritic
            dia_num += 1
            # list comprehension and one-line if combined
            latinized = ''.join(diacritics[c] if c in dia_set else c for c in word)
            latinized_forms[latinized].add(word)

    lexdiff = 0
    for type_ in word_types:
        # the built-in dict's get method allows us to assign a default value if
        # the key is not present in the dictionary
        diff_form = len(latinized_forms.get(type_, set()))
        # let's not forget the non-diacritic form
        lexdiff += diff_form + 1

    lexdiff /= float(len(word_types))  # int/int is int unless we cast at least one operand

    print('{0} tokens, {1} types'.format(token_num, len(word_types))) 
    print('{0} lexdif, {1} diacritic ratio'.format(lexdiff, float(dia_num) / token_num))

# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()
