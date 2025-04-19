import math
import os
from collections import Counter

import pymorphy3
from bs4 import BeautifulSoup
from nltk import wordpunct_tokenize

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
raw_files_dir = os.path.join(PROJECT_ROOT, "out")
TOKENS_PATH = os.path.join(PROJECT_ROOT, "out", "tokens")
res_path = os.path.join(PROJECT_ROOT, "hw4", "out")
morph = pymorphy3.MorphAnalyzer()


def get_tokens():
    tokens = []
    for fname in sorted(os.listdir(TOKENS_PATH)):
        if fname.startswith("tokens_") and fname.endswith(".txt"):
            path = os.path.join(TOKENS_PATH, fname)
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    tok = line.strip()
                    if tok:
                        tokens.append([tok])
    return tokens


def get_lemmas():
    groups = []

    for fname in sorted(os.listdir(TOKENS_PATH)):
        if fname.startswith("lemmas_") and fname.endswith(".txt"):
            with open(os.path.join(TOKENS_PATH, fname), encoding='utf-8') as f:
                for line in f:
                    forms = line.strip().split()
                    if forms:
                        groups.append(forms)

    return groups


class TfIdfCounter:
    def __init__(self):
        self.tokens = get_tokens()
        self.lemmas = get_lemmas()

        self.file_names = []
        self.documents_words = []
        self.counters = []

    def load_data(self, use_lemmas: bool):
        print("load _ data")
        if len(self.file_names) > 0 and len(self.documents_words) > 0 and len(self.counters) > 0:
            return

        for fname in sorted(os.listdir(raw_files_dir)):
            if not fname.isdigit():
                continue

            base, ext = os.path.splitext(fname)
            path = os.path.join(raw_files_dir, fname)
            self.file_names.append(base)
            print(fname)

            with open(path, encoding='utf-8') as f:
                text = BeautifulSoup(f, features='lxml').get_text().lower()
                tokens = wordpunct_tokenize(text)

            # if use_lemmas:
            #     data = []
            #     # for w in tokens:
            #     #     p = morph.parse(w)[0]
            #     #     norm = p.normal_form if p.normalized.is_known else w
            #     #     if norm in self.lemmas:
            #     #         data.append(norm)
            #     data = [w for w in tokens if w in self.lemmas]
            # else:
            data = [w for w in tokens if w in self.tokens]

            self.documents_words.append(data)
            self.counters.append(Counter(data))

    @staticmethod
    def compute_tf(counters, documents, word_groups: list[list[str]]):
        print("tf")
        result = []
        for ctr, doc in zip(counters, documents):
            total = len(doc)
            tf = {}
            for group in word_groups:
                key = ' '.join(group)
                group_count = sum(ctr.get(word, 0) for word in group)
                tf[key] = group_count / total if total > 0 else 0
            result.append(tf)
        return result

    @staticmethod
    def compute_idf(counters, word_groups: list[list[str]]):
        print("idf")
        df = {}
        for group in word_groups:
            key = ' '.join(group)
            df[key] = sum(
                1 for ctr in counters
                if any(ctr.get(word, 0) > 0 for word in group)
            )
        return {
            key: (math.log10(len(counters) / df[key]) if df[key] > 0 else 0)
            for key in df
        }

    @staticmethod
    def compute_tf_idf(tf_list, idf_dict):
        print("tf idf")
        return [{w: tf[w] * idf_dict[w] for w in tf} for tf in tf_list]

    def calculate_tf_idf(self, subdir: str, use_lemmas: bool, word_groups: list[list[str]]):
        self.load_data(use_lemmas)

        tf_list = self.compute_tf(self.counters, self.documents_words, word_groups)
        idf_dict = self.compute_idf(self.counters, word_groups)
        tfidf = self.compute_tf_idf(tf_list, idf_dict)

        out_dir = os.path.join(res_path, subdir)
        os.makedirs(out_dir, exist_ok=True)

        for base_name, tf_idf_doc in zip(self.file_names, tfidf):
            out_path = os.path.join(out_dir, f"{base_name}.txt")
            with open(out_path, 'w', encoding='utf-8') as f:
                for group in word_groups:
                    if use_lemmas:
                        key = self.get_group_lemma(group)
                    else:
                        key = group[0]
                    f.write(f"{key} {idf_dict[key]:.6f} {tf_idf_doc[key]:.6f}\n")

    @staticmethod
    def get_group_lemma(forms) -> str:
        normal_forms = []
        for word in forms:
            parsed = morph.parse(word)[0]
            norm = parsed.normal_form if parsed.normalized.is_known else word
            normal_forms.append(norm)

        most_common = Counter(normal_forms).most_common(1)[0][0]
        return most_common


if __name__ == '__main__':
    processor = TfIdfCounter()

    processor.calculate_tf_idf(subdir="tokens", use_lemmas=False, word_groups=processor.tokens)
    processor.calculate_tf_idf(subdir="lemmas", use_lemmas=True, word_groups=processor.lemmas)
