# Python 3.6 ``sre_parse`` module

### Why

The initial motivation to "create" ``sre_parse36`` is to provide a colorizer for regular expressions that produce the *same* expression as initially provided. 

The handling of non-capturing groups changed from Python 3.7, we can't back reproduce the original regular expression from a ``SubPattern`` instance anymore. This regression is tracked at https://bugs.python.org/issue45674, hopefully it will be fixed in a future Python 3.9 bugfix release.

In Python 3.6: 

```python
>>> import sre_parse
>>> sre_parse.parse("(?:foo (?:bar) | (?:baz))").dump()
SUBPATTERN None 0 0
  BRANCH
    LITERAL 102
    LITERAL 111
    LITERAL 111
    LITERAL 32
    SUBPATTERN None 0 0
      LITERAL 98
      LITERAL 97
      LITERAL 114
    LITERAL 32
  OR
    LITERAL 32
    SUBPATTERN None 0 0
      LITERAL 98
      LITERAL 97
      LITERAL 122
```

In Python 3.7 and beyond: 

```python
>>> import sre_parse
>>> sre_parse.parse("(?:foo (?:bar) | (?:baz))").dump()
BRANCH
  LITERAL 102
  LITERAL 111
  LITERAL 111
  LITERAL 32
  LITERAL 98
  LITERAL 97
  LITERAL 114
  LITERAL 32
OR
  LITERAL 32
  LITERAL 98
  LITERAL 97
  LITERAL 122
```


### Install

```
pip install sre_parse36
```

### Usage

Replace ``sre_parse`` by ``sre_parse36``.
