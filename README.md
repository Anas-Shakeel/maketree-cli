<p align="center">
  <img src="https://raw.githubusercontent.com/Anas-Shakeel/maketree-cli/main/assets/header.jpg" />
</p>

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
-   **Color support**
-   **Simple and easy to write structure syntax**
-   **Lightweight, fast, and has zero dependencies**
-   **Simple and user-friendly CLI**

## 🛠️ Installation:

### Install via **pip**:

`Maketree` is available on PyPI. **(Recommended if you're a python developer and have python already installed on your system)**

You can install it using:

```sh
pip install maketree
```

`python>=3.8` must be installed on your system.

### Install from **Source**:

If you are installing from source, you will need `python>=3.8`.

```sh
git clone https://github.com/Anas-Shakeel/maketree-cli.git
cd maketree-cli
pip install .
```

### Download **Standalone Executable**: _(No Python Required)_

Maketree provides standalone binaries for **Linux**, **macOS**, and **Windows**. **(Recommended if you don't want to install Python.)**

-   Download the latest release from the [Releases page](https://github.com/anas-shakeel/maketree-cli/releases/).

-   **(Optional)** Move the executable to a directory in your system's `PATH` (e.g., `/usr/local/bin` on **Linux/macOS** OR `C:\maketree` on **Windows**).

-   Run `maketree` from the terminal.

    ```sh
    maketree -h
    ```

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

This will instantly generate the entire structure in your current directory.

## 📖 Usage

You can `maketree` from any location in your terminal. **(If installed via `pip` or if moved the executable to a directory recognized by system's `PATH`)**

### 🔹 Display Help

```sh
maketree -h
```

This will show the available commands and options:

```sh
usage: maketree [OPTIONS]

Create complex project structures effortlessly.

positional arguments:
  src                source file (with .tree extension)
  dst                where to create the tree structure (default: .)

options:
  -h, --help         show this help message and exit
  -cd, --create-dst  create destination folder if it doesn't exist.
  -g, --graphical    show source file as graphical tree and exit
  -o, --overwrite    overwrite existing files
  -s, --skip         skip existing files
  -nc, --no-color    don't use colors in output
  -nC, --no-confirm  don't ask for confirmation
  -v, --verbose      enable verbose mode

Maketree 1.1.0
```

### 🔹 Creating a Directory Structure

**Maketree** reads `.tree` file that defines the folder and file structure and then creates the corresponding structure on your filesystem.

#### 1️⃣ Define the Structure

Create a file named `myapp.tree`:

```
src/
    style.css
    app.js
    index.html
```

This will create a src folder with three files: `index.html`, `style.css`, and `app.js`.

#### 2️⃣ Generate the Structure

To generate the structure, Run:

```sh
maketree myapp.tree
```

It will ask for confirmation with a graphical representation of the structure.

```sh
.
└─── src/
│   ├─── app.js
│   ├─── index.html
│   └─── style.css
Create this structure? (y/N):
```

Output:

```sh
1 directory and 3 files have been created.
```

By default, maketree creates the structure in the current directory.

### 🔹 Rules for Writing a `.tree` File

To ensure correctness, follow these three rules:

1. **Directories must end with `/`**
2. **Indentation must be exactly 4 spaces (other indentations may cause unexpected results)**
3. **File and folder names must be valid according to your OS**

#### Example: (Not so) Complex Structure

`myapp.tree`

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

Now, run:

```sh
maketree myapp.tree
```

Output: (After confirming)

```
3 directories and 8 files have been created.
```

### 🔹 Specifying a Destination Folder

You can specify a destination folder instead of creating the structure in the current directory.

```sh
maketree myapp.tree myapp/
```

It will throw an error if `myapp/` does not exist.

```sh
Error: destination path 'myapp' does not exist.
```

Use `--create-dst` or `-cd` flag, `maketree` then creates the destination directory if it doesn't exists.

```sh
maketree myapp.tree myapp/ --create-dst
```

Output:

```
3 directories and 8 files have been created.
```

### 🔹 Handling Existing Files

If you run `maketree` again in the same directory without deleting files, you’ll see an error:

```sh
maketree myapp.tree myapp
```

Output:

```
Error: Found 8 existing files, cannot proceed. (try --skip or --overwrite)
```

By default, `maketree` does not **overwrite** or **skip** existing files.

#### 1️⃣ Overwrite Existing Files

Use the `--overwrite` or `-o` flag to overwrite existing files:

```sh
maketree myapp.tree myapp --overwrite
```

Output:

```
0 directories and 8 files have been created.
```

#### 2️⃣ Skip Existing Files

Use the `--skip` or `-s` flag to keep existing files but create missing ones:

```sh
maketree myapp.tree myapp --skip
```

Output: (After deleting 3 files)

```
0 directories and 3 files have been created.
```

### 🔹 Preview the Structure

Use `--graphical` or `-g` to visualize the `myapp.tree` file:

```sh
maketree myapp.tree -g
```

Output:

```
.
├─── node_modules/
├─── public/
│   ├─── favicon.ico
│   ├─── index.html
│   └─── robots.txt
├─── src/
│   ├─── index.css
│   └─── index.js
├─── .gitignore
├─── package.json
└─── README.md
```

It is also shown before you create a structure for confirmation.

### 🔹 Avoid Confirming:

By default, `maketree` confirms before creating the structure. But this can sometimes be anoyying. Use `--no-confirm` or `-nC` flag to create the structure without confirming. _(Notice the C is capital in `-nC`)_

```sh
maketree myapp.tree myapp --no-confirm
```

### 🔹 Avoid Color Output:

By default, `maketree` uses [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code) to color the output.

```sh
maketree myapp.tree myapp/
```

If you're seeing something like this:

```sh
←[1m←[3m←[92msrc/←[0m
←[90m├───←[0m ←[1m←[3m←[92mnode_modules/←[0m
←[90m├───←[0m ←[1m←[3m←[92mpublic/←[0m
←[90m│   ←[0m←[90m├───←[0m favicon.ico
←[90m│   ←[0m←[90m├───←[0m index.html
←[90m│   ←[0m←[90m└───←[0m robots.txt
←[90m├───←[0m ←[1m←[3m←[92msrc/←[0m
←[90m│   ←[0m←[90m├───←[0m index.css
←[90m│   ←[0m←[90m└───←[0m index.js
←[90m├───←[0m .gitignore
←[90m├───←[0m package.json
←[90m└───←[0m README.md
←[95mCreate this structure? (y/N): ←[0m
```

Then your terminal doesn't support **ANSI escape codes** by default. **(there are workarounds but they require extra python dependencies)**.

You will have to disable colors using `--no-color` or `-nc` flag.

```sh-session
maketree myapp.tree myapp/ --no-color
```

This will disable colors and you'll see normal text again.

### 🚀 Summary

| Feature           | Command Example                 |
| ----------------- | ------------------------------- |
| Create structure  | `maketree myapp.tree`           |
| Set destination   | `maketree myapp.tree myapp -cd` |
| Overwrite files   | `maketree myapp.tree myapp -o`  |
| Skip existing     | `maketree myapp.tree myapp -s`  |
| Graphical preview | `maketree myapp.tree -g`        |
| Avoid Confirm     | `maketree myapp.tree myapp -nC` |
| Avoid Colors      | `maketree myapp.tree myapp -nc` |

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

**Maketree** is a command-line tool that helps developers quickly generate a predefined folder and file structures for your projects. It eliminates the need to manually create directories and files, allowing developers to start coding right away with a well-organized project structure.

#### ❓ Do I have to be a Software Developer to use Maketree?

No, you can be anyone. You can be a lawyer, student, or heck even Yavascript programmer.

#### ❓ Why should I use Maketree?

If you frequently create CLI applications, Maketree saves you time by setting up a standardized project structure instantly. It follows best practices and helps you maintain consistency across different projects.

#### ❓ How do I install Maketree?

You can install **Maketree** via pip. _(for python developers)_

```sh
pip install maketree
```

Or download the executable for your OS from [Releases page](https://github.com/anas-shakeel/maketree-cli/releases/).

#### ❓ How do I use Maketree to generate a project structure?

Simply create a file like `anything.tree` and define your project structure in it:

`anything.tree`

```
src/
    app.js
    index.html
    style.css
```

then run the following command:

```sh
maketree anything.tree
```

This will create the files and folders you specified in `anything.tree` file.

#### ❓ What should I do if I find a bug?

If you encounter a bug, please [open an issue](https://github.com/Anas-Shakeel/maketree-cli/issues) on GitHub with details about the problem. Be sure to include:

-   A description of the issue
-   Steps to reproduce
-   Expected vs. actual behavior
-   Any error messages you received

#### ❓ How do I uninstall Maketree?

To uninstall **Maketree** (installed via `pip`), Run:

```sh
pip uninstall maketree
```

## Contributing

Contributions to **Maketree** are welcome and highly appreciated. However, before you jump right into it, i would like you to review [Contribution Guidelines](https://github.com/anas-shakeel/maketree-cli/blob/main/CONTRIBUTING.md) to make sure you have a smooth experience contributing to **Maketree**.
