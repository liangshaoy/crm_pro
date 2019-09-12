import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AliCRM.settings")  # 引入django的环境
    import django
    django.setup()
    from rbac import models


    # 初始化用户数据
    # models.UserInfo.objects.create_superuser(
    #     username = "ryxiong",
    #     password = "ryxiong520",
    #     gender=1,
    #     phone="17788979651",
    #     email="275310126@qq.com",
    # )
    # models.UserInfo.objects.create_user(
    #     username="alex",
    #     password="alex123",
    #     gender=1,
    #     phone="1245638792",
    #     email="alex@qq.com",
    # )
    # models.UserInfo.objects.create_user(
    #     username="chao",
    #     password="chao123",
    #     gender=2,
    #     phone="14236587952",
    #     email="chao@163.com",
    # )
    # models.UserInfo.objects.create_user(
    #     username="jinjin",
    #     password="jinjin123",
    #     gender=2,
    #     phone="1475869231",
    #     email="jinjin@qq.com",
    # )
    # models.UserInfo.objects.create_user(
    #     username="baozhu",
    #     password="baozhu123",
    #     gender=2,
    #     phone="1385454667",
    #     email="baozhu@qq.com",
    # )


    # 初始化菜单数据
    # models.Menu.objects.create(
    #     title="主页",
    #     icon="fa fa-home"
    # )
    # models.Menu.objects.create(
    #     title="客户信息展示",
    #     icon="fa fa-connectdevelop"
    # )
    # models.Menu.objects.create(
    #     title="客户数据分析",
    #     icon="fa fa-pie-chart"
    # )
    # models.Menu.objects.create(
    #     title="客户跟进信息",
    #     icon="fa fa-info"
    # )
    # models.Menu.objects.create(
    #     title="报名信息展示",
    #     icon="fa fa-table"
    # )


    # 初始化权限表
    # models.Permission.objects.create(
    #     name="主页",
    #     url="/crmweb/index/",
    # )
    # models.Permission.objects.create(
    #     name="公户信息展示",
    #     url="/crmweb/customer/common/",
    # )
    # models.Permission.objects.create(
    #     name="私户信息展示",
    #     url="/crmweb/customer/private/",
    # )
    # models.Permission.objects.create(
    #     name="客户数据添加",
    #     url="/crmweb/customer/add/",
    # )
    # models.Permission.objects.create(
    #     name="客户信息编辑",
    #     url="/crmweb/customer/edit/(\d+)/",
    # )
    # models.Permission.objects.create(
    #     name="客户信息删除",
    #     url="/crmweb/customer/del/(\d+)/",
    # )
    # models.Permission.objects.create(
    #     name="课程咨询分析",
    #     url="/crmweb/customer/charts/1/",
    # )
    # models.Permission.objects.create(
    #     name="课程来源分析",
    #     url="/crmweb/customer/charts/2/",
    # )
    # models.Permission.objects.create(
    #     name="客户流量分析",
    #     url="/crmweb/customer/charts/3/",
    # )
    # models.Permission.objects.create(
    #     name="报名信息展示",
    #     url="/crmweb/enrollment/list/",
    # )
    # models.Permission.objects.create(
    #     name="客户跟进信息",
    #     url="/crmweb/consult/record/",
    # )

    # 初始化用户身份表
    models.Identity.objects.create()

