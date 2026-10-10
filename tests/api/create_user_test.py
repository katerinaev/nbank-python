import pytest, requests


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.debug
    def test_create_valid_user(self):
        response = requests.post(
            url='http://localhost:4111/api/v1/admin/users',
            json={
                'username': 'newuser75yct',
                'password': 'verysTRongPassword33$',
                'role': 'USER'
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Basic YWRtaW46YWRtaW4=',
            }
        )

        assert response.status_code == 201
        assert response.json().get('username') == 'newuser75yct'
        assert response.json().get('role') == 'USER'

    @pytest.mark.parametrize(
        argnames='username, password, role, error_key, error_value',
        argvalues=[
            ('', 'verysTRongPassword33$', 'USER', 'username', 'Username cannot be blank'),
            ('qwerty@', 'verysTRongPassword33$', 'USER', 'username', 'Username must contain only letters, digits, dashes, underscores, and dots'),
            ('ab', 'verysTRongPassword33$', 'USER', 'username', 'Username must be between 3 and 15 characters'),
            ('abababababababab', 'verysTRongPassword33$', 'USER', 'username', 'Username must be between 3 and 15 characters'),
        ]
    )
    def test_create_invalid_user(self, username: str, password: str, role: str, error_key:str, error_value: str):
        response = requests.post(
            url='http://localhost:4111/api/v1/admin/users',
            json={
                "username": username,
                "password": password,
                "role": role
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Basic YWRtaW46YWRtaW4=',
            }
        )
        # {'username': ['Username must be between 3 and 15 characters', 'Username must contain only letters, digits, dashes, underscores, and dots', 'Username cannot be blank']}
        assert response.status_code == 400
        assert error_value in response.json().get(error_key)