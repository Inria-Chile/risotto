# 🍚 RISOTTO
> Research Intelligent Support and Organization TOol against COVID-19 


![Python 3.x](https://img.shields.io/badge/python-3.x-green.svg)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Inria-Chile/risotto)
[![License: CeCILL-B](https://img.shields.io/badge/license-CeCILL--B-orange)](https://cecill.info/licences.en.html)
[![Fighting against COVID-19](https://img.shields.io/badge/fighting-%F0%9F%A6%A0COVID--19-9cf)]()

# About RISOTTO

[COVID-19](https://en.wikipedia.org/wiki/Coronavirus_disease_2019) research effort is generating a massive amount of information. Traditional human-annotated, ontology-based or supervised (tag-based) learning NLP methods are not able to handle the task of supporting research and understanding results adequately.

So far, to the best of our knowledge, there is not a research support tool that exploits the current state of the art of unsupervised learning in NLP that could be used to provide a quick response to this problem.

RISOTTO is a research support tool that applies state of the art unsupervised NLP and ML methods to:
- analyze COVID-19-related research papers freely available online,
- automatically detect hierarchical groups of these papers and topics,
- present leading "popular" papers as well as potential breakthroughs and new results, and
- provide a visualization tool to understand how is the progress doing what areas are receiving more attention in time, etc.

At the moment, use as input the research papers that have been consolidated as the [CORD-19 dataset](https://www.semanticscholar.org/cord19) by the [Allen Institute for AI](https://allenai.org) and collaborating institutions. [1]

**Note:** It is expected that, as we progress on the conception and development of this tool new tasks/tools will be added to this list.

### References

1. Wang, L.L., Lo, K., Chandrasekhar, Y., Reas, R., Yang, J., Eide, D., Funk, K., Kinney, R.M., Liu, Z., Merrill, W., Mooney, P., Murdick, D.A., Rishi, D., Sheehan, J., Shen, Z., Stilson, B., Wade, A.D., Wang, K., Wilhelm, C., Xie, B., Raymond, D.M., Weld, D.S., Etzioni, O., & Kohlmeier, S. (2020). CORD-19: The Covid-19 Open Research Dataset. *ArXiv, [abs/2004.10706.](https://arxiv.org/pdf/2004.10706.pdf)*

# How to use

## Prerequisites

In order to use RISOTTO you will need a [Kaggle](https://www.kaggle.com) username and key.

### Get a Kaggle API key

If you do not have a Kaggle api key, you may follow the instructions here: https://www.kaggle.com/docs/api. You can set your API key by either:

- Copying the `kaggle.json` file in your local system, in `~/.kaggle/kaggle.json` for Linux/Mac or `C:\Users<Windows-username>.kaggle\kaggle.json` for Windows.
- Setting the `KAGGLE_USERNAME` and `KAGGLE_KEY` environment variables by one of the following options:

```bash
# Temporarily (you will need to do this everytime you open a new terminal):
export $KAGGLE_USERNAME=<your_username>
export $KAGGLE_KEY=<your_key>
```

```bash
# For bash
echo 'export KAGGLE_USERNAME=<your_username>' >> ~/.bash_profile
echo 'export KAGGLE_KEY=<your_key>' >> ~/.bash_profile
```

```bash
# For zsh
echo 'export KAGGLE_USERNAME=<your_username>' >> ~/.zshenv
echo 'export KAGGLE_KEY=<your_key>' >> ~/.zshenv
```

- Setting the `KAGGLE_USERNAME` and `KAGGLE_KEY` environment variables in a `.env` file (for Docker use only!)

```bash
touch .env
echo 'KAGGLE_USERNAME=<your_username>' >> .env
echo 'KAGGLE_KEY=<your_key>' >> .env
```

### Clone or download the repository

```bash
git clone git@github.com:Inria-Chile/risotto.git
cd risotto
```

## How to use RISOTTO locally (without docker)

### Build virtual environment with python3 and install requirements

```bash
python -m virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the build and preprocess scripts

The build script converts the jupyter notebooks to python scripts. The `preprocess.py` script downloads the dataset and builds the artifacts if it is necessary, the `-f` flag forces to re-download and re-build.

```bash
source venv/bin/activate # If you have not sourced the virtual environment already
python scripts/build.py
python scripts/preprocess.py -f # Use the -f flag to override dataset and artifact ts if they exist
```

### Run the GUI

The GUI will be available at localhost:8000

```bash
source venv/bin/activate # If you have not sourced the virtual environment already
voila --port=8000 --no-browser --enable_nbextensions=True 06_GUI.ipynb
```

## How to use Risotto with docker

We provide 2 sets of docker files to serve 2 different purposes: development and production

### Docker for development

This option mounts the whole repository inside the docker container, in order to facilitate using changes in the code

```bash
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up -d

# To restart the container:
docker-compose -f docker-compose-dev.yml restart risotto
docker-compose -f docker-compose-dev.yml up -d

# To force update the dataset and artifacts:
docker-compose -f docker-compose-dev.yml exec risotto python scripts/preprocess.py -f

# To stop the container:
docker-compose -f docker-compose-dev.yml down -v
```

### Docker for production

This option only mounts the dataset and artifacts folders, in order to keep them out of the container

```bash
docker-compose build
docker-compose up -d

# To restart the container:
docker-compose restart risotto
docker-compose up -d

# To force update the dataset and artifacts:
docker-compose exec risotto python scripts/preprocess.py -f

# To stop the container:
docker-compose down -v
```

```bash
docker-compose build
docker-compose up -d
# To stop the container:
docker-compose down -v
```

# How to contribute

## How to get started

Before anything else, please install the `nbdev` git hooks that run automatic scripts during each commit and merge to strip the notebooks of superfluous metadata (and avoid merge conflicts). After cloning the repository, run the following command inside it:
```
nbdev_install_git_hooks
```

## Did you find a bug?

* Ensure the bug was not already reported by searching on GitHub under Issues.
* If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.
* Be sure to add the complete error messages.

#### Did you write a patch that fixes a bug?

* Open a new GitHub pull request with the patch.
* Ensure that your PR includes a test that fails without your patch, and pass with it.
* Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.


## PR submission guidelines

* Keep each PR focused. While it's more convenient, do not combine several unrelated fixes together. Create as many branches as needing to keep each PR focused.
* Do not mix style changes/fixes with "functional" changes. It's very difficult to review such PRs and it most likely get rejected.
* Do not add/remove vertical whitespace. Preserve the original style of the file you edit as much as you can.
* Do not turn an already submitted PR into your development playground. If after you submitted PR, you discovered that more work is needed - close the PR, do the required work and then submit a new PR. Otherwise each of your commits requires attention from maintainers of the project.
* If, however, you submitted a PR and received a request for changes, you should proceed with commits inside that PR, so that the maintainer can see the incremental fixes and won't need to review the whole PR again. In the exception case where you realize it'll take many many commits to complete the requests, then it's probably best to close the PR, do the work and then submit it again. Use common sense where you'd choose one way over another.


## Do you want to contribute to the documentation?

* Docs are automatically created from the notebooks.
