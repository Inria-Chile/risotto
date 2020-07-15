import os
import sys
import time

import streamlit as st
import numpy as np

sys.path.append(".")

from risotto.artifacts import ARTIFACTS_FOLDER_NAME, load_papers_artifact, load_papers_embeddings
from risotto.zero_shot import cosine_distance_query, get_sentence_transformer

ARTIFACT_NAME = os.environ.get("ARTIFACT_NAME", "zero_shot_artifacts.hdf")
artifacts_path = os.path.join(ARTIFACTS_FOLDER_NAME, ARTIFACT_NAME)


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
def get_papers_embeddings():
    return load_papers_embeddings(artifacts_path)

@st.cache(allow_output_mutation=True)
def get_model():
    return get_sentence_transformer()


papers = get_papers()
papers_embeddings = get_papers_embeddings()
model = get_model()

order_criteria = {
    "PageRank": ("pagerank", False),
    "Cosine Similarity": ("distances", True)
}

# Main widgets
st.title("RISOTTO")
query_label = "What do we know about"
query_text = st.text_input(f"{query_label}...", value="vaccines and therapeutics?")
st.button("Search", key="search_main")
st.subheader("Relevant research")

# Sidebar widgets
st.sidebar.markdown("""
<p>
    <img src="https://raw.githubusercontent.com/Inria-Chile/risotto/master/assets/inria-white.png" alt="Inria Chile" width="270"/>
</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
RISOTTO is still in an early stage.
We expect to deploy RISOTTO 2.0 in the coming days.

---
""")
st.sidebar.title("Parameter tuning")

similarity_threshold = st.sidebar.slider("Cosine similarity threshold:", min_value=0.0, max_value=1.0, value=0.65)

min_pagerank = papers["pagerank"].min()
max_pagerank = papers["pagerank"].max()
default_pagerank = max_pagerank - 1.5 * (max_pagerank - min_pagerank) / 2
pagerank_threshold = st.sidebar.slider("PageRank threshold:", min_value=min_pagerank, max_value=max_pagerank, value=default_pagerank)

order_by_select = st.sidebar.selectbox("Order by:", list(order_criteria.keys()))

st.sidebar.button("Search", key="search_sidebar")

st.sidebar.markdown("""
---

We use [Sentence-BERT](https://arxiv.org/abs/1908.10084) to embed the [CORD-19](https://arxiv.org/abs/2004.10706) papers and the never-seen-before queries in order to measure the cosine similariry and assess the papers relevance to the question.
This method is inspired by [experiments made at HuggingFace](https://joeddav.github.io/blog/2020/05/29/ZSL.html).

For more details, see [this notebook](https://github.com/Inria-Chile/risotto/blob/master/07_ZeroShotTopicClassificationCORD19.ipynb).
""")

# Do the search
papers_distances = cosine_distance_query(model, f"{query_label} {query_text}", papers_embeddings)
papers_with_distances = papers.join(papers_distances)
similarity_filter = (1 - papers_distances) > similarity_threshold
pagerank_filter = papers["pagerank"] > pagerank_threshold
relevant_papers = papers_with_distances[similarity_filter & pagerank_filter]
sort_column, sort_ascending = order_criteria[order_by_select]
papers_by_relevance = relevant_papers.sort_values(by=sort_column, ascending=sort_ascending)


for i in range(min(20, len(papers_by_relevance))):
    paper = papers_by_relevance.iloc[i]

    st.write(f"""
**{paper.title} ({paper.publish_time})**

{paper.authors}

[https://doi.org/{paper.doi}](https://doi.org/{paper.doi})

Cosine similarity: {(1 - paper.distances):.2f}; PageRank: {paper.pagerank:.2f}

---
""")

if len(papers_by_relevance) == 0:
    st.write("There aren't relevant papers")
