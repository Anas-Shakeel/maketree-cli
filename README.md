# Maketree CLI

[![GitHub Repository](https://img.shields.io/badge/-GitHub-%230D0D0D?logo=github&labelColor=gray)](https://github.com/anas-shakeel/maketree-cli) 
[![Latest PyPi version](https://img.shields.io/pypi/v/maketree.svg)](https://pypi.python.org/pypi/maketree)
[![supported Python versions](https://img.shields.io/pypi/pyversions/maketree)](https://pypi.python.org/pypi/maketree)
[![Project licence](https://img.shields.io/pypi/l/maketree?color=blue)](LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](black)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/maketree?color=%232ecc71)](https://pypistats.org/packages/maketree)


A Command-line Application to create directory structures from a structure file. It let's you create the most complex directory structures in a blink or two.


## Features:
- Zero dependencies
- Easy to write structure syntax
- User friendly.
  

## Installation:

`maketree` can easily be installed using `pip`.

```shell
pip install maketree
```

`python>=3.8` must be installed on your system.



## Basic Usage:

Once `maketree` is installed, you can run it from any location in your terminal.

```shell
>> maketree -h
usage: maketree [OPTIONS]

A CLI tool to create directory structures from a structure file.

positional arguments:
  src              source file (with .tree extension)
  dst              where to create the tree structure (default: .)

options:
  -h, --help       show this help message and exit
  -g, --graphical  show source file as graphical tree and exit
  -o, --overwrite  overwrite existing files
  -s, --skip       skip existing files
  -v, --verbose    increase verbosity

Maketree 1.0.0
```

There is only one required argument that you need to provide, and that is `src`, a source file that defines the tree structure to create.

`maketree` parses the tree structure defined in a `.tree` file and then creates the directories and/or files on the filesystem. Let's create this structure file and name it `myapp.tree`.

```
src/
    index.css
    index.js
```

We want maketree to create a folder called `src` and two files in that folder namely `index.css` and `index.js`. Notice i've used `4` space indentation for nesting and a forward slash to mark `src` as a directory and not a file.

Defining a directory structure is fairly easy. You just write the names of folders and files you want to create, nest them as per you needs and that's it.

**There are only three rules you must follow:**

1. Directories must end with a forward slash `/`

2. Indentation must always be of `4` spaces *(it tolerates other indentations but may produce unexpected results)*

3. And directory or file names must be valid according to your OS.
   
   

Let's add more files and folders in `myapp.tree` file.

```
node_modules/
public/
    favicon.ico
    index.html
    robots.txt
src/
    index.css
    index.js
.gitignore
package.json
README.md
```

Let's now create the structure on our filesystem:

```shell
>> maketree myapp.tree
3 directories and 8 files have been created.
```

`maketree` creates the structure in current directory by default. You can also provide a destination location to create the structure in that location.



Let's create a folder in our current directory called `myapp`.

```shell
>> mkdir myapp
```

And now let's create the structure again, but this time inside `myapp` folder.

```shell
>> maketree myapp.tree myapp
3 directories and 8 files have been created.
```

It created the structure in `myapp` folder.



But what if we run it again? without deleting the structure in `myapp` folder? Let's see.

```shell
>> maketree myapp.tree myapp
Warning: File 'app\public\favicon.ico' already exists
Warning: File 'app\public\index.html' already exists
Warning: File 'app\public\robots.txt' already exists
Warning: File 'app\src\index.css' already exists
Warning: File 'app\src\index.js' already exists
Warning: File 'app\.gitignore' already exists
Warning: File 'app\package.json' already exists
Warning: File 'app\README.md' already exists

Fix 8 issues before moving forward.
```

`maketree` won't overwrite existing files by default. It warns you which files already exist and quits.

But if you don't want to delete the files yourself or you just want `maketree` to overwrite them, You can give `-o` or `--overwrite` to overwrite existing files.

```shell
>> maketree myapp.tree myapp --overwrite
0 directories and 8 files have been created.
```

It overwrites existing files as expected.



There's also a `-s` or `-skip` flag that skips existing files and create non-existing ones.

Let's first delete all files in public folder.

```shell
>> rm myapp/public/*
```

Now let's re-run the maketree command *(but this time, with `--skip` flag)*.

```shell
>> maketree myapp.tree myapp --skip
0 directories and 3 files have been created.
```

It skipped all files that already existed and created the ones that didn't.



You can also see a graphical representation of the tree structure in `.tree` file with `'-g` or `--graphical` command.

```shell
>> maketree myapp.tree -g
.
├─── node_modules
├─── public
│   ├─── favicon.ico
│   ├─── index.html
│   └─── robots.txt
├─── src
│   ├─── index.css
│   └─── index.js
├─── .gitignore
├─── package.json
└─── README.md
```

It makes it easy to see visualize the structure `maketree` will create on your filesystem.

The structure file can be as simple or complex as you want. There's no limit *(well unless the OS you're using doesn't have any)*.



### Note:

_`maketree` is still in it's alpha phase, so you may encounter some bugs. Please report if you do._ 
