# Run from source

This page details how to run the program from source. If you have no idea what this page is saying, you *probably* shouldn't follow it.

## Setup

In order to build, you'll need the following as prerequisites:

- A working Python installation that supports the code. The version used for developing this program originally was Python 3.11 from the [official Python website](https://python.org).
- Required dependencies installed. They are marked in the `requirements.txt` file for your convenience.
- While not required, it is *highly recommended* to use a virtual environment. You can create one using `python -m venv venv`, then using `venv\scripts\activate`.

## Running the app

Once you have the "App" category of dependencies installed, you can simply run `python script.py`.

## Compiling from source

After installing dependencies in both the "App" and "Compiling" categories, you can run `pyinstaller script.py` to compile.
Some additional arguments you might want to use are:

- `--onefile`: Builds into a singular executable file.
- `--name <name>`: Sets the executable output's name.
- `--windowed`: Prevents CMD from coming up when you launch the executable.

## Building the documentation site

You only need to install the dependencies listed in the "Documentation" category.
After that, you can simply run `mkdocs build`, which will output a `site/` folder that contains the fully built site.

Do NOT attempt to run `mkdocs gh-deploy`, as it will create a new branch and (attempt to) push it to the remote.
