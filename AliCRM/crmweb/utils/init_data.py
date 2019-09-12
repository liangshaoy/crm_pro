import os
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AliCRM.settings")
    import django
    django.setup()
    import random
    import string
    from crmweb import models

    # # 初始化客户数据
    # data_list = []
    # for i in range(1,2001):
    #     customer = models.Customer(
    #         qq=''.join(random.choices(string.digits,k=9)),
    #         qq_name="熊%s"%random.sample(range(1,2001),k=2000)[i-1],
    #         gender=random.choice(("male","female")),
    #         birthday=f"199{random.choice(range(0,9))}-{random.choice(range(1,13))}-{random.choice(range(1,29))}",
    #         phone="".join(random.choices(string.digits,k=9)),
    #         source=random.choice(("qq","referral","website","baidu_ads","WoM","public_class","website_luffy","others","office_direct")),
    #         course=random.choice(("Linux","PythonFullStack","BigData")),
    #         class_type=random.choice(("fulltime","online","weekend")),
    #         customer_note="".join(random.choices(string.ascii_letters,k=15)),
    #         date=f"2019-{random.choice(range(1,13))}-{random.choice(range(1,29))} {random.choice(range(8,16))}:{random.choice(range(1,60))}",
    #     )
    #     data_list.append(customer)
    #
    # models.Customer.objects.bulk_create(data_list)
    #
    #
    #
    # # 初始化校区
    # models.Campuses.objects.create(
    #     name="北京沙河校区",
    #     address="北京市昌平区沙河镇汇德商厦",
    # )
    # models.Campuses.objects.create(
    #     name="上海浦东校区",
    #     address="上海市浦东新区康桥东路",
    # )
    # models.Campuses.objects.create(
    #     name="深圳大学城校区",
    #     address="深圳市南山区西丽大学城",
    # )
    #
    #
    # # 初始化班级数据
    # models.ClassList.objects.create(
    #     course="Linux",
    #     semester=25,
    #     campuses_id=2,
    #     price=15800,
    #     memo="linux运维",
    #     start_date="2019-3-27",
    #     graduate_date="2019-9-27",
    # )
    # models.ClassList.objects.create(
    #     course="PythonFullStack",
    #     semester=20,
    #     campuses_id=1,
    #     price=20000,
    #     memo="python全栈开发",
    #     start_date="2019-2-27",
    #     graduate_date="2019-8-27",
    # )
    # models.ClassList.objects.create(
    #     course="BigData",
    #     semester=6,
    #     campuses_id=3,
    #     price=22000,
    #     memo="大数据开发",
    #     start_date="2019-5-27",
    #     graduate_date="2019-11-27",
    # )
    #
    #
    # # 初始化班级老师表
    # class1 = models.ClassList.objects.get(id=1)
    # class2 = models.ClassList.objects.get(id=2)
    # class3 = models.ClassList.objects.get(id=3)
    # class1.teachers.add(2)
    # class2.teachers.add(3)
    # class3.teachers.add(2)
    #
    #
    #
    # # 初始化报名表数据
    #
    # data = []
    # customer_list = random.sample(list(models.Customer.objects.all()),k=20)
    # class_list = list(models.ClassList.objects.all())
    # # print(class_list)
    # for customer_obj in customer_list:
    #     for class_obj in class_list:
    #         data.append((customer_obj,class_obj))
    # # print(data)
    #
    # enrollment_list = []
    # for i in range(len(data)):
    #     obj = models.Enrollment(
    #         customer_id=data[i][0].id,
    #         why=random.choice(["美女多","被忽悠了","不知道还有哪","帅哥多"]),
    #         expectation=random.choice(["月入百万","美女相伴","赢取白富美","走向人生巅峰"]),
    #         enrolled_date=f"2019-{random.choice(range(1, 13))}-{random.choice(range(1, 29))} {random.choice(range(8, 16))}:{random.choice(range(1, 60))}",
    #         school_id = data[i][1].campuses.id,
    #         enrollment_class_id = data[i][1].id,
    #     )
    #     enrollment_list.append(obj)
    # models.Enrollment.objects.bulk_create(enrollment_list)
    #
    #
    # # 更改已经报名的顾客在顾客表中的状态
    # enrolled_customers = models.Enrollment.objects.values_list("customer").distinct()
    # for enrolled_customer in enrolled_customers:
    #     models.Customer.objects.filter(pk=enrolled_customer[0]).update(status="signed")














