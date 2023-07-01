import unittest

from analyze.speech2text import Recognizer


TEST_RECORD_PATH = "test_record.mp3"
TEST_RECORD_TEXT = "расписание я хочу хочу списание и расписание я хочу хочу от списания е пятьдесят подписано по подписи"


class TextAnalyzeTest(unittest.TestCase):
    def test_speech2text(self):
        speech2text = Recognizer(
            model_path="../analyze/for_speech2text/recognize_model/vosk-model-ru-0.22",
            model="small"
        )

        with open(TEST_RECORD_PATH, 'rb') as bin_data:
            result = speech2text.recognize(bytes(bin_data))

        print(result['text'])
        self.assertEqual(result['text'], TEST_RECORD_TEXT)


if __name__ == "__main__":
    unittest.main()
