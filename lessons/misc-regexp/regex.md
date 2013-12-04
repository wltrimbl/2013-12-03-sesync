
#  Regular Expressions

When manipulating strings, the task of finding a string that contains a certain substring is 
very common--we can use `string.find(bigstring, smallstring)` to check for this, but often we
need more flexibility than exact matches. 

Regular expressions are a convention for speccifying match patterns that allow us to match
match more complicated patterns.   Sometimes regular expressions are likened to a miniature
programming language.   There are slight variations in regular expression syntax between
perl, python, and unix utilities like grep, sed, and awk, but the essential funcitonality is 
the same.  

# Regular expression syntax resembles wildcard shell expansion 

But the agreement is not perfect:
*  In the shell, the '?' character is the single-character wildcard; it matches any character except '/'.
*  In regular expresisons syntax '.' is the single-character wildcard; it matches any character except the newline.
*  In the shell, the * characer matches zero or more characters (except '/') 
*  In regular expressions syntax ".*" is a combination of the single-character wildcard and the "zero or more times" quantifier.


`ls /bin/??              # list files in /bin with exactly two characters in their name`
`ls /bin | grep '^..$'   # do the same using grep  ` 

`ls /bin/* `

`ls /bin | grep '.*'  `

Speaking of the shell, since some of the punctuation marks in regular expressions ( like ? and *) 
have meaning to the shell, it is good practice to put quotation marks around regular expressions 
when using them on the command line. 

If our only task is filtering data line-by-line for matching a pattern, `grep` is our friend.
We can show the most important parts of regular expression syntax by using `grep` to select
lines from `months.txt` and `crossword.txt`, a list of the names of the 12 months and a list
of 227,000 english words.  (Note: this is an easy way to cheat at crossword puzzles.)

If our task has us extracting multiple fields from an expression, we probably want to use
regular expressions in a scripting language like python.

#grep syntax

    grep pattern [file]
    Grep searches the named input FILEs (or standard input if no files are named) for lines 
containing a match to the given PATTERN.  By default, grep prints the matching lines.

If we invoke grep with only one argument, it waits for input from standard in.  If we invoke
with two arguments, `grep` treats the second argument as a filename and searches for the pattern
in that file.  When we invoke `grep` with more than two arguments, all but the first argument
are taken as filenames, and the output is prepdended with the name of the filename.

# Regexpal
The site
[http://regexpal.com/](http://regexpal.com/)
Has a form for a regular expression and a form for the data.  The website will highlight 
the parts of your data that match your regular expression on the fly.

# Exact matches

Most characters (including letters and numbers) match themselves in regular expressions.  

`grep 'm' months.txt`

Shows us a list of the lines in `months.txt` that contain a lower-case m anywhere in the line, 
in this case, months containing the letter m not as their first letter.

`grep 'z' months.txt`

Shows us a list of the lines in `months.txt` that contain a lower-case z anywhere in the line.
There aren't any, so the output is empty.

`grep anders crossword.txt`
shows all the lines in the file that contain the exact string anders

That's nice.  Suppose we want only the lines that begin or end with a given string?

# Beginning / end of line symbols

The character  ^ (  **caret** ) at the beginning of a pattern will force a match to occur at the 
beginning of a line.  Matches not at the beginning of the line won't match.

`grep '^[mM]' months.txt`

Will only show me the names of months that begin with M, but doesn't include September.

The character  $ (  **dollar sign** ) will force a match to occur at the end of a line.

`grep 'r' months.txt`
shows all months with an r in the name
`grep 'r$' months.txt 
shows all months which end in r 

This gives us a simple test for empty lines:
`grep '^$' `

# Character classes

Sets of characters that are enclosed in square brackets match a single character whose value 
is any of the enclosed characters:

`grep '[mM]' months.txt`
Shows us a list of the lines in `months.txt` that contain an m or M anywhere in the line.

`grep '[ae]' months.txt`
Shows us a list of the lines in `months.txt` that contain a lower-case e or a anywhere in the line.

When the opening [ is followed by a caret, the block instead matches all characters except the 
listed characters : 

`grep '^[^aeiou]` crossword.txt  ` 
matches all the words that do not begin with vowels.

`grep '^[^aeiou][aeiou][aeiou]$` crossword.txt  ` 
matches all the three-letter words that start with a consonant and end with two vowels.

# Quantifiers

Quantifiers are where the real power of regular expressions appears.  Characters and character
classes can be modified to match 0 or 1, 1 or more, or 0 or more times, or even a specified number
of times. 

`grep '^[^aeiou][aeiou]*$' `
matches all the words consisting of exactly one consonant and zero or more vowels.

# Python regexp syntax.

What you need to know is described in the [Python documentation on the re module](http://docs.python.org/2.7/library/re.html), but it's a little dry.  

The essentials:  
you need the line `import re` to use regular expressions.  This is built in to python.

```
import re
match_object = re.search(pattern, string_to_be_searched)
if match_object != None:
    print match_object.string
```

`re.search(pattern, string_to_be_searched)` is the basic
syntax for searching for a (possibly complicated) pattern.
Likemany of the regular expression methods, it returns
"match objects" if there is a match, and "None" if there
is no match.  It is conventional to test whether a match
is equal to None, and if not, get the data out.  Trying
to get the data out of a NoneType object results in an error.

# Grouping

Within regular expressions, we will often desire to match more 
than one pattern
at the same time, or to extract different parts of the matched string
as different variables.

This can be accomplished by using groups.  Sets of symbols enclosed
in parentheses will be returned as separately accessible variables.

Suppose we wanted to match the html link address and the tag text 
from a webpage.
```
import re
s = "<a href=THISISAMONSTER.ZIP>tag</a>"
matchresult=re.search(r"a href=(.*?)>(.*?)<", s)
if matchresult != None:
    print matchresult.groups()
```

# Scraping

Sometimes you will get data is a less than convenient
format.  Like HTML.  This page 
http://www.ncbi.nlm.nih.gov/projects/WGS/WGSprojectlist.cgi
Has a list of several thousand datasets in an HTML table;
they have dataset numbers, organism names, urls, and 
some summaries of the data.  Suppose we wanted to extract
all the urls (and later decide which urls looked relevant
to our research).

Exercise:
Use curl to download this page.
```
curl http://www.ncbi.nlm.nih.gov/projects/WGS/WGSprojectlist.cgi > WGSprojectlist.html
```

Go through the page one line at a time.
Use a regular expression to find the href=URL tags.
Print all the urls linked on the page.


