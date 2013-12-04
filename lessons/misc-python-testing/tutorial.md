---
layout: lesson
root: ../..
github_username: your_user_id
bootcamp_slug: yyyy-mm-dd-site
title: Python Testing
---
**By R. David Murray**

## What more is there to testing beside running my program?

When you are writing your program for the first time, you generally
engage in a cycle that goes like this:

1. Decide what you want to do
2. Write some code
3. Run your program
4. Get an error
5. Fix your code
6. Go to 3

Eventually step 4 doesn't produce an error, and you are "done".

Except that in reality you are rarely really done.  Once you've got
your program doing what you want things are great...until you realize
there's something slightly different you need to do, or your new data
set is slightly different from the old one.

We've already talked about using version control to track your changes
when this happens to you, so that you can always get back to a previous
working version of your program if you screw up.

As your program grows in complexity, though, a funny thing happens.
You make a change that gets your new feature working, so when you run
your program in step 3, you get no error in step 4, and you are happy.
But then the next day you go back and need to run your program on your
original data, or to replicate your original results...and you get
an error.

What happened?  You added feature, or maybe even fixed a bug, in one
part of your code, and you broke something that used to be working before
your change.

If you are using version control, you can easily get back to a working
version...but now you have to fix this new bug without breaking your
new feature.  So steps 3 and 4 become:

* Run your program using feature 1
* Check for errors
* Run your program using feature 2
* Check for errors

You can easily see that when you add features 3, 4, and 5, this is going
to get really tedious.

But by now you know the answer to that problem as well.  When you find
yourself repeating a task over and over again, what do you do?


## Test Automation

*The* most important advantage that good experienced programmers have
over the less experienced is the use of automated testing.  At the most
fundamental level this means that the multiple steps above
become just one:

* Run the test suite and see if it passes

In other words, you *automate* running your program in all the ways that
you care about (and as many that you don't care about that you can make
yourself take the time to write tests for).

And you run that test suite *every time you make a change*.  That way
you know *right away* if you break something, instead of finding out
days later when you need your results 'yesterday'.

There are two fundamental features of an adequate set of automated
tests: the result of running the tests should make it *obvious* whether
or not the tests passed, and the test failures should provide enough
information to let you track down the bug that caused the test to fail.
Anything beyond that is a nicety.

How do you create automated tests?  The same way you do anything new with
a computer: you write a program.


## Dumb Testing: diff -r

The simplest form of automated testing, which is neither very sophisticated
nor all that easy to use in the long run, is to write a simple script to
run your program against sample data, and make sure the output matches
what you expect.  It is, however, easy to think about and set up, and since
any tests are better than no tests, it is worth talking about.

To use this form of testing you do have to make your programs minimally
smart: it must be possible to specify both the name(s) of the input
file(s) and the name(s) of the output file(s) when you run the program.

In the `examples` directory of this lesson you'll find a sample program
named `reformat_usaid_map.py` that we'll be using throughout the remainder
of this lesson.

`reformat_usaid_map.py` can be called like this:

    > python reformat_usaid_map.py input_fn output_fn

It reads the data in the file named by input_fn, processes it, and writes
the results to the file output_fn.

In the examples directory you'll also find subdirectories named
`test_data` and `test_results`, and a simple shell script named
`test_reformat_usaid_map.sh`.

The test program looks like this:


    #!/bin/sh
    newdir='new_test_results'
    olddir='test_results'
    rm -rf $newdir
    mkdir $newdir
    python reformat_usaid_map.py test_data/BDKR4JFL.MAP $newdir/BDKR4JFL.CSV >$newdir/data1.stdout 2>$newdir/data1.stderr
    python reformat_usaid_map.py test_data/nosuchfile $newdir/nosuchfile.results >$newdir/nosuchfile.stdout 2>$newdir/nosuchfile.stderr
    python reformat_usaid_map.py test_data/BDKR4JFL.MAP no_such_dir/nosuchdir.results >$newdir/nosuchdir.stdout 2>$newdir/nosuchdir.stderr
    diff -r test_results new_test_results
    if [ "$?" == "0" ]; then
        echo "Tests succeeded"
        rm -rf new_test_results
    else
        echo
        echo "!!! Tests failed !!!"
        echo
    fi

As you can see, this is fairly simple.  It runs the program on some
sample data files and directs the output to a new subdirectory.  It also
captures the programs `stdout` and `stderr` into separate files in that same
new directory.  It then uses the unix `diff` program to compare the output
directory to a copy of the directory that contains the data we expect
the program to produce.  If there are no differences, `diff` has a `0`
return code, and the `if` statement prints the `Tests succeeded` line.
Otherwise `diff` prints the differences, and has a non-zero return code,
in which case the script prints that the tests failed.  Notice that
we only delete the `new_test_results` directory if the tests succeed.
That way we can look through the new results while trying to figure out
what we broke...and we can copy the output files from the test directory
to the test_results directory when we are sure they are correct.

### Exercise:

`cd` into the examples directory of this lesson and run the test
program:

    > ./test_reformat_usaid_map.sh

Now edit the reformat_usaid_map.py program, and "break it" by changing
the name of one of the columns in the COLUMNS variable value.

Then run the test program again and observe the results.

Finally, edit `reformat_usaid_map.py` again, and this time break it
by making a python syntax error such as misspelling a keyword.

Run `test_data_processor.sh` again.

To undo your changes to `reformat_usaid_map.py`, do the following:

    > git checkout reformat_usaid_map.py


## Automated Testing Tools

Programmers being programmers, we have of course written tools to help
with testing.  We will cover two such tools for Python: doctest and
nose/unittest.

## Doctest

Let me preface this section by saying that there are people who think
doctests are evil and shouldn't be used, and others who love them (for
what they are good for).

doctests have one large advantage for the beginner: they are *easy*
to write.  Having tests is *way* better than having no tests, so in my
opinion anything that makes them easier to write makes them more likely
to exist and is therefore good.  But do keep in mind that doctests have
limited capabilities, and when your code base and tests start to get at
all complicated, you really want to be using unittests instead.

You'll understand why when we get to the unittest example.

Remember I said that adequate tests have two characteristics: they make
it clear when a failure occurs, and they help track down the problem.
Our simple scripted automated testing satisfies the first, but it often
*doesn't* satisfy the second.  A traceback might get printed to the
console followed a huge diff in the resulting data, and the traceback
scrolls off the screen before you can see it.  `less` can solve that
problem, but the general problem remains: the errors produced by diff
aren't necessarily easy to track back to the code that produced them.

What we really want to do is test the individual *parts* of our program
one by one.  For example, at the Python interactive prompt we could play
around with the `reformat_usaid_map.py` function `reformat_spec_line`
like this:

    >>> from process_data import normalize_string
    >>> spec = 'CASEID            (id) Case Identification                1   15   AN    I    1   0   No   No'
    >>> reformat_spec_line(spec)
    ['CASEID', '(id) Case Identification', '1', '15', 'AN', 'I', '1', '0', 'No', 'No']

(I cut and pasted that string from the sample data file.)

Guess what?  We just wrote a doctest.  And the .md source file for this
page could now be run as a test file using doctest.

In general a great way to write doctests is to run some experiments
at the Python prompt, and then save the test by cutting and pasting it
into your doctest file.  A better way is to write the output by hand,
based on what you expect the output to be.  (I usually do a mixture of
the two in practice.)

Doctests are similar in principle to our scripted test using diff,
in that the output of the commands is compared to what is actually
returned when the preceding command is executed, and if it is different,
both the expected and the actual result are printed.  The difference
is we are testing individual functions with individual bits of data,
which means the test failure is *localized* to right where the problem
is, making it easier to find and fix.  (You'll see in a moment that it
doesn't help with finding what exactly changed in the output when the
difference is subtle, though!)

A single doctest file is like a single interactive interpreter session
or a single iPython Notebook page: everything you do (imports, giving
a value to a variable, etc) affects the later examples, even if you put
non-doctest text in between the doctest snippets.

### Exercise:

In the examples directory, take a look at the `reformat_usaid_map.doctests`
file, and then run the following command:

    > python -m doctest reformat_usaid_map.doctests

If you remembered to undo your changes to `reformat_usaid_map.py`, you will
just get the prompt back (no output).  This means the tests succeeded.
If you would prefer more feedback that the tests actually succeeded
(not a bad idea), you can run the doctests this way:

    > python -m doctest -v process_data.doctests

Try it.

Now edit `reformat_usaid_map.py` and change a column name again, and
re-run the tests.  Notice how you can go to the line in the doctest
file where it says that the test failed, and see that the problem is
occurring in the generate_csv function somewhere.

Now try making a syntax error.  This time you get many more failures,
but I think it is easier to see and understand the tracebacks than
it was with the shell script tests.

Again, reset your reformat_usaid_map.py file:

    > git checkout reformat_usaid_map.py
    

## nose and unittest

`unittest`, like `doctest`, is a module included in the Python Standard
Library.  `nose` is a third party program, that comes bundled with
Anaconda and Canopy, that makes running unit tests easier.

Unit test are a little harder to write (they require a bit more
scaffolding), but the huge advantage is that they are designed to
be *unit* tests, which means that the goal is to reset everything to
"ground zero" before running each test, so that you are testing isolated
bits of code.  Unlike a doctest, unless you make a mistake the things
you do inside one test do *not* affect things you do inside other tests.

Here is the above doctest example rewritten as a unit test:

    from reformat_usaid_map import reformat_spec_line
    from unittest import TestCase

    class ReformatTests(TestCase):

        def test_reformat_spec_line(self):
            self.assertEqual(
                reformat_spec_string(
                    'CASEID            (id) Case Identification'
                    ' 1   15   AN    I    1   0   No   No'),
                ['CASEID', '(id) Case Identification', '1', '15',
                    'AN', 'I', '1', '0', 'No', 'No'])

That may look like a more work than a doctest (and it is), but the
advantage will become clear when you start dealing with more complicated
programs and tests.  You'll see one of the advantages when you do the
example.

A test case can have any number of test methods.  Each one is run
individually and the results reported individually.

### Excercise:

Take a look at the file `test_reformat_usaid_map.py` in the examples directory.

In the exercises directory, run the following command:

    > nosetests

This automatically "discovers" all of the `.py` files that contain
classes that are subclasses of `unittest.TestCase`, collects all of
the methods of those classes whose name begins with the string `test_`,
and runs them one by one, reporting the results.  Each '.' represents
a single successful test method.

You know the drill by now: edit `reformat_usaid_map.py` and break it,
first by changing the column name, then by making a syntax error,
and re-run the `nosetests` command each time to see what it does.
Like `doctest`, `nosetests` has a `-v` option you might want to try out
as well.


## Bonus Exercise:

Perhaps we will be processing more than one MAP file, and we will end up
concatenating all the output files together.  We'll only want one header
line in that case.  So let's add an option to suppress generating the
header line.  You can add the option by adding a line like this to the
`__main__` part of the program:

    parser.add_argument('-n', '--no-header', action='store_true', default=False,
                        help='Suppress the header line')

With that in place, `args.no_header` will be `False` unless the `-b`
option is specified when the command is run.  You can then pass
the `args.no_header` value to the `generate_csv` function to
control whether or not it produces the header.

The exercise is to *first* add a new unit test method to
`test_reformat_usaid_map.py` and a new command line test to
`test_reformat_isaid_map.sh` that exercise the new behavior and tests
that it produces the correct output.  Run the tests and confirm that
your new test fails.  *Then* modify `reformat_usaid_map.py` to add the
new option, and run your test suite as many times as it takes to get
your new code working.

Note: unless you know about and use a keyword argument, you will also
have to modify the existing `test_generate_csv` test method slightly to
account for the new `generate_csv` function signature.  Do *not* however,
modify it into the new test.  You should have two different tests for
`generate_csv` at the end of the exercise: the one with the original
output, and the one with the new output.
