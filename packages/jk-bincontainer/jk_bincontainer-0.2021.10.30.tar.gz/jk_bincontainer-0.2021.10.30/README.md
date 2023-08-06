jk_bincontainer
==========

Introduction
------------

This python module implements a container for data blocks.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/....)
* [pypi.python.org](https://pypi.python.org/pypi/jk_bincontainer)

Why this module?
----------------

Sometimes it is more convenient to store a single file instead of multiple ones. For purposes of reuse of such kind of functionality this module has been created. It implements a container that allows adding binary data blocks, store the whole set ob blocks in a single file, and load everything again later.

This module is heavily inspired by the internal structure of PNG files.

Limitations of this module
--------------------------

Every data block must have a unique key so that it can be identified within the container. This key must consist of exactly 4 ASCII characters.

All data handling is done in memory. Therefore it is recommended to not use this container for huge amounts of data. (This container is not intended to meet such requirements.)

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_bincontainer
```

### Create a data container

To create an empty container simply construct it:

```python
bc = BinContainer()
```

The container is now ready for use.

### Add a data block

You can add binary data blocks like this:

```python
bc.addBinaryBlock("abcd", b"\x01\x02\x03")
```

This data block will be added as a binary data block. In the current implementation there are only binary data blocks. In the future more blocks of different kind might be supported.
Please note that because of this reason a data block is associated with a type identifier internally that is used implicitely if `addBinaryBlock()` (or other methods in the future)
are called.

### Retrieve the block again

Of course, you can find the block again later:

```python
blockType, rawData = bc.getBlockByKeyE("abcd")
```

As stated above data blocks are associated with a type identifier. For now only binary data blocks are supported, therefore `blockType` will always receive "`bin`" currently.

All named data retrieval methods return such a tuple. If you retrieve by index you will receive a triple:

```python
blockKey, blockType, rawData = bc.getBlockByIndexE(0)
```

Again `blockType` will contain "`bin`" as right now only binary data blocks are supported.

In general the following methods are available:

| Method				| Argument(s)	| Return Value(s)								|
| ---					| ---			| ---											|
| `getBlockByIndexE`	| `int index`	| `str blockKey`, `str blockType`, `data`		|
| `getBlockByIndex`		| `int index`	| `str blockKey`, `str blockType`, `data`		|
| `getBlockByKeyE`		| `str key`		| `str blockType`, `data`						|
| `getBlockByKey`		| `str key`		| `str blockType`, `data`						|

### Serialize the data container

The data container can be serialized like this:

```python
rawBytes = bytes(bc)
```

Or:

```python
rawBytes = bc.toBytes()
```

Both approaches will construct a `bytes` object with data currently stored in the container.

Additionally you could construct a `bytearray` object if you are interested in `bytearray` instead of `bytes`:

```python
rawByteArray = bc.toByteArray()
```

### Write the data container to disk

The data container can be serialized and written to disk. Example:

```python
bc.writeToFile("/path/to/myfile")
```

### Loading the data from disk

If you have written the data to disk you can load them again. Example:

```python
bc.loadFromFile("/path/to/myfile")
```

### Deserialize data

Alternatively you might already have binary data and want to load directly from it. Example:

```python
bc.loadFromData(binData)
```

Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



