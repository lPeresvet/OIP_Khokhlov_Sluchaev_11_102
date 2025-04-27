import os
import math
from collections import defaultdict
from typing import Dict, List, Tuple
import pymorphy2
from nltk.tokenize import word_tokenize


class VectorSearch:
    def __init__(self, tfidf_dir: str):
        """
        :param tfidf_dir: Папка с файлами TF-IDF в формате "термин tf idf"
        """
        self.morph = pymorphy2.MorphAnalyzer()
        self.tfidf_dir = tfidf_dir

        # Структуры данных
        self.doc_vectors: Dict[str, Dict[str, float]] = {}  # {doc_id: {term: tfidf}}
        self.term_idf: Dict[str, float] = {}  # {term: idf}
        self.doc_lengths: Dict[str, float] = {}  # {doc_id: vector_length}

        self._load_tfidf_files()
        self._compute_doc_lengths()

    def _load_tfidf_files(self):
        """Загрузка TF-IDF из файлов в указанном формате"""
        for filename in os.listdir(self.tfidf_dir):
            if not filename.endswith('.txt'):
                continue

            doc_id = filename.split('_')[0]+".html"
            self.doc_vectors[doc_id] = {}

            with open(os.path.join(self.tfidf_dir, filename), 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        term = parts[0]
                        tf = float(parts[1])
                        idf = float(parts[2])
                        tfidf = tf * idf

                        self.doc_vectors[doc_id][term] = tfidf
                        # Сохраняем IDF (будет перезаписываться, но значение одинаковое для всех документов)
                        self.term_idf[term] = idf

    def _compute_doc_lengths(self):
        """Вычисление длин векторов документов"""
        for doc_id, terms in self.doc_vectors.items():
            self.doc_lengths[doc_id] = math.sqrt(
                sum(tfidf ** 2 for tfidf in terms.values())
            )

    def preprocess_query(self, query: str) -> List[str]:
        """Нормализация запроса"""
        tokens = word_tokenize(query.lower())
        return [
            self.morph.parse(token)[0].normal_form
            for token in tokens
            if token.isalpha()
        ]

    def search(self, query: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """Поиск с косинусной мерой"""
        query_terms = self.preprocess_query(query)
        if not query_terms:
            return []

        # Векторизация запроса
        query_tf = defaultdict(float)
        for term in query_terms:
            query_tf[term] += 1
        query_len = len(query_terms)

        query_vector = {
            term: (tf / query_len) * self.term_idf.get(term, 0)
            for term, tf in query_tf.items()
        }
        query_norm = math.sqrt(sum(v ** 2 for v in query_vector.values()))

        # Поиск по документам
        scores = []
        for doc_id, doc_vector in self.doc_vectors.items():
            dot_product = sum(
                query_vector.get(term, 0) * doc_vector.get(term, 0)
                for term in query_vector
            )

            doc_norm = self.doc_lengths[doc_id]
            if query_norm > 0 and doc_norm > 0:
                cosine = dot_product / (query_norm * doc_norm)
                scores.append((doc_id, cosine))

        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]


# Пример использования
if __name__ == "__main__":
    TFIDF_DIR = "../hw_4/out/lemmas"

    searcher = VectorSearch(TFIDF_DIR)

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
