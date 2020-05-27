import os
import sys
from pathlib import Path

"""
The following environment variables must be set in order to download the dataset:
- KAGGLE_USERNAME
- KAGGLE_KEY
See https://www.kaggle.com/docs/api for more information.
"""

CORD19_DATASET_FOLDER = Path("./datasets/CORD-19-research-challenge")
ARTIFACTS_PATH = "./artifacta"
DATASETS_PATH = "./dataseta"

sys.path.append(".")


def main():
    from risotto.downloader import download_cord19_dataset
    from risotto.artifacts import build_artifacts

    forced = False

    if forced or len(os.listdir(DATASETS_PATH)) <= 1:
        print("Downloading dataset")
        download_cord19_dataset()
        forced = True
    else:
        print("Using previously downloaded dataset")

    if forced or len(os.listdir(ARTIFACTS_PATH)) <= 1:
        print(
            "Building artifacts. You may go for a coffee, this will take some time..."
        )
        _, _, _ = build_artifacts(CORD19_DATASET_FOLDER)
    else:
        print("Using previously built artifacts")

    sys.exit(0)


if __name__ == "__main__":
    main()
