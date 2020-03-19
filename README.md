# くコ:彡 (The Skwid Programming Language)
 くコ:彡 (Skwid from now on) is a small functional (and arguably esoteric) language whose code compiles directly to Python lambdas, allowing full interoperability with Python 3. This means that every function inside Skwid has a direct translation to Python and can be fed any data type that the parent language allows. To top it off, you only need NumPy to run the compiler!
 
 ## Features
 
 Skwid has the following advantages:
 * Its code is really small, so it's ideal for code golf!
 * It allows tacit programming
 * Great for numerical algorithms
 * Integrating it with Python 3 is trivial
 
 ## Syntax
 
 ### Basics
 
Skwid is a array-oriented, functional language. This means that it excels at working with functions and allows easy composition. If you have ever worked with APL or J, this will be very easy to get.

The basic syntax is as follows:

```html
<integer>       := {0|1|2|3|4|5|6|7|8|9}
<variable>      := {a|b|...|z|A|B|...|Z}
<function-name> := any non-alphanumeric single character
<reference>     := ("#" | "@") <integer>
<expression>    := <integer> | 
                   <variable> |
                   (<function-name> | <reference>) [<expression> {"," <expression>}]
                   "(" <expression> ")"
                    
<skwid-code>    := <expression> {("|" | "\n") <expression>}
```

But enough about the theory! The basic idea is that **any Skwid expression is either a function or a value**. A function can be applied arguments that can also be values or functions. These are the exact rules for application:

Given the following:
* A function ```f => (x1, x2, ..., xn) -> R```
* A function ```g => (y1, y2, ..., yn) -> P```
* A value ```v```

```f(v) = f(x1 = v) => (x2, x3, ..., xn) -> R```

```f(g) = f(x1 = g(y1, y2, ..., yn)) => (y1, y2, ..., yn, x2, x3, ..., xn) -> R```

This means that functions are composed automatically by default. To visualize this, imagine the function ```+```, that takes two elements and sums them. In Skwid, it can be applied like this:

```+1,3```

But that's trivial, let's make something more complex. lets make a function that sums **three elements**. Using the previous rule, we can compose the ```+``` with itself:

```++1,2,3``` = ```+(+1,2),3```

Of course, we can omit the arguments and just type ```++``` to get a lambda that sums three elements.

You may have noticed that arguments are always separated by commas and that there seems to be no mandatory spaces. To be exact, **there cannot be any spaces**, since the Skwid compiler will automatically remove them.

### Variables

Now comes the beautiful world of variables, which are more like kind of named placeholders. Let's imagine that we want to return a function that substracts a number from two. We would do it like this:

```-2```

Since ```-``` is a binary function, the second argument will be the only argument of the returned function. This, however, changes when we want to return a function that substracts two from a number. Since this time around we have to bind the second argument instead of the first one, we use a variable X:

```-X,2```

This will compile into a lambda whose kwargs include X and calculates exactly what it looks like.

### References

This is a key concept to properly organize Skwid code. Any expression can reference any *previous* expression in the code using its index. Let's use an example to understand implicit indexing:

```
ιX,Y|∑#0
```
Some notes:
* ```ι``` is the iota function with arity 2. This means that ```ι2,7``` returns ```[2, 3, 4, 5, 6]``` as a NumPy array.
* ```∑``` is the sum function with arity 1. This means that ```∑X``` returns 10 if ```X``` is ```[1, 2, 3, 4]```.

Having this in mind, we say that the first expression has index 0. Expressions are separated with line jumps and with ```|``` and assigned indexes from left to right and from the top to the bottom.

You can see that the second expression has the argument ```#0```. This means that whatever the first expression returns, it is fed to the second function, so ```∑ιX,Y``` would be equivalent.

As you may have noticed, Skwid does not support recursion yet. I'm figuring how to implement it in a nice way ;)

As a final note, references can be marked with either ```#``` or ```@```. This is because the later **flattens** the reference, which means that any variable that would be needed as a kwarg would be converted into a positional argument **following a lexicographical order**.

### Combinator and higher order functions

As of now, you may have noticed that this function composition paradigm does not support higher order functions. This can be fixed using what I call **combinators**, which are kind of composition tricks.

As of now, Skwid supports the ``` ` ``` combinator, which does the following:

```
`X => () -> (x1, x2, ..., xn) -> X(x1, x2, ..., xn)
```

This effectively returns a function with arity zero that, when applied, returns the original function. This allows the following code:

```
+1|$X,`#0
```

Some notes:
* ```$``` is the map function with arity 2. This means that ```$X,Y``` returns a copy of ```X``` where each element has been applied the unary function ```Y```.
* The composition operator will not preserve the keyword arguments, so references should be flattened when this operator is applied.

### Comments

This is an easy one. We consider that a comment is any sequence of characters that is enclosed in square brackets. Here are some examples:

```
+1|$X,`#0 [This is a comment]

+1|$X,[This is also a comment]`#0

+1|$X,[And
so is
this]`#0
```

You can use comments to add explanations to rather opaque code or to make multi-line expressions!

## Functions
 
I promise I'll get to this section sometime soon :(
