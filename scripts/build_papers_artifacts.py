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
    from risotto.downloader import download_cord19_dataset
    from risotto.artifacts import build_papers_artifact

    if force or len(os.listdir(DATASETS_PATH)) <= 1:
        print("Downloading dataset")
        download_cord19_dataset()
        force = True
    else:
        print("Using previously downloaded dataset")

    if force or len(os.listdir(ARTIFACTS_PATH)) <= 1:
        print(
            "Building artifacts. You may go for a coffee, this will take some time..."
        )
        _, _, _ = build_papers_artifact(CORD19_DATASET_FOLDER)
    else:
        print("Using previously built artifacts")

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
