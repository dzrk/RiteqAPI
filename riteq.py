import requests
import json
import requests
import config as config

class Riteq:

    def get_token(self):
        # gets token via password
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
        # asks for data with token auth
        headers = {"Authorization": "Bearer " + token}
        get_request = requests.get(url, headers=headers)
        return json.loads(get_request.text)

    def get_request_url(self, request_type, start_date=None, end_date=None, pay_id=None):
        # additional request types can be added in this switch-case
        if pay_id == None:
            return {
                'shift': config.BASE_URL + "Shift?startTime=" +
                         start_date.strftime('%Y-%m-%d') + "&endTime=" +
                         end_date.strftime('%Y-%m-%d'),
                'org': config.BASE_URL + "Organization",
            }[request_type]
        else:
            return {
                'pay_rule': config.BASE_URL + "PayRule/" + str(pay_id)
            }[request_type]
