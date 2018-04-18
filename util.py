import csv


class Util:
    pay_rules = []
    employee_list = []
    skills_list = []
    org_list = []
    def write_csv(self, file_name, json_r):
        with open(file_name + '.csv', 'wb') as csvfile:
            csvout = csv.writer(csvfile)
            if file_name == 'shift':
                self.write_shift_data(json_r, csvout)

            elif file_name == 'org':
                self.write_org_data(json_r, csvout)

            elif file_name == 'pay_rule':
                self.write_pay_rule_data(json_r, csvout)

            elif file_name == 'employee':
                self.write_emp_data(json_r, csvout)

            elif file_name == 'skill':
                self.write_skill_data(json_r, csvout)


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

            if shifts['EmployeeId'] not in self.employee_list:
                self.employee_list.append(shifts['EmployeeId'])

            data = [shifts['Id'], shifts['EmployeeId'], shifts['ScheduledShiftId'],
                    shifts['StartTime'], shifts['EndTime'],
                    break_start, break_end,
                    shifts['PayRuleId'], org_id]
            csvout.writerow(data)

    def write_org_data(self, json_r, csvout):
        col_titles = ["Org Id", "Name", "Parent Id", "Group Id", "Role Id", "Stencil Id"]
        csvout.writerow(col_titles)

        for org in json_r:
            validate_data = self.check_attr_exists(org, 'RoleId', 'StencilId', 'GroupId')
            role_id = validate_data['RoleId'] if 'RoleId' in validate_data else None
            stencil_id = validate_data['StencilId'] if 'StencilId' in validate_data else None
            group_id = validate_data['GroupId'] if 'GroupId' in validate_data else None

            data = [org['Id'], org['Name'], org['ParentId'], group_id, role_id, stencil_id]
            self.org_list.append(data)
            csvout.writerow(data)

    def write_pay_rule_data(self, json_r, csvout):
        col_titles = ["Pay Id", "Name", "Pay Rule Group Id"]
        csvout.writerow(col_titles)

        for pay_rule in json_r:
            data = [pay_rule['Id'], pay_rule['Name'], pay_rule['PayRuleGroupId']]
            csvout.writerow(data)

    def write_emp_data(self, json_r, csvout):
        col_titles = ["Id", "First Name", "Last Name", "Export Code", "Skill Id"]
        csvout.writerow(col_titles)

        for emp in json_r:
            skills = None
            if self.check_dict_exists(emp, 'Skills'):
                skills = emp['Skills'][0]['SkillId']
                if skills not in self.skills_list:
                    self.skills_list.append(skills)
            data = [emp['Id'], emp['FirstName'], emp['LastName'],
                    emp['ExportCode']['ExportCode'], skills]
            csvout.writerow(data)

    def write_skill_data(self, json_r, csvout):
        col_titles = ["Id", "Short Name"]
        csvout.writerow(col_titles)

        for skills in json_r:
            data = [skills["Id"], skills["ShortName"]]
            csvout.writerow(data)

    def get_org_chain(self, org_id, org_string):
        if org_id == 0:
            return org_string[:-1]
        else:
            parent = [org for org in self.org_list if org_id == org[0]]
            return self.get_org_chain(parent[0][2], org_string + str(parent[0][1]) + "/")

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

    def get_emp_list(self):
        return self.employee_list

    def get_skills_list(self):
        return self.skills_list
