This is a important file... 

Consultar para escrever esse arquivo:
https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

You can install your pyproject.toml with the command in venv enviroment:
$ pip install -e .

The . refers to the current directory where pyproject.toml resides, 
and -e flag installs it in editable mode.

If you install your project with pip, the Rich library will automatically
be installed as part of the regular installation. Nice! If you want to 
install the optional dependencies too, then you can call:
$ python -m pip install -e ".[dev]"

Appending [dev] to the directory with the pyproject.toml file will 
include the optional dependencies you’ve specified under dev, along 
with the core dependencies specified in the [project] table. Very nice!
For example:
...

[project]
name = "snakesay"
version = "1.0.0"
+dependencies = ["rich>=13.9.0"]

[project.optional-dependencies]
+dev = ["black>=24.1.0", "isort>=5.13.0"]

...

