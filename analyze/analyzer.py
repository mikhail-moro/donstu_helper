import re
from abc import ABC

import pandas as pd
import nltk

from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer, tokenizers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances


class Analyzer(ABC):
    """
    Абстрактный класс анализатора текста для более удобного расширения функционала в будущем
    """
    def get_result(self, text: str) -> int:
        """
        Данный метод, по завершению анализа текста, возвращает число (класс) соответствующее одному из
        реализованных на данный момент запросов:

            0 - пары на сегодня

            1 - пары на завтра

            2 - оценки

        :param text: текст для анализа
        """
        pass


class VectorizeAnalyzer(Analyzer):
    """
    Реализация анализатора текста на основе метода опорных векторов
    :arg vectorize_data_path: файл с данными для векторизации (пока что только Excell)
    """
    nltk.download('stopwords')
    vectorizer = CountVectorizer()
    morph = MorphAnalyzer()
    stop = stopwords.words('russian')

    def __init__(
        self,
        vectorize_data_path: str
    ):
        self.table = pd.read_excel(vectorize_data_path)
        self.table_data = self._table_vectorize()

    def get_result(self, text):
        request_tokenize = ' '.join([i for i in str(text).split() if i not in self.stop])
        request_tokenize = self._text_normalize(request_tokenize)

        request_data = self.vectorizer.transform([request_tokenize]).toarray()
        cosine_value = 1 - pairwise_distances(self.table_data, request_data, metric='cosine')

        return int(self.table['Response'].loc[cosine_value.argmax()])

    def _text_normalize(self, text):
        words = re.sub('[^а-я0-9]', ' ', str(text).lower())
        token = tokenizers.simple_word_tokenize(words)

        return ' '.join([self.morph.parse(i)[0].normal_form for i in token])

    def _table_vectorize(self):
        self.table.ffill(axis=0, inplace=True)
        self.table['Lemmatize'] = self.table['Context'].apply(self._text_normalize)

        data = self.vectorizer.fit_transform(self.table['Lemmatize']).toarray()
        features = self.vectorizer.get_feature_names_out()

        return pd.DataFrame(data, columns=features)
