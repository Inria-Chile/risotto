import sys
from pathlib import Path

from nbdev.export import notebook2script

"""
The following environment variables must be set in order to download the dataset:
- KAGGLE_USERNAME
- KAGGLE_KEY
See https://www.kaggle.com/docs/api for more information.
"""

CORD19_DATASET_FOLDER = Path("./datasets/CORD-19-research-challenge")

sys.path.append(".")


def main():
    notebook2script()

    from risotto.downloader import download_cord19_dataset
    from risotto.artifacts import build_artifacts

    download_cord19_dataset()
    _, _, _ = build_artifacts(CORD19_DATASET_FOLDER)

    sys.exit(0)


if __name__ == "__main__":
    main()