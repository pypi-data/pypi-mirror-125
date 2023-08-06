"""用于批量自动生成用户信息"""


import codecs
import csv
from time import time
from time import localtime
from faker import Faker


class PersonInfo(object):
    def __init__(self, IDCard):
        self.year = int(IDCard[6:10])
        self.month = int(IDCard[10:12])
        self.day = int(IDCard[12:14])
        self.sex = int(IDCard[16])

    def get_birth(self):
        birthday = "%4d/%02d/%02d" % (self.year, self.month, self.day)
        return birthday

    def get_age(self):
        cur_year = int(localtime()[0])
        age = cur_year - self.year
        return age

    def get_sex(self):
        if self.sex % 2 == 0:
            s = "女"
            return s
        else:
            s = "男"
            return s


def save_data_csv(maxdata_int, userpwd_str, spacal_char, pwd_len):
    with open("./person_info.csv",  "w", newline="") as f:
        fwrite = csv.writer(f)
        faker_cn = Faker(locale="zh_CN")
        faker_us = Faker(locale="en_US")

        for i in range(maxdata_int):
            IDCard = faker_cn.ssn()
            pi = PersonInfo(IDCard)
            # 姓名
            name = faker_cn.name()
            # 出生年月日
            birthday = pi.get_birth()
            # 年龄
            age = pi.get_age()
            # 性别
            sex = pi.get_sex()
            # 电话
            phone = faker_cn.phone_number()
            # 住址
            address = faker_cn.address()
            # 用户昵称
            username = faker_us.name()
            if userpwd_str == 'y' :
                if spacal_char == 'y':
                    # 用户密码(长度，特殊字符，数字，大写字母，小写字母)
                    userpwd = faker_us.password(length=pwd_len, special_chars=True, digits=True, upper_case=True,
                                                lower_case=True)
                elif spacal_char == 'n':
                    # 用户密码(长度，特殊字符，数字，大写字母，小写字母)
                    userpwd = faker_us.password(length=pwd_len, special_chars=False, digits=True, upper_case=True,
                                                lower_case=True)

                fwrite.writerow([name, IDCard, birthday, age, sex, phone, address, username, userpwd])
            else:
                fwrite.writerow([name, IDCard, birthday, age, sex, phone, address, username])


if __name__ == '__main__':
    maxdata_int = int(input("请输入需要生成的数剧量："))
    userpwd_str = input("是否生成用户密码？(y/n)")
    if userpwd_str == 'y':
        spacal_char = input("密码是否包含特殊字符？(y/n)")
        userpwd_len_int = int(input("请输入密码长度(len>=4)"))
        save_data_csv(maxdata_int, userpwd_str,  spacal_char, userpwd_len_int)
    else:
        save_data_csv(maxdata_int, userpwd_str, spacal_char, 0)
