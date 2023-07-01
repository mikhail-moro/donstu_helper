import unittest

from analyze.analyzer import VectorizeAnalyzer
from analyze.speech2text import Recognizer


TEST_RECORD_PATH = "test_record.m4a"
TEST_RECORD_TEXT = "мы расписание на сегодня пожалуйста сегодня"
TEST_RECORD_CLASS = 0


recognizer = Recognizer(
    model_path="..\\recognize_model\\vosk-model-small-ru-0.22",
)
analyzer = VectorizeAnalyzer(
    vectorize_data_path="..\\vectorize_data.xlsx"
)


class TextRecognizeTest(unittest.TestCase):
    def test_speech2text(self):
        with open(TEST_RECORD_PATH, 'rb') as bin_data:
            result = recognizer.recognize(bin_data.read())

        print(result)
        self.assertEqual(result, TEST_RECORD_TEXT)


class AnalyzeTest(unittest.TestCase):
    def test_analyze(self):
        with open(TEST_RECORD_PATH, 'rb') as bin_data:
            result = recognizer.recognize(bin_data.read())
        analyze = analyzer.get_result(result)

        print(analyze)
        self.assertEqual(analyze, TEST_RECORD_CLASS)


if __name__ == "__main__":
    unittest.main()
