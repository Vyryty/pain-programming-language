# Pain
A silly programming language I made for Programming Languages. I thought it would be funny to just call it "pain", so I tried to make things "pain"-themed. I ended up going for a medieval combat / barbarian theme for things.

## Grammar
Make sure to follow your statements with commas (like you would use semicolons in most programming languages) in order to proceed to the next line. If you don't following lines will be ignored (but still error-checked). The only other major thing is that I didn't get around to making numerical expressions work, so you'll only really be able to do things through a few built-in function calls. The functions you can use are:
* cry(arg1 [, arg2]*) -- works very similarly to "print" in Python
* kind(lit) -- gets the type of a literal
* tellme([prompt]) -- just "input()" from Python, but with an optional prompt to give the user before collecting input
* counter(str) -- takes an input string and returns it reversed
* again(str, count) -- takes an input string and returns it repeated "count" times
* blah(lit) -- casts a literal to the "blah" data type
* num(lit) -- casts a literal to the "num" data type
* mathynum(lit) -- casts a literal to the "mathynum" data type
* by(arg1, arg2) -- multiplies two terms together

Keep in mind that the functions don't actually pay too much attention to how many arguments you pass in, so for functions which don't take an infinite number of parameters, extras will just be ignored (but still error-checked).

## Data Types
* blah -- String
* booboo -- Boolean
    - yea -- True
    - nay -- False
* mathynum -- Float
* num -- Integer
* weapon -- Function

## Errors
Some errors I didn't get around to incorporating, so Python will handle them (and stop the program, so watch out). As for the others, they should tell you the file, the line number, column, and length of the offending token.

## Parse Tree
I made the parse tree able to print itself because it helped me debug some of the program, but as a bonus, it lets you see how your code is getting parsed. Hope you enjoy!