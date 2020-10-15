---
author: Rodolfo Palma
geometry: margin=2cm
urlcolor: blue
---

# RISOTTO - Research Intelligent Support and Organization TOol for fighting against COVID-19

RISOTO is a project developed to help researchers navigate through the vast amount of COVID-19--related papers that have been published in recent months.

The [Allen Institute for AI](https://allenai.org/) and other collaborating institutions have consolidated the different sources of openly available research papers in the [COVID-19 Open Research Dataset (CORD-19)](https://www.semanticscholar.org/cord19) (CORD-19, Wang et al., 2020).
From March 2020 to October 2020 CORD-19 has grown from about 28 000 papers to more than 288 800, thus multiplying the number of papers more than ten times.
This dataset has received wide attention in the data mining and natural language processing community in order to develop tools to aid health workers stay up-to-date with the latest and most relevant research about the current pandemic.

Three web applications and prototypes were built leveraging modern natural language processing (NLP) and information retrieval techniques.
This document will explain the techniques and technical decisions characterizing each one of them.

## Two--Stage LDA Web Application

This application implements a two--stage LDA approach to organize the CORD-19 papers.
The model source code can be found in the following Jupyter Notebooks.

- [`references.ipynb`](https://github.com/Inria-Chile/risotto/blob/master/01_references.ipynb): builds the references directed graph
- [`representations_and_lda.ipynb`](https://github.com/Inria-Chile/risotto/blob/master/02_representations_and_lda.ipynb): builds the encoded representations of each paper
- [`hierarchical_topic_modelling.ipynb`](https://github.com/Inria-Chile/risotto/blob/master/03_hierarchical_topic_modelling.ipynb): trains the two-stage topic models

The PageRank scores of each paper are computed building the references graph of the CORD-19 papers that have full text parsing.
We calculate representations of the papers based on their text content using the `CountVectorizer` encoder available in scikit-learn.
Using these representations, hierarchical topic models are trained using the LDA method.
Finally, the most relevant papers for each topic will be determined using the PageRank scores of each paper.

The hierarchical topic models are implemented as a two--stage LDA topic modeling algorithm.
First, we model the high level corpus topics by running LDA over the entire papers dataset.
The second stage runs LDA over the subgroups of papers modeled by the first stage to model the subtopics.
Since each topic and subtopic is modeled as a mixture of words, we represent them to the end--user as the most relevant words of each mixture.


The models are served through a [lightweight REST backend](https://github.com/Inria-Chile/risotto-backend) built using the Flask web framework.
On the other hand, a [React frontend](https://github.com/Inria-Chile/risotto-frontend) enables users to filter and search the papers leveraging the topic models.
Finally, an [integration repository](https://github.com/Inria-Chile/risotto-integration) orchestrates and coordinates the previous components using docker-compose and an `nginx` reverse proxy.

This application is being served at https://risotto.inria.cl.

### Deployment Instructions

The following steps are required to deploy the two-stage LDA web application in a production environment.

```bash
$ git clone https://github.com/Inria-Chile/risotto-backend.git
$ git clone https://github.com/Inria-Chile/risotto-frontend.git
$ git clone https://github.com/Inria-Chile/risotto-integration.git
$ cp /path/to/artifacts.hdf risotto-integration/artifacts
$ cd risotto-integration/production
$ docker-compose build
$ docker-compose up -d
```

The `artifacts.hdf` file is available at the Shared Google Drive named `Risotto`.
It contains dataframes with the papers content and topic classifications required by the application.

## Zero Shot Prototypes

In the Zero Shot Prototypes we'll create Zero Shot Topic Classifiers for CORD-19.
Essentially, we aim to build a web application capable of receiving natural language questions, such as "what do we know about vaccines and therapeutics?", and then displaying the most relevant research literature regarding the specific question.

Recent advances in NLP, such as OpenAI's GPT-3 (Brown et al., 2020), have shown that large language models can achieve competitive performance on downstream tasks with less task-specific data than it'd be required by smaller models.
However, GPT-3 is currently difficult to use on real world applications due to its size of ~175 billions of parameters.

Recent experiments done at HuggingFace (Davison, 2020) explored the potential of using Sentence-BERT (Reimers and Gurevych, 2020) to separately embed sentences and never-seen-before topic labels.
Then, they'd rank the sentence's topics by measuring the cosine distance between both vectors (Veeranna, 2016), obtaining promising results.

In another experiment, they use a pre-trained natural languange inference (NLI) sequence-pair classifier as an out of-the-box zero shot text classifier, as proposed by Yin et al. (2020).
By using a pre-trained BART model (Lewis et al., 2019) fine-tuned on the Multigenre NLI corpus, they were able to score an F1 score of 53.7 on the Yahoo News dataset.
The dataset has 10 classes and the current supervised models state of the art is an accuracy of 77.62.

Inspired by the previously described prior work, we built two prototypes to solve the task of Zero Shot Topic Classification.
None of these prototypes is ready to be deployed in a production environment, since there are still some hyperparameters that need to be tweaked.

The prototypes were developed using [Streamlit](https://www.streamlit.io/).
For more details about the implementation of these prototypes see [this notebook](https://github.com/Inria-Chile/risotto/blob/master/07_ZeroShotTopicClassificationCORD19.ipynb).

### Cosine Similarity Approach

This prototype implements a cosine similarity approach to assess the relevance of a given natural language question with each paper.

First, we use Sentence-BERT to embed both the papers and the never-seen-before question to measure the cosine similarity and assess the papers relevance to the question.
For the sake of efficiency, we iterate over the dataset and precompute the papers representations using their title and abstract.
Then, we compute the cosine distance between the embedded question and each one of the papers representations.
Finally, the papers might be ordered by their distances to first display those that are relevant to the question.

The script [`streamlit_apps/zero_shot_run.sh`](https://github.com/Inria-Chile/risotto/blob/master/streamlit_apps/zero_shot_run.sh) must be run to serve the Streamlit prototype.

### Natural Language Inference Approach

This prototype leverages pre--trained language models to perform natural language inferences over the papers.
In this approach we use a BART classifier (Lewis et al., 2019) pre-trained on the Multi-Genre NLI (MultiNLI, Williams et al., 2018) corpus as the base model.

Given research interests expressed in natural language, we pose the problem of recovering relevant research from the CORD-19 dataset (Wang et al., 2020) as a Zero Shot Topic Classification task (Yin et al., 2019).
Leveraging the Natural Language Inference task framework, we assess each paper relevance by feeding the model with the paper's title and abstract as premise and a research interest as hypothesis.

Finally, we use the model's entailment inference values as proxy relevance scores for each paper.

The script [`streamlit_apps/nli/run.sh`](https://github.com/Inria-Chile/risotto/blob/master/streamlit_apps/nli/run.sh) must be run to serve the Streamlit prototype.

## References

Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., Wu, J., Winter, C., … Amodei, D. (2020). Language Models are Few-Shot Learners. https://arxiv.org/abs/2005.14165

Davison, J. (2020). Zero-Shot Learning in Modern NLP. https://joeddav.github.io/blog/2020/05/29/ZSL.html

Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A., Levy, O., Stoyanov, V., & Zettlemoyer, L. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension. http://arxiv.org/abs/1910.13461

Reimers, N., & Gurevych, I. (2020). Sentence-BERT: Sentence embeddings using siamese BERT-networks. EMNLP-IJCNLP 2019 - 2019 Conference on Empirical Methods in Natural Language Processing and 9th International Joint Conference on Natural Language Processing, Proceedings of the Conference, 3982–3992. https://doi.org/10.18653/v1/d19-1410

Veeranna, S. P., Nam, J., Mencía, E. L., & Fürnkranz, J. (2016). Using semantic similarity for multi-label zero-shot classification of text documents. ESANN 2016 - 24th European Symposium on Artificial Neural Networks, April, 423–428.

Wang, L. L., Lo, K., Chandrasekhar, Y., Reas, R., Yang, J., Eide, D., Funk, K., Kinney, R., Liu, Z., Merrill, W., Mooney, P., Murdick, D., Rishi, D., Sheehan, J., Shen, Z., Stilson, B., Wade, A. D., Wang, K., Wilhelm, C., … Kohlmeier, S. (2020). CORD-19: The Covid-19 Open Research Dataset. https://arxiv.org/abs/2004.10706

Williams, A., Nangia, N., & Bowman, S. R. (2018). A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference. Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), 1112--1122. http://aclweb.org/anthology/N18-1101

Yin, W., Hay, J., & Roth, D. (2019). Benchmarking zero-shot text classification: Datasets, evaluation and entailment approach. EMNLP-IJCNLP 2019 - 2019 Conference on Empirical Methods in Natural Language Processing and 9th International Joint Conference on Natural Language Processing, Proceedings of the Conference, 3914–3923. https://doi.org/10.18653/v1/d19-1404