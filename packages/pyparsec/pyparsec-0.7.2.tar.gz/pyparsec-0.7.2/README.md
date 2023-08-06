# PyParsec

PyParsec is a Haskell combinator library, PyParsec is a parsec library for python 3+

## Installation

```
pip install pyparsec 
```

## Usage

Just like this:

```
>>> import parsec
>>> simple = "It is a simple string."
>>> st = BasicState(simple)
>>> p = many(eq("I"))
>>> p(st)
['I']
```

## What's New

### 0.6.1

 - add built in combinators decorator
 - add ahead

### 0.7.0

 - add result class

### 0.7.2

 - document

