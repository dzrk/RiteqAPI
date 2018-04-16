from riteq import Riteq
from util import Util
import datetime

REQUESTS = ['org']


class main:

    def main(self):
        api = Riteq()
        util = Util()
        token = api.get_token()

        # need some confirmation
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=13)

        for request_type in REQUESTS:
            url = api.get_request_url(request_type, start_date, end_date)
            data = api.get_data(token, url)
            util.write_csv(request_type,data)

if __name__ == '__main__':
    main = main()
    main.main()