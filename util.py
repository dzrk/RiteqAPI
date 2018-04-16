import csv


class Util:
    pay_rules = []

    def write_csv(self, file_name, json_r):
        with open(file_name + '.csv', 'wb') as csvfile:
            csvout = csv.writer(csvfile)
            if file_name == 'shift':
                self.write_shift_data(json_r, csvout)
            elif file_name == 'org':
                self.write_org_data(json_r, csvout)
            elif file_name == 'pay_rule':
                self.write_pay_rule_data(json_r, csvout)

    def write_shift_data(self, json_r, csvout):
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

            if shifts['PayRuleId'] not in self.pay_rules:
                self.pay_rules.append(shifts['PayRuleId'])

            data = [shifts['Id'], shifts['EmployeeId'], shifts['ScheduledShiftId'],
                    shifts['StartTime'], shifts['EndTime'],
                    break_start, break_end,
                    shifts['PayRuleId'], org_id]
            csvout.writerow(data)

    def write_org_data(self, json_r, csvout):
        col_titles = ["Org Id", "Name", "Parent Id", "Group Id", "Role Id", "Stencil Id"]
        csvout.writerow(col_titles)

        for orgs in json_r:
            validate_data = self.check_attr_exists(orgs, 'RoleId', 'StencilId', 'GroupId')
            role_id = validate_data['RoleId'] if 'RoleId' in validate_data else None
            stencil_id = validate_data['StencilId'] if 'StencilId' in validate_data else None
            group_id = validate_data['GroupId'] if 'GroupId' in validate_data else None

            data = [orgs['Id'], orgs['Name'], orgs['ParentId'], group_id, role_id, stencil_id]
            csvout.writerow(data)

    def write_pay_rule_data(self, json_r, csvout):
        col_titles = ["Pay Id", "Name", "Pay Rule Group Id"]
        csvout.writerow(col_titles)

        for pay_rule in json_r:
            data = [pay_rule['Id'], pay_rule['Name'], pay_rule['PayRuleGroupId']]
            csvout.writerow(data)

    def check_dict_exists(self, obj, key):
        return len(obj[key]) > 0

    def check_attr_exists(self, obj, *attr):
        data = {}
        for args in attr:
            if args in obj:
                data[args] = obj[args]
        return data

    def get_pay_rules(self):
        return self.pay_rules