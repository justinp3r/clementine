# clementine
A lightweight decorator for logging and tracking the usuage of python functions

how to use:

1) clementine.py must exist in the same path like your python module
2) simply add @clementine to your python function.
3) clementine will now track if and how that function gets called and will create a logfile

a terminal output could look like this:

[09.12.23 23:45:23][clementine.py] myFunction1(Argument1=Apfel:str, Argument2=banane:str)\
[09.12.23 23:45:23][clementine.py] myFunction1 -> Apfel
