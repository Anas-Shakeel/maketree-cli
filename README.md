# Maketree CLI

[![GitHub Repository](https://img.shields.io/badge/-GitHub-%230D0D0D?logo=github&labelColor=gray)](https://github.com/anas-shakeel/maketree-cli)
[![Latest PyPi version](https://img.shields.io/pypi/v/maketree.svg)](https://pypi.python.org/pypi/maketree)
[![supported Python versions](https://img.shields.io/pypi/pyversions/maketree)](https://pypi.python.org/pypi/maketree)
[![Project licence](https://img.shields.io/pypi/l/maketree?color=blue)](LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](black)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/maketree?color=%232ecc71)](https://pypistats.org/packages/maketree)

Create project structures effortlessly with a single command.

## 📜 Overview

Maketree is a powerful CLI tool that generates **directories** and **files** based on a predefined structure. Instead of manually creating folders and files, just define your structure and let **Maketree** handle the rest.

## 💡 Why Maketree?

-   **Saves Time**: No more manually creating directories and files.
-   **Consistency**: Maintain a standard project structure across all your projects.
-   **Easy to Use**: Define a structure in plain text and generate it instantly.

## 🧐 Features:

-   **Supports nested directory structures**
-   **Automatically creates missing parent directories**
-   **Flexible file handling with warning, skip, and overwrite options**
-   **Preview the directory tree before creation**
-   **Simple and easy to write structure syntax**
-   **Lightweight, fast, and has zero dependencies**
-   **Simple and user-friendly CLI**

## 🛠️ Installation:

`maketree` can easily be installed using `pip`.

```shell
pip install maketree
```

`python>=3.8` must be installed on your system.

## ⚡ Quickstart:

Define your project structure in a `.tree` file:

`structure.tree`

```plaintext
my_project/
    src/
        main.py
        utils.py
    tests/
        test_main.py
    README.md
    .gitignore
```

Then, run:

```sh
maketree structure.tree
```

This will instantly generate the entire structure in the current directory, on your machine.

## 📖 Usage

You can `maketree` from any location in your terminal.

### 🔹 Display Help

```sh
maketree -h
```

This will show the available commands and options:

```sh
usage: maketree [OPTIONS]

A CLI tool to create directory structures from a structure file.

positional arguments:
  src              source file (with .tree extension)
  dst              destination folder (default: .)

options:
  -h, --help         show this help message and exit
  -cd, --create-dst  create destination folder if it does not exist
  -g, --graphical    display source file as graphical tree and exit
  -o, --overwrite    overwrite existing files
  -s, --skip         skip existing files
  -v, --verbose      increase verbosity

Maketree 1.0.1
```

### 🔹 Creating a Directory Structure

**Maketree** reads a `.tree` file that defines the folder and file hierarchy and then creates the corresponding structure on your filesystem.

#### 1️⃣ Define the Structure

Create a file named `myapp.tree`:

```sh
src/
    index.css
    index.js
```

This will create a src folder with two files: `index.css` and `index.js`.

#### 2️⃣ Generate the Structure

Run:

```sh
maketree myapp.tree
```

Output:

```
1 directory and 2 files have been created.
```

By default, maketree creates the structure in the current directory.

### 🔹 Rules for Writing a `.tree` File

To ensure correctness, follow these three rules:

1. **Directories must end with `/`**
2. **Indentation must be exactly 4 spaces (other indentations may cause unexpected results)**
3. **File and folder names must be valid according to your OS**

#### Example: Complex Structure

```sh
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

Now, run:

```sh
maketree myapp.tree
```

Output:

```
3 directories and 8 files have been created.
```

### 🔹 Specifying a Destination Folder

You can specify a destination folder instead of creating the structure in the current directory.

#### Example: Create a folder myapp and generate the structure inside it

```sh
maketree myapp.tree myapp --create-dst
```

Output:

```
3 directories and 8 files have been created.
```

### 🔹 Handling Existing Files

If you run `maketree` again in the same directory without deleting files, you’ll see warnings:

```sh
maketree myapp.tree myapp
```

Output:

```
Warning: File 'myapp/public/favicon.ico' already exists
Warning: File 'myapp/public/index.html' already exists
...
Fix 8 issues before moving forward.
```

By default, `maketree` does not overwrite existing files.

#### 1️⃣ Overwrite Existing Files

Use the `-o` or `--overwrite` flag to replace files:

```sh
maketree myapp.tree myapp --overwrite
```

Output:

```
0 directories and 8 files have been created.
```

#### 2️⃣ Skip Existing Files

Use the `-s` or `--skip` flag to keep existing files but create missing ones:

```sh
maketree myapp.tree myapp --skip
```

Output:

```
0 directories and 3 files have been created.
```

### 🔹 Viewing the Structure Graphically

Use `-g` or `--graphical` to visualize the `.tree` file before running `maketree`:

```sh
maketree myapp.tree -g
```

Output:

```
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

This helps you preview the structure before applying changes to your filesystem.

### 🚀 Summary

| Feature           | Command Example                 |
| ----------------- | ------------------------------- |
| Create structure  | `maketree myapp.tree`           |
| Set destination   | `maketree myapp.tree myapp -cd` |
| Overwrite files   | `maketree myapp.tree myapp -o`  |
| Skip existing     | `maketree myapp.tree myapp -s`  |
| Graphical preview | `maketree myapp.tree -g`        |

## 🔗 Compatibility

Maketree is compatible with the following operating systems and Python versions:

| OS      | Compatibility |
| ------- | ------------- |
| Linux   | ✅ Supported  |
| macOS   | ✅ Supported  |
| Windows | ✅ Supported  |

### 🐍 Python Version Support

Maketree works with **Python 3.8 and later**, ensuring compatibility with the latest Python releases.

| Python Version | Compatibility         |
| -------------- | --------------------- |
| 3.8            | ✅ Supported          |
| 3.9            | ✅ Supported          |
| 3.10           | ✅ Supported          |
| 3.11           | ✅ Supported          |
| 3.12           | ✅ Supported          |
| 3.13           | ✅ Supported (Latest) |

## ❓ FAQ

#### ❓ What is Maketree?

Maketree is a command-line tool that helps developers quickly generate a predefined folder and file structure for Python-based CLI applications. It eliminates the need to manually create directories and files, allowing developers to start coding right away with a well-organized project structure.

#### ❓ Why should I use Maketree?

If you frequently create CLI applications, Maketree saves you time by setting up a standardized project structure instantly. It follows best practices and helps you maintain consistency across different projects.

#### ❓ How do I install Maketree?

You can install Maketree via pip:

```sh
pip install maketree
```

After installation, you can use the `maketree` command in your terminal.

#### ❓ How do I use Maketree to generate a project structure?

Simply create a file like `filename.tree` and define your project structure in it, then run the following command:

```sh
maketree filename.tree
```

This will create the files and folders you specified in `filename.tree` file.

#### ❓ What should I do if I find a bug?

If you encounter a bug, please [open an issue](https://github.com/Anas-Shakeel/maketree-cli/issues) on GitHub with details about the problem. Be sure to include:

-   A description of the issue
-   Steps to reproduce
-   Expected vs. actual behavior
-   Any error messages you received

#### ❓ How can I uninstall Maketree?

To remove Maketree from your system, run:

```sh
pip uninstall maketree
```

## Contributing

Contributions to **Maketree** are welcome and highly appreciated. However, before you jump right into it, i would like you to review [Contribution Guidelines](https://github.com/anas-shakeel/maketree-cli/blob/main/CONTRIBUTING.md) to make sure you have a smooth experience contributing to **Maketree**.

## ❕ Note:

_`maketree` is in it's beta phase, so you may encounter some bugs. Please report if you do._
