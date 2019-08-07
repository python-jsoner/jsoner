# jsoner

*A thin wrapper of Python stdlib's json module to convert objects to JSON and back, with the purpose of maintaining readability of objects serialized with old versions of their class definition.*

[![Build Status](https://travis-ci.org/python-jsoner/jsoner.svg?branch=master)](https://travis-ci.org/python-jsoner/jsoner) [![Tests Status](https://python-jsoner.github.io/jsoner/junit/junit-badge.svg?dummy=8484744)](https://python-jsoner.github.io/jsoner/junit/report.html) [![codecov](https://codecov.io/gh/python-jsoner/jsoner/branch/master/graph/badge.svg)](https://codecov.io/gh/python-jsoner/jsoner) [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://python-jsoner.github.io/jsoner/) [![PyPI](https://img.shields.io/badge/PyPI-jsoner-blue.svg)](https://pypi.python.org/pypi/jsoner/)


## Installing

```bash
> pip install jsoner
```

## Usage

Let's make a class JSON-able: we have to

 - inherit from `JSONAble`
 - decorate it with the `@json_info` annotation to declare the associated json "schema" id and version
 - *optionally* implement `__from_json_dict__` (class method called during decoding) and/or `__to_json_dict__` (instance method called during encoding) if we wish to have control on the process, for example to only dump part of the attributes or perform some custom instance creation. Note that default implementation relies on `vars(self)` for dumping and on `cls(**dct)` for loading.
 
**TODO complete**
```python
from jsoner import json_info, JSONAble

@yaml_info(yaml_tag_ns='com.yamlable.example')
class Foo(YamlAble):

    def __init__(self, a, b):
        """ Constructor """
        self.a = a
        self.b = b
        self.irrelevant = 37

    def __str__(self):
        """ String representation for prints """
        return "Foo - " + str(dict(a=self.a, b=self.b))
    
    def __to_yaml_dict__(self):
        """ This optional method is called when you call yaml.dump()"""
        return {'a': self.a, 'b': self.b}

    @classmethod
    def __from_yaml_dict__(cls, dct, yaml_tag):
        """ This optional method is called when you call yaml.load()"""
        return Foo(dct['a'], dct['b'])
```

That's it! Let's check that our class is correct and allows us to create instances:

```python
>>> f = Foo(1, 'hello')
>>> print(f)

Foo - {'a': 1, 'b': 'hello'}
```

Now let's dump and load it using `pyyaml`:

```python
>>> import yaml
>>> print(yaml.dump(f))

!yamlable/com.yamlable.example.Foo {a: 1, b: hello}
```

```python
>>> print(yaml.safe_load("!yamlable/com.yamlable.example.Foo {a: 0, b: hey}"))

Foo - {'a': 0, 'b': 'hey'}
```

For more general cases where your object is embedded in a more complex structure for example, it will work as expected:

```python
>>> d = {'foo': f, 'foo2': 12}
>>> print(yaml.safe_dump(d))

foo: !yamlable/com.yamlable.example.Foo {a: 1, b: hello}
foo2: 12
```


In addition, the object directly offers the `dump_yaml` (dumping to file) / `dumps_yaml` (dumping to string) convenience methods, and the class directly offers the `load_yaml` (load from file) / `loads_yaml` (load from string) convenience methods.

See [PyYaml documentation](http://pyyaml.org/wiki/PyYAMLDocumentation) for the various formatting arguments that you can use, they are the same than in the `yaml.dump` method. For example:

```python
>>> print(f.dumps_yaml(default_flow_style=False))

!yamlable/com.yamlable.example.Foo
a: 1
b: hello
```

### Plugins

Plugins for many types are available here: [https://github.com/python-jsoner](https://github.com/python-jsoner)

**END TODO**

See [Usage](./usage) for other possibilities of `jsoner`.

## Main features / benefits

 * Add json-ability to any class easily through inheritance without metaclass and without knowledge of internal `JSONEncoder`/`JSONDecoder` logic (hooks, etc.).
 * Write codecs to support several types at a time with `JSONCodec`. Distribute them and maintain them in separate repositories such as in [https://github.com/python-jsoner](https://github.com/python-jsoner).


## See Also

[Python json documentation](https://docs.python.org/3/library/json.html)

### Others

*Do you like this library ? You might also like [my other python libraries](https://github.com/smarie/OVERVIEW#python)* 

## Want to contribute ?

Details on the github page: [https://github.com/python-jsoner/jsoner](https://github.com/python-jsoner/jsoner)
