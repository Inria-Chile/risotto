# 🍚 RISOTTO

> Research Intelligent Support and Organization TOol against COVID-19

![Python 3.x](https://img.shields.io/badge/python-3.x-green.svg)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Inria-Chile/risotto)
[![License: CeCILL-B](https://img.shields.io/badge/license-CeCILL--B-orange)](https://cecill.info/licences.en.html)

# Context

One of the positive implications of the Covid-19 outbreak is that it has generated a massive amount of focused scientific effort that is disseminated as research papers. However, because of the novel and massive amount of information that is being generated, traditional hand-annotated, ontology-based or supervised (tag-based) learning NLP methods are not able to handle the task of supporting research and understanding results in an adequate manner.

So far, to the best of our knowledge, there is not a research support tool that exploits the current state of the art of unsupervised learning in NLP that could be used to provide a quick response to this problem.

Consequently, our proposal is to generate as fast as possible a research support tool that applies the state of the art unsupervised NLP and ML methods that will able to:

- analyze all research papers available from global online sources,
- automatically detect hierarchical groups of these papers and topics,
- present leading "popular" papers as well as potential breakthroughs and new results, and
- provide a visualization tool to understand how is the progress doing what areas are receiving more attention in time, etc.

**Note:** It is expected that, as we progress on the conception and development of this tool new tasks/tools will be added to this list.

# How to use

## How to use Risotto locally

In order to use Risotto you will need a Kaggle username and key

### 1. Get Kaggle Api key

If you do not have a Kaggle api key, you may follow the instructions here: https://www.kaggle.com/docs/api. You can set your API key by either:

- Copying the `kaggle.json` file in your local system, in `~/.kaggle/kaggle.json` for Linux/Mac or `C:\Users<Windows-username>.kaggle\kaggle.json` for Windows

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

### 2. Clone or download the repository

```bash
git clone git@github.com:Inria-Chile/risotto.git
cd risotto
```

### 3. Build virtual environment with python3 and install requirements

```bash
python -m virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the prerelease script

```bash
source venv/bin/activate # If you have not sourced the virtualenvironment already
python scripts/prerelease.py
```

### 5. Run the GUI

The GUIwill be available at localhost:8000

```bash
source venv/bin/activate # If you have not sourced the virtualenvironment already
voila --port=8000 --no-browser --enable_nbextensions=True 06_GUI.ipynb
```

# How to contribute

## How to get started

Before anything else, please install the git hooks that run automatic scripts during each commit and merge to strip the notebooks of superfluous metadata (and avoid merge conflicts). After cloning the repository, run the following command inside it:

```bash
nbdev_install_git_hooks
```

**Note:** if you installed the full requirements list on `requirements.txt` you can skip this, as it is already included there.

## Did you find a bug?

- Ensure the bug was not already reported by searching on GitHub under Issues.
- If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.
- Be sure to add the complete error messages.

#### Did you write a patch that fixes a bug?

- Open a new GitHub pull request with the patch.
- Ensure that your PR includes a test that fails without your patch, and pass with it.
- Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

## PR submission guidelines

- Keep each PR focused. While it's more convenient, do not combine several unrelated fixes together. Create as many branches as needing to keep each PR focused.
- Do not mix style changes/fixes with "functional" changes. It's very difficult to review such PRs and it most likely get rejected.
- Do not add/remove vertical whitespace. Preserve the original style of the file you edit as much as you can.
- Do not turn an already submitted PR into your development playground. If after you submitted PR, you discovered that more work is needed - close the PR, do the required work and then submit a new PR. Otherwise each of your commits requires attention from maintainers of the project.
- If, however, you submitted a PR and received a request for changes, you should proceed with commits inside that PR, so that the maintainer can see the incremental fixes and won't need to review the whole PR again. In the exception case where you realize it'll take many many commits to complete the requests, then it's probably best to close the PR, do the work and then submit it again. Use common sense where you'd choose one way over another.

## Do you want to contribute to the documentation?

- Docs are automatically created from the notebooks in the nbs folder.
