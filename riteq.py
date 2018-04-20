import json
import requests
import config as config
import datetime

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

    def get_request_url(self, request_type, pay_id=None, emp_id=None, skill_id=None, shift_id=None):
        # additional request types can be added in this pseudo switch-case
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)
        return {
            'shift': config.BASE_URL + "Shift?startTime=" +
                     start_date.strftime('%Y-%m-%d') + "&endTime=" +
                     end_date.strftime('%Y-%m-%d'),
            'org': config.BASE_URL + "Organization",
            'pay_rule': config.BASE_URL + "PayRule/" + str(pay_id),
            'employee': config.BASE_URL + "Employee/" + str(emp_id),
            'skill': config.BASE_URL + "Skill/" + str(skill_id),
            'shift_type': config.BASE_URL + "ShiftType/" + str(shift_id)
        }[request_type]

