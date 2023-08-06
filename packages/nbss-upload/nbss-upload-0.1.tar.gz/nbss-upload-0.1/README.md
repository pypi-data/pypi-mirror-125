# nbss-upload

Upload notebooks (Jupyter, Rmd, etc) to a [NotebookSharing.space](https://notebooksharing.space)
instance.

## Installation

`nbss-upload` is available on PyPI, and can be installed with `pip`.

```bash
pip install nbss-upload
```

## Usage

Simply call it with the path to the notebook you want to upload.

```bash
$ nbss-upload test.ipynb
https://notebooksharing.space/view/04ab7ab45c2f08628eba9cb8fe5fb9a63f5961d5dfce622b9e26974ddc138916
```

This will upload the notebook and return the URL you can use to share it with others.

By default, only users who you share the URL with can access the notebook - it will
not be visible to search engines. Annotations will also be turned off by default to
help fight abuse.

You can enable annotations via `hypothes.is` by passing `--enable-annotations` or `-a`.
The notebook can be made discoverable to search engines by passing `--enable-discvery`
or `-d`.

All notebook formats supported by notebooksharing.space - `.ipynb`, `.rmd`, `.html`
are supported.