import requests
import json
import requests
import config as config

class Riteq:

    def get_token(self):
        url = config.BASE_URL + "token"
        params = {
            "username": config.USER,
            "password": config.PASS,
            "grant_type": "password"
        }
        post_r = requests.post(url, params)
        response = json.loads(post_r.text)

        return response['access_token']

    def get_data(self, token, url):
        headers = {"Authorization": "Bearer " + token}
        get_request = requests.get(url, headers=headers)

        return json.loads(get_request.text)

    def get_request_url(self, request_type, start_date, end_date):
        return {
            'shift': config.BASE_URL + "Shift?startTime=" +
                     start_date.strftime('%Y-%m-%d') + "&endTime=" +
                     end_date.strftime('%Y-%m-%d')
        }[request_type]