# RE-Lab_template
Template repository for Python projects

## Get started

Simply click on the green `Use this template` button on the left of the `Clone or download` button.

The detailed instructions to create a new repository from this template can be found [here](https://help.github.com/en/articles/creating-a-repository-from-a-template).

## To Do

These steps should be taken after creating a project from this template:

1. Choose a license
	Open the LICENSE file and and fill in the year and name. If you don't want to use the MIT license you can find other licenses at [choosealicense.com](https://choosealicense.com/).

2. Edit setup.py
	Fill in the right name and add a short description. Please read the comments above the corresponding variables.

## Distributing initial version via PyPI (pip)

A more in-depth tutorial can be found on the [official documentation](https://packaging.python.org/tutorials/packaging-projects/).

Everytime you upload a new version to PyPi you have to increase the version number in the setup.py file beforehand!

1. If you want to share the project with users you might want them to be able to easily install the software. Here are the necessary steps:
	The pip installation will automatically add all python-files and all files specified in package_data and data_files in setup() arguments in the setup.py, as well
	as the README and pyproject.toml. If you need to include other files create a new file 'MANIFEST.in' in the project root folder and refer to the [official guidelines](https://packaging.python.org/guides/using-manifest-in/#using-manifest-in)
	on how to add these files.

2. Make sure you have the latest version of PyPA's build installed:
	(Linux)		python3 -m pip install --upgrade build
	(Windows)	py -m pip install --upgrade build

3. From the project root directory run:
	(Linux)		python3 -m build
	(Windows)	py -m build

	There should now be a 'dist' directory with two files in it.

4. Install Twine
	(Linux)		python3 -m pip install --upgrade twine
	(Windows)	py -m pip install --upgrade twine	

5. Upload (you still need to be in the project root folder)
	(Linux)		python3 -m twine upload dist/*
	(Windows)	py -m twine upload dist/*
	Enter the credentials. There is a RE-Lab account for PyPI.

Done. You can now install the package
	pip install package-name


## src folder

This folder is where you should place the code of your package (package name to be edited in 'setup.py' under name)

You can install it locally for developing with

    python setup.py install
    
More details for packaging are available on [https://packaging.python.org](https://packaging.python.org/tutorials/packaging-projects/)


## Docs

To build the docs simply go to the `docs` folder

    cd docs

Install the requirements

    pip install -r docs_requirements.txt

and run

 (Linux)	make html
 (Windows)	make.bat html

The output will then be located in `docs/_build/html` and can be opened with your favorite browser

## Code linting

In this template, 3 possible linters are proposed:
- flake8 only sends warnings and error about linting (PEP8)
- pylint sends warnings and error about linting (PEP8) and also allows warning about imports order
- black sends warning but can also fix the files for you

You can perfectly use the 3 of them or subset, at your preference. Don't forget to edit `.travis.yml` if you want to deactivate the automatic testing of some linters!