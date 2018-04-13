import csv

class Util:
    def write_csv(self, file_name, json_r):
        with open(file_name + '.csv','wb') as csvfile:
            if file_name == 'shift':
                self.write_shift_data(json_r, csvfile)

    def write_shift_data(self, json_r, csvfile):
        csvout = csv.writer(csvfile)
        col_titles = ["Id", "Employee Id", "Scheduled Shift Id", "Start Time - Shift", "End Time - Shift",
                      "Start Time - Break", "End Time - Break", "Pay Rule ID", "Org Id - Sub Shift"]
        csvout.writerow(col_titles)
        for shifts in json_r:

            break_start, break_end, org_id = [None]*3
            if self.check_dict_exists(shifts, 'Breaks'):
                break_start = shifts['Breaks'][0]['StartTime']
                break_end = shifts['Breaks'][0]['EndTime']
            if self.check_dict_exists(shifts, 'SubShifts'):
                org_id = shifts['SubShifts'][0]['OrgId']

            data = [shifts['Id'], shifts['EmployeeId'], shifts['ScheduledShiftId'],
                    shifts['StartTime'], shifts['EndTime'],
                    break_start, break_end,
                    shifts['PayRuleId'], org_id]
            csvout.writerow(data)

    def check_dict_exists(self, obj, key):
        return len(obj[key]) > 0
