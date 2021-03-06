import os
import sys
import time

import streamlit as st
import numpy as np

sys.path.append(".")

from risotto.artifacts import ARTIFACTS_FOLDER_NAME, load_papers_artifact
from risotto.zero_shot import load_entailments_artifact

ARTIFACT_NAME = os.environ.get("ARTIFACT_NAME", "entailments_artifact.hdf")
BERT_ARTIFACT_NAME = os.environ.get("BERT_ARTIFACT_NAME", "nli_bert_artifacts.hdf")
artifacts_path = os.path.join(ARTIFACTS_FOLDER_NAME, ARTIFACT_NAME)
bert_artifact_path = os.path.join(ARTIFACTS_FOLDER_NAME, BERT_ARTIFACT_NAME)


@st.cache
def get_papers():
    papers = load_papers_artifact(artifacts_path)
    # Scale PageRank to be in (0, 1) in log scale
    papers["pagerank"] = np.log(papers["pagerank"])
    mean_pagerank = papers["pagerank"].mean()
    std_pagerank = papers["pagerank"].std()
    papers["pagerank"] = (papers["pagerank"] - mean_pagerank) / std_pagerank
    min_pagerank = papers["pagerank"].min()
    max_pagerank = papers["pagerank"].max()
    papers["pagerank"] = (papers["pagerank"] - min_pagerank) / (max_pagerank - min_pagerank)
    return papers

@st.cache
def get_papers_entailments(artifact_path):
    return load_entailments_artifact(artifact_path)


models = {
    "BART": artifacts_path,
    "BERT": bert_artifact_path,
}

order_criteria = {
    "Entailment": ("entailments", False),
    "PageRank": ("pagerank", False),
}

# Main widgets
st.title("RISOTTO")
st.subheader("What do we know about vaccines and therapeutics?")

# Sidebar widgets
st.sidebar.title("Parameter tuning")

model_select = st.sidebar.selectbox("Language model:", list(models.keys()))

papers = get_papers()
papers_entailments = get_papers_entailments(models[model_select])

entailment_threshold = st.sidebar.slider("Entailment threshold:", min_value=0.0, max_value=100.0, value=85.0)

min_pagerank = papers["pagerank"].min()
max_pagerank = papers["pagerank"].max()
default_pagerank = max_pagerank - 1.5 * (max_pagerank - min_pagerank) / 2
pagerank_threshold = st.sidebar.slider("PageRank threshold:", min_value=min_pagerank, max_value=max_pagerank, value=default_pagerank)

order_by_select = st.sidebar.selectbox("Order by:", list(order_criteria.keys()))

st.sidebar.button("Search", key="search_sidebar")

# TODO: add more descriptions
st.sidebar.markdown("""
---

We use pre-trained models on the [MultiNLI](https://cims.nyu.edu/~sbowman/multinli/) corpus to obtain relevant research from the [CORD-19 papers](https://arxiv.org/abs/2004.10706) regarding vaccines and therapeutics.
We pose the problem as a [Zero Shot Text Classification](https://www.aclweb.org/anthology/D19-1404/) task leveraging the Natural Language Inference framework, whereas each paper is a premise and "this paper is about vaccines and therapeutics" is the hypothesis.

This method is inspired by [experiments made at HuggingFace](https://joeddav.github.io/blog/2020/05/29/ZSL.html).

For more details, see [this notebook](https://github.com/Inria-Chile/risotto/blob/master/07_ZeroShotTopicClassificationCORD19.ipynb).
""")

# Do the search
papers_with_entailments = papers.join(papers_entailments)
entailment_filter = papers_entailments > entailment_threshold
pagerank_filter = papers["pagerank"] > pagerank_threshold
relevant_papers = papers_with_entailments[entailment_filter & pagerank_filter]
sort_column, sort_ascending = order_criteria[order_by_select]
papers_by_relevance = relevant_papers.sort_values(by=sort_column, ascending=sort_ascending)


for i in range(min(20, len(papers_by_relevance))):
    paper = papers_by_relevance.iloc[i]

    st.write(f"""
**{paper.title} ({paper.publish_time})**

{paper.authors}

[https://doi.org/{paper.doi}](https://doi.org/{paper.doi})

Entailment: {paper.entailments:.2f}%; PageRank: {paper.pagerank:.2f}

---
""")

if len(papers_by_relevance) == 0:
    st.write("There aren't relevant papers")
