# Twitter Lexical Normalisation
COMP90049 Knowledge Technologies, Semester 2 2017 Project 1 Assignment - Lexical Normalisation of Twitter Data

## Overview
This project is a python script that utilized several methods to find a correct form of correct words from a mispelled word in the dictionary.

In this project, the author want to compare token that comes from twitter text (contain some mispelled word) against a list of English words to find a correct form.

The author use three methods for approximate string matching in the script.

* Only use Levenshtein Distance
* Use Levenshtein Distance + Soundex algorithm
* Use Levenshtein Distance + Metaphone algorithm

## Getting Started

Make sure you have python2.7 installed in your system.

### Setup Python and VirtualEnv
VirtualEnv is a way to create isolated Python environments for every project and VirtualEnvWrapper "wraps" the virtualenv API to make it more user friendly.

```bash
$ pip install pip --upgrade
$ pip install virtualenv
$ pip install virtualenvwrapper
```

To complete the virtualenv setup process, put the following in your ~/.bash_profile
```bash
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

### Create VirtualEnv and Install Dependencies
The following commands will ensure you have the Python dependencies installed inside your `virtualenv`.

```bash
mkvirtualenv lexical-twitter --python=python2
pip install -r requirements.txt
```

## Running The Program
### Data Preprocessing
```
usage: main.py [-h] -d DICTIONARY -m METHOD -f FILENAME [-v]

A CLI app to for lexical twitter

optional arguments:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Dictionary path
  -m METHOD, --method METHOD
                        String matching algorithm method [0 - levenshtein, 1 -
                        levenshtein + soundex, 2 - levenshtein + metaphone]
  -f FILENAME, --filename FILENAME
                        Filename for a dump file
  -v, --verbose         increase output verbosity
```

Running the program to get the matching results 

```
$ workon lexical-twitter
$ mkdir output
$ python main.py -m 0 -f output/levenshtein.json -d data/words.txt # run levenshtein only program

$ python main.py -m 1 -f output/levenshtein_soundex.json -d data/words.txt # run levenshtein + soundex program

$ python main.py -m 2 -f output/levenshtein_metaphone.json - d data/words.txt # run levenshtein + metaphone program
```

### Data Analysis
The author use jupyter notebook to do the analysis. We need to firstly run the notebook, and open `Similarity Analysis.ipynp` file from jupyter notebook

```
$ workon lexical-twitter
$ jupyter notebook
```