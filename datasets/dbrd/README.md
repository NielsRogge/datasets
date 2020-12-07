# Dataset Card for DBRD

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** https://benjaminvdb.github.io/DBRD/
- **Repository:** https://github.com/benjaminvdb/DBRD
- **Paper:** https://arxiv.org/abs/1910.00896
- **Leaderboard:** https://paperswithcode.com/sota/sentiment-analysis-on-dbrd
- **Point of Contact:** Benjamin van der Burgh (b.van.der.burgh@liacs.leidenuniv.nl)

### Dataset Summary

The DBRD (pronounced dee-bird) dataset contains over 110k book reviews along with associated binary sentiment polarity labels. It is greatly influenced by the Large Movie Review Dataset and intended as a benchmark for sentiment classification in Dutch. The scripts that were used to scrape the reviews from Hebban can be found in the DBRD [GitHub repository](https://github.com/benjaminvdb/DBRD).

### Supported Tasks and Leaderboards

- `text-classification`: The dataset can be used to train a model for text classification, which consists in classifying whether a given review is positive or negative. Success on this task is typically measured by achieving a *high* [accuracy](https://huggingface.co/metrics/accuracy) or *high* [f1](https://huggingface.co/metrics/f1). The RobBERT model currently achieves an accuracy and f1 of 94.422%. The base model can be found in the HuggingFace [model hub](https://huggingface.co/pdelobelle/robbert-v2-dutch-base).
- This task has an active (but unofficial) leaderboard which can be found at [Papers with Code](https://paperswithcode.com/sota/sentiment-analysis-on-dbrd) and ranks models based on [accuracy](https://huggingface.co/metrics/accuracy) and [f1](https://huggingface.co/metrics/f1).

### Language

Dutch

## Dataset Structure

The dataset includes three folders with data: `test` (test split), `train` (train split) and `unsup` (remaining reviews).
Each review is assigned a unique identifier and can be deduced from the filename, as well as the rating: `[ID]_[RATING].txt`. *This is different from the Large Movie Review Dataset, where each file in a directory has a unique ID, but IDs are reused between folders.*

The `urls.txt` file contains on line `L` the URL of the book review on Hebban for the book review with that ID, i.e., the URL of the book review in `48091_5.txt` can be found on line 48091 of `urls.txt`. It cannot be guaranteed that these pages still exist.

```
├── README.md     // the file you're reading
├── test          // balanced 10% test split
│   ├── neg
│   └── pos:
├── train:        // balanced 90% train split
│   ├── neg
│   └── pos
└── unsup         // unbalanced positive and neutral
└── urls.txt      // urls to reviews on Hebban
```

### Data Instances
A typical example looks like this:
```
{
  'text': 'Het boek was heel mooi! Aanrader.'
  'label': 'positief'
}
```

### Data Fields

[More Information Needed]

### Data Splits

The data is splitted in 3 parts: train, test and unsupervised. The train and test splits are balanced (i.e. contain as many positive as negative reviews). The unsupervised split (which are the remaining, unlabeled reviews) consists of only positive and neutral reviews. 

The splits have the following size:
````
  #all:           118516 (= #supervised + #unsupervised)
  #supervised:     22252 (= #training + #testing)
  #unsupervised:   96264
  #training:       20028
  #testing:         2224
````
The distribution of the labels `positive/negative/neutral` in rounded percentages:
````
  training: 50/50/ 0
  test:     50/50/ 0
  unsup:    72/ 0/28
````  

## Dataset Creation

### Curation Rationale

This dataset was created for testing out the [ULMFiT](https://arxiv.org/abs/1801.06146) (by Jeremy Howard and Sebastian Ruder) deep learning algorithm for text classification which is implemented in the [FastAI](https://github.com/fastai/fastai) Python library.

### Source Data

#### Initial Data Collection and Normalization

The data is scrapted from the [Hebban](https://www.hebban.nl/) website. The scripts that were used for scraping can be found on the DBRD [Github repository](https://github.com/benjaminvdb/DBRD).

#### Who are the source language producers?

The reviews are written by people who like to write a book review on the website of [Hebban](https://www.hebban.nl/), a Dutch website which collects and maintains book reviews.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

All code in this repository is licensed under a MIT License.

The dataset is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Citation Information

Please use the following citation when making use of this dataset in your work.

```
@article{DBLP:journals/corr/abs-1910-00896,
  author    = {Benjamin van der Burgh and
               Suzan Verberne},
  title     = {The merits of Universal Language Model Fine-tuning for Small Datasets
               - a case with Dutch book reviews},
  journal   = {CoRR},
  volume    = {abs/1910.00896},
  year      = {2019},
  url       = {http://arxiv.org/abs/1910.00896},
  archivePrefix = {arXiv},
  eprint    = {1910.00896},
  timestamp = {Fri, 04 Oct 2019 12:28:06 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1910-00896.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```