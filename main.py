from riteq import Riteq
from util import Util
import datetime

STATIC_REQUESTS = ['shift', 'org']
DYNAMIC_REQUESTS = ['pay_rule']
REQUESTS = [STATIC_REQUESTS, DYNAMIC_REQUESTS]

class main:

    def main(self):
        api = Riteq()
        util = Util()
        token = api.get_token()

        # need some confirmation
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=13)

        for request_type in REQUESTS:
            for request in request_type:
                if request_type == REQUESTS[0]:
                    url = api.get_request_url(request, start_date, end_date)
                    data = api.get_data(token, url)
                    util.write_csv(request, data)
                else:
                    pay_data = []
                    if request == 'pay_rule':
                        pay_rules = util.get_pay_rules()

                        for pay_id in pay_rules:
                            url = api.get_request_url(request, pay_id=pay_id)
                            data = api.get_data(token, url)
                            pay_data.extend(data)
                        util.write_csv(request, pay_data)



if __name__ == '__main__':
    main = main()
    main.main()