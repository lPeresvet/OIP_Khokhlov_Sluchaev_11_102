import math
import os
from collections import Counter

import pymorphy3
from nltk import wordpunct_tokenize

from hw_2.page_payload_extractor import extract_page

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
raw_files_dir = os.path.join(PROJECT_ROOT, "out")
TOKENS_PATH = os.path.join(PROJECT_ROOT, "out", "tokens")
res_path = os.path.join(PROJECT_ROOT, "hw_4", "out")
morph = pymorphy3.MorphAnalyzer()


def get_tokens():
    tokens_map = {}

    for fname in sorted(os.listdir(TOKENS_PATH)):
        if fname.startswith("tokens_") and fname.endswith(".txt"):
            file_num = fname.replace("tokens_", "").replace(".txt", "")
            path = os.path.join(TOKENS_PATH, fname)
            with open(path, 'r', encoding='utf-8') as f:
                tokens = []
                for line in f:
                    tok = line.strip()
                    if tok:
                        tokens.append([tok])
                tokens_map[file_num] = tokens

    return tokens_map


def get_lemmas():
    lemmas_map = {}

    for fname in sorted(os.listdir(TOKENS_PATH)):
        if fname.startswith("lemmas_") and fname.endswith(".txt"):
            file_num = fname.replace("lemmas_", "").replace(".txt", "")
            path = os.path.join(TOKENS_PATH, fname)
            with open(path, 'r', encoding='utf-8') as f:
                groups = []
                for line in f:
                    forms = line.strip().split()
                    if forms:
                        groups.append(forms)
                lemmas_map[file_num] = groups

    return lemmas_map


class TfIdfCalculator:
    def __init__(self):
        self.tokens = get_tokens()
        self.lemmas = get_lemmas()

        self.file_names = []
        self.documents_words = {}
        self.counters = {}

    def load_data(self):
        if len(self.file_names) > 0 and len(self.documents_words) > 0 and len(self.counters) > 0:
            return

        for fname in sorted(os.listdir(raw_files_dir)):

            if not fname.isdigit():
                continue

            base_name, text = os.path.splitext(fname)
            path = os.path.join(raw_files_dir, fname)
            self.file_names.append(base_name)
            print(fname)

            extracted_text = extract_page(path).lower()
            tokens = wordpunct_tokenize(extracted_text)

            allowed_words = {word for group in self.tokens[base_name] for word in group}
            data = [w for w in tokens if w in allowed_words]

            self.documents_words[base_name] = data
            self.counters[base_name] = Counter(data)

    def compute_tf(self, word_groups):
        result = {}

        for file_id in self.documents_words:
            doc = self.documents_words[file_id]
            counter = self.counters[file_id]
            total = len(doc)

            tf_for_doc = {}

            for group_list in word_groups.get(file_id, []):
                group_key = ' '.join(group_list)
                count = sum(counter.get(w, 0) for w in group_list)
                tf_for_doc[group_key] = count / total if total > 0 else 0.0

            result[file_id] = tf_for_doc

        return result

    def compute_idf(self, word_groups):
        total_docs = len(self.counters)

        idf_result = {}

        for file_id, group_list in word_groups.items():
            idf_result[file_id] = {}

            for group in group_list:
                words = group
                group_key = ' '.join(words)

                df = sum(
                    1 for counter in self.counters.values()
                    if any(counter.get(w, 0) > 0 for w in words)
                )

                idf_value = math.log10(total_docs / df) if df > 0 else 0.0
                idf_result[file_id][group_key] = idf_value

        return idf_result

    @staticmethod
    def compute_tf_idf(tf_dict, idf_dict):
        result = {}

        for file_id in tf_dict:
            tf_doc = tf_dict[file_id]
            idf_doc = idf_dict.get(file_id, {})

            result[file_id] = {
                word: tf_doc[word] * idf_doc.get(word, 0.0)
                for word in tf_doc
            }

        return result

    def calculate_tf_idf(self, subdir: str, use_lemmas: bool, word_groups):
        self.load_data()

        tf_list = self.compute_tf(word_groups)
        idf_dict = self.compute_idf(word_groups)
        tfidf = self.compute_tf_idf(tf_list, idf_dict)

        out_dir = os.path.join(res_path, subdir)
        os.makedirs(out_dir, exist_ok=True)

        for file_id, tf_idf_doc in tfidf.items():
            out_path = os.path.join(out_dir, f"{file_id}_tf_idf.txt")

            with open(out_path, 'w', encoding='utf-8') as f:
                for group in word_groups.get(file_id, []):
                    group_key = ' '.join(group)
                    idf_val = idf_dict.get(file_id, {}).get(group_key, 0.0)
                    tfidf_val = tf_idf_doc.get(group_key, 0.0)

                    visible_key = group[0]
                    if use_lemmas:
                        visible_key = self.get_group_lemma(group)

                    f.write(f"{visible_key} {idf_val:.6f} {tfidf_val:.6f}\n")

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
    processor = TfIdfCalculator()

    processor.calculate_tf_idf(subdir="tokens", use_lemmas=False, word_groups=processor.tokens)
    processor.calculate_tf_idf(subdir="lemmas", use_lemmas=True, word_groups=processor.lemmas)
