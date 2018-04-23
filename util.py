import csv
from datetime import datetime

class Util:

    pay_rule_list = []
    pay_rule_id = []
    employee_list = []
    employee_id = []
    skills_list = []
    skills_id = []
    org_list = []
    shift_type_id = []
    shift_type_list = []
    shift_list = []
    pay_rule_group_id = []
    pay_rule_group_list = []
    pay_rate_group_id = []
    pay_rate_group_list = []
    pay_rate_id = []
    pay_rate_list = []

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

            elif file_name == 'skill' or file_name == 'shift_type':
                self.write_skill_shift_data(json_r, csvout)

            elif file_name == 'pay_rule_group':
                self.write_pay_rule_group(json_r, csvout)

            elif file_name == 'pay_rate_group':
                self.write_pay_rate_group(json_r, csvout)

            elif file_name == 'pay_rate':
                self.write_pay_rate(json_r, csvout)




    def write_shift_data(self, json_r, csvout):
        col_titles = ["Shift Id", "Employee Id", "Scheduled Shift Id", "Start Time - Shift", "End Time - Shift",
                         "Total Shift Hours", "Start Time - Break", "End Time - Break", "Total Break Hours",
                         "Pay Rule ID", "Org Id - Sub Shift", "Shift Type Id"]
        csvout.writerow(col_titles)
        for shifts in json_r:
            break_start, break_end, org_id, shift_type_id, break_total, hours_total = [None]*6
            if self.check_dict_exists(shifts, 'Breaks'):
                break_start = shifts['Breaks'][0]['StartTime']
                break_end = shifts['Breaks'][0]['EndTime']
                break_total = self.difference_in_time(break_start, break_end)

            if self.check_dict_exists(shifts, 'SubShifts'):
                org_id = shifts['SubShifts'][0]['OrgId']
                shift_type_id = shifts['SubShifts'][0]['TypeId']
                if shifts['SubShifts'][0]['TypeId'] not in self.shift_type_id:
                    self.shift_type_id.append(shifts['SubShifts'][0]['TypeId'])

            if shifts['PayRuleId'] not in self.pay_rule_id:
                self.pay_rule_id.append(shifts['PayRuleId'])

            if shifts['EmployeeId'] not in self.employee_id:
                self.employee_id.append(shifts['EmployeeId'])

            if self.check_dict_exists(shifts, 'EndTime'):
                hours_total = self.difference_in_time(shifts['StartTime'], shifts['EndTime'])

            data = [shifts['Id'], shifts['EmployeeId'], shifts['ScheduledShiftId'],
                    shifts['StartTime'], shifts['EndTime'], hours_total,
                    break_start, break_end, break_total,
                    shifts['PayRuleId'], org_id, shift_type_id]
            self.shift_list.append(data)
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
            if pay_rule['PayRuleGroupId'] not in self.pay_rule_group_id:
                self.pay_rule_group_list.append(pay_rule['PayRuleGroupId'])

            self.pay_rule_list.append(data)
            csvout.writerow(data)

    def write_emp_data(self, json_r, csvout):
        col_titles = ["Id", "First Name", "Last Name", "Export Code", "Skill Id", "Pay Rate Id"]
        csvout.writerow(col_titles)
        for emp in json_r:
            skills = None
            if self.check_dict_exists(emp, 'Skills'):
                skills = emp['Skills'][0]['SkillId']
                if skills not in self.skills_id:
                    self.skills_id.append(skills)
            if emp['Revisions'][-1]['OrganizationLevels'][-1]['PayRateId'] not in self.pay_rate_id:
                self.pay_rate_id.append(emp['Revisions'][-1]['OrganizationLevels'][-1]['PayRateId'])
            data = [emp['Id'], emp['FirstName'], emp['LastName'],
                    emp['ExportCode']['ExportCode'], skills, emp['Revisions'][-1]['OrganizationLevels'][-1]['PayRateId']]
            self.employee_list.append(data)
            csvout.writerow(data)

    def write_skill_shift_data(self, json_r, csvout):
        col_titles = ["Id", "Name"]
        csvout.writerow(col_titles)

        for skills in json_r:
            if len(skills) == 1:
                data = [skills[0]['Id'], skills[0]['Name']]
                self.shift_type_list.append(data)
            else:
                data = [skills['Id'], skills['Name']]
                self.skills_list.append(data)
            csvout.writerow(data)

    def write_pay_rule_group(self, json_r, csvout):
        col_titles = ["Id", "Name"]
        csvout.writerow(col_titles)

        for prg in json_r:
            data = [prg['Id'], prg['Name']]
            self.pay_rule_group_list.append(data)
            csvout.writerow(data)

    def write_pay_rate_group(self, json_r, csvout):
        col_titles = ["Id", "Name"]
        csvout.writerow(col_titles)

        for prg in json_r:
            data = [prg['Id'], prg['Name']]
            self.pay_rate_group_list.append(data)
            csvout.writerow(data)

    def write_pay_rate(self, json_r, csvout):
        col_titles = ["Id", "Name"]
        csvout.writerow(col_titles)

        for prg in json_r:
            data = [prg[-1]['Id'], prg[-1]['Name']]
            self.pay_rate_list.append(data)
            csvout.writerow(data)

    def get_org_chain(self, org_id, org_string):
        if org_id == 0:
            return org_string[:-1]
        else:
            parent = [org for org in self.org_list if org_id == org[0]]
            return self.get_org_chain(parent[0][2], org_string + str(parent[0][1]) + "/")

    def combine_all_data(self):
        with open('combined.csv', 'wb') as csvfile:
            csvout = csv.writer(csvfile)
            print("\nCompiling data...")
            col_title = ["Shift Id", "Employee Id", "Scheduled Shift Id", "Start Time - Shift", "End Time - Shift",
                         "Total Shift Hours", "Start Time - Break", "End Time - Break", "Total Break Hours",
                         "Pay Rule ID", "Org Id - Sub Shift", "Shift Type Id", "First Name", "Last Name",
                         "Export Code", "Skill Id", "Pay Rate Id", "Role", "Org", "Pay Name",
                         "Pay Rule Group Id", "Skill Name", " Shift Type", "Pay Rate"]
            csvout.writerow(col_title)
            for shift in self.shift_list:
                data = []
                employee = self.find_from_list(self.employee_list, shift[1])
                org = self.find_from_list(self.org_list, shift[10])
                pay = self.find_from_list(self.pay_rule_list, shift[-3])
                skill = self.find_from_list(self.skills_list, employee[-2]) if employee[-2] != None else []
                shift_type = self.find_from_list(self.shift_type_list, shift[-1])
                pay_rate = self.find_from_list(self.pay_rate_list, employee[-1])
                data.extend(shift + employee + [org[0]] + [self.get_org_chain(shift[-2], "")] + pay + skill
                            + shift_type + pay_rate)
                csvout.writerow(data)

    def check_dict_exists(self, obj, key):
        if obj[key] == None:
            return False
        return len(obj[key]) > 0

    def check_attr_exists(self, obj, *attr):
        data = {}
        for args in attr:
            if args in obj:
                data[args] = obj[args]
        return data

    def find_from_list(self, data, key): # looks inside lists to find the correct list id
        return [entry[1:] for entry in data if entry[0] == key][0]

    def difference_in_time(self, start, end):
        start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        return end - start

    def get_pay_rules(self):
        return self.pay_rule_id

    def get_emp_list(self):
        return self.employee_id

    def get_skills_list(self):
        return self.skills_id

    def get_shift_type_list(self):
        return self.shift_type_id

    def get_shift_list(self):
        return self.shift_list

    def get_pay_rate_list(self):
        return self.pay_rate_id
