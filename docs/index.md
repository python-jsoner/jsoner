# jsabl

*A thin wrapper of Python stdlib's json module to convert objects to JSON and back, with the purpose of maintaining readability of objects serialized with old versions of their class definition.*

[![Build Status](https://travis-ci.org/python-jsabl/jsabl.svg?branch=master)](https://travis-ci.org/python-jsabl/jsabl) [![Tests Status](https://python-jsabl.github.io/jsabl/junit/junit-badge.svg?dummy=8484744)](https://python-jsabl.github.io/jsabl/junit/report.html) [![codecov](https://codecov.io/gh/python-jsabl/jsabl/branch/master/graph/badge.svg)](https://codecov.io/gh/python-jsabl/jsabl) [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://python-jsabl.github.io/jsabl/) [![PyPI](https://img.shields.io/badge/PyPI-jsabl-blue.svg)](https://pypi.python.org/pypi/jsabl/)


## Installing

```bash
> pip install jsabl
```

## Usage

Let's make a class JSON-able: we have to

 - inherit from `JSONAble`
 - decorate it with the `@json_info` annotation to declare the associated json "schema" id and version
 - *optionally* implement `__from_json_dict__` (class method called during decoding) and/or `__to_json_dict__` (instance method called during encoding) if we wish to have control on the process, for example to only dump part of the attributes or perform some custom instance creation. Note that default implementation relies on `vars(self)` for dumping and on `cls(**dct)` for loading.
 
**TODO complete**

See [Usage](./usage) for other possibilities of `jsabl`.


## Main features / benefits

 * Add json-ability to any class easily through inheritance without metaclass and without knowledge of internal `JSONEncoder`/`JSONDecoder` logic (hooks, etc.).
 * Write codecs to support several types at a time with `JSONCodec`


## See Also

[Python json documentation](https://docs.python.org/3/library/json.html)

### Others

*Do you like this library ? You might also like [my other python libraries](https://github.com/smarie/OVERVIEW#python)* 

## Want to contribute ?

Details on the github page: [https://github.com/python-jsabl/jsabl](https://github.com/python-jsabl/jsabl)
