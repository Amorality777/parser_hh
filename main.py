import requests


class HHApi:
    access_token = None
    refresh_token = None
    expires_in = None
    base_url = 'api.hh.ru'
    token_url = 'hh.ru/oauth/token'

    def get_token(self):
        params = {
            'grant_type': 'authorization_code',
            'client_id': '101404183',
            'client_secret': '',
            'code': '',
        }
        res = requests.post(self.token_url, params=params)
        if res.status_code == 200:
            self.save_token(res.json())

    def get_refresh_token(self):
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': 'refresh_token',
        }
        res = requests.post(self.token_url, params=params)
        if res.status_code == 200:
            self.save_token(res.json())

    def save_token(self, json):
        self.access_token = json['access_token']
        self.refresh_token = json['refresh_token']
        self.expires_in = json['expires_in']

    def get_vacancies(self):
        url = '/vacancies'
        params = {
            'type': 'json',
            'text': 'json',
            'search_field': '',
            'vacancy_label': '',
            'employment': 'json',
        }


if __name__ == '__main__':
    api = HHApi()
    api.get_token()
