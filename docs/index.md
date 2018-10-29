<div class="badges">
    <a href="http://travis-ci.org/Naeka/wagtailmodelchooser">
        <img src="https://travis-ci.org/Naeka/wagtailmodelchooser.svg?branch=master">
    </a>
    <a href="https://pypi.python.org/pypi/wagtailmodelchooser">
        <img src="https://img.shields.io/pypi/v/wagtailmodelchooser.svg">
    </a>
</div>

---

## Overview

Wagtail chooser panel generator for generic Django models.

It elegantly completes `wagtail.contrib.modeladmin` and allows a simple selection of
any model instance anywhere in the Wagtail admin.

## Requirements

* Python (3.4, 3.5, 3.6)
* Django (1.11, 2.0, 2.1)
* Wagtail (2.2, 2.3)

## Installation

Install using `pip`...

```bash
$ pip install wagtailmodelchooser
```

## Example

The most simple usecase, without any customization.

```python
from wagtailmodelchooser.edit_handlers import register_chooser_for_model

ItemChooserPanel = register_chooser_for_model(Item)
```

Advanced examples, customizations are available in the usage section.

## Testing

Install testing requirements.

```bash
$ pip install -e ".[testing]"
```

Run with runtests.

```bash
$ ./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
$ pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
$ mkdocs build
```
