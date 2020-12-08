# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""DBRD (Dutch Book Reviews Dataset): 110k Dutch book reviews for sentiment analysis."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
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
"""

_DESCRIPTION = """\
The DBRD (pronounced dee-bird) dataset contains over 110k book reviews along with associated binary sentiment polarity labels. 
It is greatly influenced by the Large Movie Review Dataset and intended as a benchmark for sentiment classification in Dutch. 
The reviews were scraped from the Dutch Hebban website (https://hebban.nl) using scripts which can be found in the DBRD GitHub repository
(https://github.com/benjaminvdb/DBRD). 
"""

_HOMEPAGE = "https://benjaminvdb.github.io/DBRD/"

_LICENSE = """\
All code in this repository is licensed under a MIT License.
The dataset is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
"""

_DOWNLOAD_URL = "https://github.com/benjaminvdb/DBRD/releases/download/v3.0/DBRD_v3.tgz"

_TRAIN_FILE = "train.jsonl"
_VAL_FILE = "val.jsonl"
_TEST_FILE = "test.jsonl"


class DBRDConfig(datasets.BuilderConfig):
    """BuilderConfig for DBRD."""

    def __init__(self, **kwargs):
        """BuilderConfig for DBRD.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(DBRDConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class DBRDDataset(datasets.GeneratorBasedBuilder):
    """DBRD (Dutch Book Reviews Dataset): 110k Dutch book reviews for sentiment analysis."""

    BUILDER_CONFIGS = [
        DBRDConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"text": datasets.Value("string"), "label": datasets.features.ClassLabel(names=["neg", "pos"])}
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _vocab_text_gen(self, archive):
        for _, ex in self._generate_examples(archive, os.path.join("aclImdb", "train")):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        # the data is splitted in 3 directories: train, test and unsup (which means unsupervised, i.e.
        # the remaining reviews). 
        arch_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "110kDBRD")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"directory": os.path.join(data_dir, "train")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"directory": os.path.join(data_dir, "test")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split("unsupervised"),
                gen_kwargs={"directory": os.path.join(data_dir, "unsup"), "labeled": False},
            ),
        ]

    def _generate_examples(self, directory, labeled=True):
        """Generate DBRD examples."""
        # For labeled examples, extract the label from the path.
        if labeled:
            files = {
                "pos": sorted(os.listdir(os.path.join(directory, "pos"))),
                "neg": sorted(os.listdir(os.path.join(directory, "neg"))),
            }
            for key in files:
                for id_, file in enumerate(files[key]):
                    filepath = os.path.join(directory, key, file)
                    with open(filepath, encoding="UTF-8") as f:
                        yield key + "_" + str(id_), {"text": f.read(), "label": key}
        else:
            unsup_files = sorted(os.listdir(os.path.join(directory, "unsup")))
            for id_, file in enumerate(unsup_files):
                filepath = os.path.join(directory, "unsup", file)
                with open(filepath, encoding="UTF-8") as f:
                    yield id_, {"text": f.read(), "label": -1}