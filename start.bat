:: Время сброса сессии пользователя для запросов к API ДГТУ в секундах
@SET /a USER_SESSION_RESET_TIME=600
:: Максимальное количество повторов запросов к API ДГТУ
@SET /a MAX_REQUEST_RETRIES=4

:: Максимальная длина данных запроса в байтах
@SET /a REQUEST_MAX_CONTENT_LENGHT=50*1024*1024
:: Максимальная длина текста для анализа в символах
@SET /a TEXT_DATA_MAX_LENGHT=100

:: Фреймрейт входной голосовой записи
@SET /a FRAME_RATE=16000
:: Количество каналов входной записи
@SET /a CHANNELS=1

:: Путь к используемому Python интерпритатору
@SET PY_PATH=C:\Users\yahry\DonSTU_Helper\Scripts\python.exe

%PY_PATH% main.py %USER_SESSION_RESET_TIME% %MAX_REQUEST_RETRIES% %REQUEST_MAX_CONTENT_LENGHT% %TEXT_DATA_MAX_LENGHT% %FRAME_RATE% %CHANNELS%

pause
