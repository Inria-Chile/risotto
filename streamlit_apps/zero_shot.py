import time
import sys

import streamlit as st

sys.path.append(".")

from risotto.artifacts import load_papers_artifact, load_papers_embeddings
from risotto.zero_shot import cosine_distance_query, get_sentence_transformer


@st.cache
def get_papers():
    return load_papers_artifact()

@st.cache
def get_papers_embeddings():
    return load_papers_embeddings()

@st.cache(allow_output_mutation=True)
def get_model():
    return get_sentence_transformer()


papers = get_papers()
papers_embeddings = get_papers_embeddings()
model = get_model()

# Sidebar widgets
st.sidebar.title("RISOTTO")

query_label = "What do we know about"
query_text = st.sidebar.text_input(f"{query_label}...", value="vaccines and therapeutics?")

st.sidebar.button("Search")

papers_distances = cosine_distance_query(model, f"{query_label} {query_text}", papers_embeddings)
papers_with_distances = papers.join(papers_distances)
papers_by_relevance = papers_with_distances.sort_values(by="distances", ascending=True)

# Main widgets

st.title("Relevant research")

for i in range(20):
    paper = papers_by_relevance.iloc[i]

    st.write(f"""
**{paper.title} ({paper.publish_time}, {(1 - paper.distances) * 100:.2f}%)**

{paper.authors}

[https://doi.org/{paper.doi}](https://doi.org/{paper.doi})

---
""")
