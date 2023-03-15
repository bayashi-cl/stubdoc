# stubdoc

`stubdoc` is a sphinx extension to read docstrings from stub files.

How to get a docstring from a stub file is discussed in this
[sphinx issue](https://github.com/sphinx-doc/sphinx/issues/7630),
and possible use cases include document generation for the c-extension.

## Stub files

Stub files are explained in detail in the
[mypy documentation](https://mypy.readthedocs.io/en/stable/stubs.html).

The module (currently) assumes that the stub file is in the same
directory as the target file.

## Usage

1. [Setup sphinx](http://sphinx-doc.org/tutorial.html)

2. install `stubdoc`

    ```sh
    pip install git+https://github.com/bayashi-cl/stubdoc
    ```

3. Edit `conf.py`

    ```py
    # Configuration file for the Sphinx documentation builder.
    ...
    extensions = ["stubdoc"]
    ...
    module_names = ["my_module"]
    ...
    ```

    The `module_names` accepts a list of module names, and any module
    **startwith** that name will be the target of the stub file search.

    ```py
    # Find stub files only under submodules.
    module_names = ["my_module.submodule"]
    ```

    ```py
    # Use setuptools.find_packages
    module_names = find_packages("path/to/src")
    ```

4. Build documents.

    ```sh
    sphinx-apidoc ...
    sphinx-build ...
    ```
