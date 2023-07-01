import time
import unittest

from donstu_api.requests import UserSession, UsersSessionsPool

TEST_CORRECT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoid29vZm1lb3czMTQxNUBnbWFpbC5jb20iLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zdXJuYW1lIjoi0JzQvtGA0L7Qt9C-0LIg0Jwu0JIuIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvaGFzaCI6IiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6Ii0yODk3MjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3VzZXJkYXRhIjoiMiIsInZlcmlmU3RyaW5nIjoiIiwibmJmIjoxNjg3NDAzMDM3LCJleHAiOjE2ODgwMDc4MzcsImlzcyI6IlZlZEthZiIsImF1ZCI6Ik1NSVNMYWIifQ.moKB1A5tbd-S81L81NVSJupD8EbjfnZL3JgWk3UHm0o"
TEST_CORRECT_MAIL = "woofmeow31415@gmail.com"
TEST_CORRECT_PASSWORD = "7j837k"

TEST_INCORRECT_TOKEN = "000eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoid29vZm1lb3czMTQxNUBnbWFpbC5jb20iLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zdXJuYW1lIjoi0JzQvtGA0L7Qt9C-0LIg0Jwu0JIuIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvaGFzaCI6IiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6Ii0yODk3MjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3VzZXJkYXRhIjoiMiIsInZlcmlmU3RyaW5nIjoiIiwibmJmIjoxNjg3NDAzMDM3LCJleHAiOjE2ODgwMDc4MzcsImlzcyI6IlZlZEthZiIsImF1ZCI6Ik1NSVNMYWIifQ.moKB1A5tbd-S81L81NVSJupD8EbjfnZL3JgWk3UHm0o"
TEST_INCORRECT_MAIL = "000woofmeow31415@gmail.com"
TEST_INCORRECT_PASSWORD = "0007j837k"


class AuthRequestTest(unittest.TestCase):
    test_session = UserSession(TEST_CORRECT_TOKEN)

    def test_correct_auth(self):
        response = self.test_session.get_token(TEST_CORRECT_MAIL, TEST_CORRECT_PASSWORD)
        print(response)
        self.assertEqual(response.is_success, True, response.message)

    def test_incorrect_auth(self):
        response = self.test_session.get_token(TEST_INCORRECT_MAIL, TEST_INCORRECT_PASSWORD)
        print(response)
        self.assertEqual(response.is_success, False, response.message)


class ApiRequestsCorrectTokenTest(unittest.TestCase):
    test_session = UserSession(TEST_CORRECT_TOKEN)

    def test_get_rasp_month_1(self):
        response = self.test_session.get_rasp(month=1, year=2022)
        print(response)
        self.assertEqual(response.is_success, True, response.message)

    def test_get_rasp_month_12(self):
        response = self.test_session.get_rasp(month=12, year=2022)
        print(response)
        self.assertEqual(response.is_success, True, response.message)

    def test_get_marks(self):
        response = self.test_session.get_marks()
        print(response)
        self.assertEqual(response.is_success, True, response.message)

    def test_get_actual_marks(self):
        response = self.test_session.get_actual_marks()
        print(response)
        self.assertEqual(response.is_success, True, response.message)


class ApiRequestsIncorrectTokenTest(unittest.TestCase):
    test_session = UserSession(TEST_INCORRECT_TOKEN)

    def test_get_rasp_month_1(self):
        response = self.test_session.get_rasp(month=1, year=2022)
        print(response)
        self.assertEqual(response.is_success, True, response.message)

    def test_get_rasp_month_12(self):
        response = self.test_session.get_rasp(month=12, year=2022)
        print(response)
        self.assertEqual(response.is_success, True, response.message)

    def test_get_marks(self):
        response = self.test_session.get_marks()
        print(response)
        self.assertEqual(response.is_success, True, response.message)

    def test_get_actual_marks(self):
        response = self.test_session.get_actual_marks()
        print(response)
        self.assertEqual(response.is_success, True, response.message)


class SessionsPoolTest(unittest.TestCase):
    def test_pool_self_clear(self):
        pool = UsersSessionsPool(session_reset_time=2)
        pool.create_new_session(TEST_CORRECT_TOKEN)

        time.sleep(3)

        self.assertEqual(len(pool), 0)


if __name__ == "__main__":
    unittest.main()
