from argparse import ArgumentParser
from server.app import run_server
from analyze.analyzer import VectorizeAnalyzer
from analyze.speech2text import Recognizer


parser = ArgumentParser()
parser.add_argument("user_session_reset_time", type=int)
parser.add_argument("max_request_retries", type=int)
parser.add_argument("request_max_content_length", type=int)
parser.add_argument("text_data_max_length", type=int)
parser.add_argument("frame_rate", type=int)
parser.add_argument("channels", type=int)
args = parser.parse_args()


recognizer = Recognizer(
    model_path="recognize_model\\vosk-model-small-ru-0.22",
    frame_rate=args.frame_rate,
    channels=args.channels
)

text_analyzer = VectorizeAnalyzer(
    vectorize_data_path="vectorize_data.xlsx"
)


run_server(
    request_max_content_length=args.request_max_content_length,
    text_data_max_length=args.text_data_max_length,
    session_reset_time=args.user_session_reset_time,
    max_request_retries=args.max_request_retries,
    speech_recognizer=recognizer,
    text_analyzer=text_analyzer
)

