import dataclasses
import datetime
import json
import time
import types

from threading import Thread

import requests
from flask import jsonify
from requests import Session
from requests.adapters import HTTPAdapter
from donstu_api.parse_utils import parsers


API_PREFIX = "https://lk.donstu.ru/api"
RASP_URL = "https://lk.donstu.ru/api/RaspManager"
MARKS_URL = "https://lk.donstu.ru/api/students/ActiveModulesList"


@dataclasses.dataclass
class ResponseData:
    is_success: bool
    message: str | None
    data: list | dict | None

    def __str__(self):
        return f"""
        {{
            "is_success": {self.is_success},
            "message": {self.message},
            "data": {self.data}
        }}
        """

    def to_json(self):
        return jsonify(
            {
                "is_success": self.is_success,
                "message": self.message,
                "data": self.data
            }
        )


def _api_request(request: types.FunctionType):
    """
    Декоратор запросов к API ДГТУ для автоматической обработки исключений, десериализации данных из тела ответа и
    упаковки данных в класс ResponseData
    """
    def _request_wrapper(*request_args, **request_kwargs) -> ResponseData:
        try:
            response = request(*request_args, **request_kwargs)

            if response.status_code == 200:
                if response.headers.get('Content-Type').startswith('application/json'):
                    data = json.loads(response.content)
                    deserialization_rule = parsers[request.__name__]

                    if data["state"] == 1:
                        return ResponseData(True, None, deserialization_rule(data))
                    else:
                        return ResponseData(False,
                                            f"Success request but server returns incorrect response with this "
                                            f"message - [{data['msg']}]", None)
                else:
                    return ResponseData(False, f"Success request but server returns non-json response", None)
            else:
                return ResponseData(False, f"Request ends with this status code - [{response.status_code}]", None)

        except Exception as er:
            return ResponseData(False, f"Request ends with this error - [{er}]", None)

    return _request_wrapper


class UserSession(Session):
    _last_use_timestamp = time.time()

    def __init__(
            self,
            token: str,
            max_retries: int = 4
    ):
        super().__init__()

        self.mount(API_PREFIX, adapter=HTTPAdapter(max_retries=max_retries))
        self.headers["Authorization"] = token

    @_api_request
    def get_rasp_today(self):
        self._last_use_timestamp = time.time()

        date = datetime.date.today()
        year = date.year
        month = date.month

        return self.get(
            RASP_URL,
            params={
                "educationSpaceID": 4,
                "month": month,
                "showJournalFilled": False,
                "year": f"{year - 1}-{year}" if month < 9 else f"{year}-{year + 1}"
            }
        )

    @_api_request
    def get_rasp_tomorrow(self):
        self._last_use_timestamp = time.time()

        date = datetime.date.today() + datetime.timedelta(days=1)
        year = date.year
        month = date.month

        return self.get(
            RASP_URL,
            params={
                "educationSpaceID": 4,
                "month": month,
                "showJournalFilled": False,
                "year": f"{year - 1}-{year}" if month < 9 else f"{year}-{year + 1}"
            }
        )

    @_api_request
    def get_marks(self):
        self._last_use_timestamp = time.time()

        return self.get(
            MARKS_URL,
            params={"educationSpaceID": 4}
        )


class UsersSessionsPool:
    """
    Простой вспомогательный класс позволяющий создавать и хранить в себе активные сессии пользователей в виде словаря,
    где ключ это токен авторизации пользователя. Позволяет автоматически удалять из оперативной памяти долго не
    используемые сессии в отдельном потоке
    :arg session_reset_time: период очистки сессий в секундах
    :arg max_request_retries: количество повторений запроса
    """
    _sessions: {str: UserSession} = {}
    """
    Словарь содержащий все активные пользовательские сессии
    """

    def __init__(
            self,
            session_reset_time: int = 600,
            max_request_retries: int = 4
    ):
        self.requests_max_retries = max_request_retries

        self._clear_thread = Thread(
            target=self._clear_sessions_task,
            args=(self._sessions, session_reset_time),
            daemon=True
        )
        self._clear_thread.start()

    @staticmethod
    def _clear_sessions_task(sessions: {str: UserSession}, clear_time):
        while True:
            time.sleep(clear_time)

            if len(sessions) > 0:
                old_time = time.time() - clear_time

                for key, value in list(sessions.items()):
                    if old_time > value._last_use_timestamp:
                        del sessions[key]

    def temporal_auth_session(self) -> UserSession:
        return UserSession(None, self.requests_max_retries)

    def __contains__(self, item):
        return item in self._sessions.keys()

    def __getitem__(self, item) -> UserSession:
        if item not in self._sessions:
            self._sessions[item] = UserSession(item, self.requests_max_retries)
        return self._sessions[item]

    def __setitem__(self, key, value):
        self._sessions[key] = value

    def __delitem__(self, key):
        del self._sessions[key]

    def __len__(self):
        return len(self._sessions)

    def __str__(self):
        return str(self._sessions)
