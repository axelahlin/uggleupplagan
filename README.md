# edan70-project

## Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## About


## Getting Started
### Prerequisites

```sh
# requirements.txt
datasets==2.14.5
matplotlib==3.8.0
numpy==1.24.2
pandas==2.1.1
plotly==5.17.0
Requests==2.31.0
scikit_learn==1.3.1
sentence_transformers==2.2.2
SPARQLWrapper==2.0.0
torch==2.1.0
transformers==4.34.0

```

### Installation
Install the dependencies like this:
```sh
$ pip install -r requirements.txt
```



### Usage
The preferred way to run the program is through the main ```run.py``` with appropriate options flags, as demonstrated below. 
```sh
$ python run.py [OPTION]
```
Options:
```
usage: run.py [-h] [-s] [-q] [-c] [-e] [-m]

options:
  -h, --help  show this help message and exit
  -s          Scraping
  -a          Annotating by Wikidata querying
  -c          Running the classifier
  -e          Evaluating the classifier
  -m          Generating a map visualization
```


## Contributing


## License
CC BY-NC-SA
## Acknowledgments
