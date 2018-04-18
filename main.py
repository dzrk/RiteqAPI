from riteq import Riteq
from util import Util
import datetime
#'shift', 'org'
STATIC_REQUESTS = ['shift']
DYNAMIC_REQUESTS = ['pay_rule','employee', 'skill']
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



if __name__ == '__main__':
    main = main()
    main.main()