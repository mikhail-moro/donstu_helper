from flask import Flask, request, make_response
from analyze.analyzer import Analyzer
from analyze.speech2text import Recognizer
from donstu_api.requests import UsersSessionsPool, ResponseData

SUPPORTED_AUDIO_EXTENSIONS = ['mp4', 'mp3', 'wav', 'wave', 'ogg']  # Может можно и другие, ещё не проверенно

lateinit_request_max_content_length: int
lateinit_text_data_max_length: int
lateinit_users_sessions_pool: UsersSessionsPool
lateinit_speech_recognizer: Recognizer
lateinit_text_analyzer: Analyzer

app = Flask(__name__)


@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    if 'Authorization' not in request.headers:
        return "", 401

    token = request.headers['Authorization']

    if token == '' or token == 'Bearer ' or token == 'Bearer':
        return "", 401

    if request.content_type != 'application/json':
        return "", 415

    if "text" not in request.json:
        return ResponseData(False, "Неправильный формат запроса", None).to_json()

    text_data = request.json["text"]

    if not (0 < len(text_data) < lateinit_text_data_max_length):
        return ResponseData(False, "Запрос либо пустой, либо слишком длинный", None).to_json()

    analyze_result = lateinit_text_analyzer.get_result(text_data)
    user_session = lateinit_users_sessions_pool[token]

    match analyze_result:
        case 0:
            return user_session.get_rasp_today().to_json()
        case 1:
            return user_session.get_rasp_tomorrow().to_json()
        case 2:
            return user_session.get_marks().to_json()


@app.route('/analyze_audio', methods=['POST'])
def analyze_audio():
    if 'Authorization' not in request.headers:
        return "", 401

    token = request.headers['Authorization']

    if token == '' or token == 'Bearer ' or token == 'Bearer':
        return "", 401

    if not request.content_type.startswith('audio'):
        return "", 415

    if not any([ext in request.content_type for ext in SUPPORTED_AUDIO_EXTENSIONS]):
        print(request.content_type)
        return "", 415

    text_data = lateinit_speech_recognizer.recognize(request.data)

    if not (0 < len(text_data) < lateinit_text_data_max_length):
        return ResponseData(False, "Ошибка распознавания текста из записи, запрос либо слишком короткий или длинный,"
                                   "либо его не удалось распознать", None).to_json()

    analyze_result = lateinit_text_analyzer.get_result(text_data)
    user_session = lateinit_users_sessions_pool[token]

    match analyze_result:
        case 0:
            return user_session.get_rasp_today().to_json()
        case 1:
            return user_session.get_rasp_tomorrow().to_json()
        case 2:
            return user_session.get_marks().to_json()


def run_server(
        request_max_content_length: int,
        text_data_max_length: int,
        session_reset_time: int,
        max_request_retries: int,
        speech_recognizer: Recognizer,
        text_analyzer: Analyzer
):
    """
    Запуск сервиса

    :param request_max_content_length: максимальная длина данных запроса в байтах
    :param text_data_max_length: максимальная длина текста для анализа в символах
    :param session_reset_time: время сброса сессии пользователя в секундах
    :param max_request_retries: максимальное количество повторов запросов
    :param speech_recognizer: распознаватель текста из аудиозаписи
    :param text_analyzer: анализатор текста
    """
    global lateinit_text_data_max_length
    global lateinit_speech_recognizer
    global lateinit_text_analyzer
    global lateinit_users_sessions_pool

    lateinit_text_data_max_length = text_data_max_length
    lateinit_speech_recognizer = speech_recognizer
    lateinit_text_analyzer = text_analyzer

    lateinit_users_sessions_pool = UsersSessionsPool(
        session_reset_time=session_reset_time,
        max_request_retries=max_request_retries
    )

    app.config['MAX_CONTENT_LENGTH'] = request_max_content_length
    app.run()
