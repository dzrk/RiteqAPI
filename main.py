from riteq import Riteq
from util import Util

STATIC_REQUESTS = ['shift','org','pay_rate_group','pay_rule_group']
DYNAMIC_REQUESTS = ['pay_rule','employee', 'skill', 'shift_type', 'pay_rate']
REQUESTS = [STATIC_REQUESTS, DYNAMIC_REQUESTS]

class main:

    def main(self):
        api = Riteq()
        util = Util()
        token = api.get_token()

        for request_type in REQUESTS:
            for request in request_type:
                if request_type == REQUESTS[0]:
                    url = api.get_request_url(request)
                    data = api.get_data(token, url)
                    util.write_csv(request, data)
                else:
                    pay_data = []
                    emp_data = []
                    skill_data = []
                    shift_data = []
                    pay_rate_data = []
                    if request == DYNAMIC_REQUESTS[0]:
                        pay_rules = util.get_pay_rules()

                        for pay_id in pay_rules:
                            url = api.get_request_url(request, pay_id=pay_id)
                            data = api.get_data(token, url)
                            pay_data.extend(data)
                        util.write_csv(request, pay_data)
                    elif request == DYNAMIC_REQUESTS[1]:
                        emp_list = util.get_emp_list()

                        for emp_id in emp_list:
                            url = api.get_request_url(request, emp_id=emp_id)
                            data = api.get_data(token, url)
                            emp_data.append(data)
                        util.write_csv(request, emp_data)
                    elif request == DYNAMIC_REQUESTS[2]:
                        skill_list = util.get_skills_list()

                        for skill_id in skill_list:
                            url = api.get_request_url(request, skill_id=skill_id)
                            data = api.get_data(token, url)
                            skill_data.append(data)
                        util.write_csv(request, skill_data)
                    elif request == DYNAMIC_REQUESTS[3]:
                        shift_list = util.get_shift_type_list()

                        for shift_id in shift_list:
                            url = api.get_request_url(request, shift_id=shift_id)
                            data = api.get_data(token, url)
                            shift_data.append(data)
                        util.write_csv(request, shift_data)
                    elif request == DYNAMIC_REQUESTS[4]:
                        pay_rate_list = util.get_pay_rate_list()

                        for pay_rate_id in pay_rate_list:
                            url = api.get_request_url(request, pay_rate_id=pay_rate_id)
                            data = api.get_data(token, url)
                            pay_rate_data.append(data)
                        util.write_csv(request, pay_rate_data)
        util.combine_all_data()

if __name__ == '__main__':
    main = main()
    main.main()