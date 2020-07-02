import os
import sys
from pathlib import Path
import argparse


"""
The following environment variables must be set in order to download the dataset:
- KAGGLE_USERNAME
- KAGGLE_KEY
See https://www.kaggle.com/docs/api for more information.
"""

CORD19_DATASET_FOLDER = Path("./datasets/CORD-19-research-challenge")
ARTIFACTS_PATH = "./artifacts"
DATASETS_PATH = "./datasets"

sys.path.append(".")


def main(force):
    from risotto.artifacts import build_papers_embeddings

    build_papers_embeddings(CORD19_DATASET_FOLDER)

    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--force",
        nargs="?",
        const=True,
        dest="force",
        default=False,
        help="Force preprocessing, overriding dataset and artifacts",
    )
    args = parser.parse_args()
    force = args.force
    main(force=force)
