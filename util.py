import csv

class Util:
    def write_csv(self, file_name, json_r):
        with open(file_name + '.csv','wb') as csvfile:
            csvout = csv.writer(csvfile)
            col_titles = ["Id", "Employee Id", "Scheduled Shift Id", "Start Time - Shift", "End Time - Shift",
                          "Start Time - Break", "End Time - Break", "Pay Rule ID", "Org Id - Sub Shift"]

            csvout.writerow(col_titles)
            for shifts in json_r:
                break_start = shifts['Breaks'][0]['StartTime'] if len(shifts['Breaks']) > 0 else None
                break_end = shifts['Breaks'][0]['EndTime'] if len(shifts['Breaks']) > 0 else None
                org_id = shifts['SubShifts'][0]['OrgId'] if len(shifts['SubShifts']) > 0 else None

                data = [shifts['Id'], shifts['EmployeeId'], shifts['ScheduledShiftId'],
                        shifts['StartTime'], shifts['EndTime'],
                        break_start, break_end,
                        shifts['PayRuleId'], org_id]
                csvout.writerow(data)