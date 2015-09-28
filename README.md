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
