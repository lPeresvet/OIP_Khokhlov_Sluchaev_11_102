import math
import os
import json
from collections import defaultdict
from typing import Dict, List, Tuple
import pymorphy2
from nltk.tokenize import word_tokenize


class VectorSearch:
    def __init__(self, tfidf_dir: str, inverted_index_path: str):
        """
        :param tfidf_dir: Папка с файлами TF-IDF (каждый файл - один документ)
        :param inverted_index_path: Путь к файлу инвертированного индекса
        """
        self.morph = pymorphy2.MorphAnalyzer()
        self.tfidf_dir = tfidf_dir
        self.inverted_index_path = inverted_index_path

        self.inverted_index = self.load_inverted_index()
        self.doc_tfidf = self.load_all_tfidf()
        self.doc_lengths = self.calculate_doc_lengths()

    def load_inverted_index(self) -> Dict[str, List[str]]:
        with open(self.inverted_index_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def load_all_tfidf(self) -> Dict[str, Dict[str, float]]:
        doc_tfidf = {}
        for filename in os.listdir(self.tfidf_dir):
            if filename.endswith('.txt'):
                doc_id = filename.split('_')[0]
                doc_tfidf[doc_id] = self.load_doc_tfidf(filename)
        return doc_tfidf

    def load_doc_tfidf(self, filename: str) -> Dict[str, float]:
        tfidf = {}
        with open(os.path.join(self.tfidf_dir, filename), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    term = parts[0]
                    tfidf_score = float(parts[2])
                    tfidf[term] = tfidf_score
        return tfidf

    def calculate_doc_lengths(self) -> Dict[str, float]:
        lengths = {}
        for doc_id, tfidf_scores in self.doc_tfidf.items():
            length = math.sqrt(sum(score ** 2 for score in tfidf_scores.values()))
            lengths[doc_id] = length
        return lengths

    def preprocess_query(self, query: str) -> List[str]:
        tokens = word_tokenize(query.lower())
        lemmas = []
        for token in tokens:
            if token.isalpha():  # Игнорируем числа и пунктуацию
                lemma = self.morph.parse(token)[0].normal_form
                lemmas.append(lemma)
        return lemmas

    def search(self, query: str, top_n: int = 10) -> List[Tuple[str, float]]:
        query_terms = self.preprocess_query(query)
        if not query_terms:
            return []

        relevant_docs = set()
        for term in query_terms:
            if term in self.inverted_index:
                relevant_docs.update(self.inverted_index[term])

        scores = []
        for doc_id in relevant_docs:
            if doc_id not in self.doc_tfidf:
                continue

            score = 0.0
            for term in query_terms:
                score += self.doc_tfidf[doc_id].get(term, 0.0)

            if self.doc_lengths[doc_id] > 0:
                score /= self.doc_lengths[doc_id]

            scores.append((doc_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]


# Пример использования
if __name__ == "__main__":
    TFIDF_DIR = "../hw_4/out/lemmas"
    INVERTED_INDEX_PATH = "../out/inverted_index.json"

    searcher = VectorSearch(TFIDF_DIR, INVERTED_INDEX_PATH)

    while True:
        query = input("Введите поисковый запрос (или '!exit' для выхода): ")
        if query.lower() == '!exit':
            break

        results = searcher.search(query)

        if not results:
            print("Ничего не найдено")
        else:
            print(f"Найдено {len(results)} результатов:")
            for i, (doc_id, score) in enumerate(results, 1):
                print(f"{i}. {doc_id} (релевантность: {score:.4f})")
