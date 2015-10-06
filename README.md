# snippets

Python snippets for educational purposes


# Statistics

## charcount.py

    cat text.txt | python statistics/charcount.py > charcount.out


Time it!

    time cat text.txt | python statistics/charcount.py > charcount.out

## charcount\_fancy.py

The same as `charcount.py` plus it prints a log message at every 100000th line processed.
If an integer argument is supplied, it only outputs characters that can be found at least N time.
It only affects the output, it doesn't reduce the scripts running time.


    time cat text.txt | python statistics/charcount.py 10 > charcount_fancy.out

## diacritic\_stats.py

Statistics on Hungarian diacritics:

1. number of tokens
1. number of types
1. ratio of words with at least one diacritic
1. lexdif: average number of words that map to the same latinized word (word with the diacritics removed)

The input is expected to be one word-per-line. Example usage:

    cat words | python statistics/diacritic_stats.py

Output format:

    8351 tokens, 3737 types
    1.00214075462 lexdif, 0.490360435876 diacritic ratio

