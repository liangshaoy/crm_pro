from crmweb.views import accounts, customers
from django.conf.urls import url

urlpatterns = [
    # 注册url
    url(r'^register/', accounts.Register.as_view(), name="register"),
    # 登录url
    url(r"^login/", accounts.Login.as_view(), name="login"),
    # 验证码url
    url(r'^get_auth_img/', accounts.GetAuthImg.as_view(), name="get_auth_img"),
    # 注销url
    url(r'^logout/', accounts.Logout.as_view(), name="logout"),
    # 个人中心url
    url(r'^profile/', accounts.Profile.as_view(), name="profile"),
    # 修改密码url
    url(r'^change_pwd/', accounts.ChangePwd.as_view(), name="change_pwd"),
    # 主页url
    url(r'^index/', customers.Index.as_view(), name="index"),


    # 公户数据url
    url(r'^customer/common/list/', customers.CommonData.as_view(), name="common"),
    # 公户信息添加url
    url(r'^customer/common/add/', customers.CustomerAdd.as_view(), name="customer_common_add"),
    # 公户信息编辑url
    url(r'^customer/common/edit/(\d+)/', customers.CustomerEdit.as_view(), name="customer_common_edit"),
    # 公户信息删除url
    url(r'^customer/common/del/(\d+)/', customers.CustomerDel.as_view(), name="customer_common_del"),


    # 私户数据url
    url(r'^customer/private/list/', customers.CommonData.as_view(), name="private"),  # 使用公户url展示
    # 私户信息添加url
    url(r'^customer/add/', customers.CustomerAdd.as_view(), name="add_customer"),
    # 私户信息编辑url
    url(r'^customer/edit/(\d+)/', customers.CustomerEdit.as_view(), name="edit_customer"),
    # 私户信息删除url
    url(r'^customer/del/(\d+)/', customers.CustomerDel.as_view(), name="del_customer"),


    # 客户数据分析url
    url(r'^customer/charts/(\d+)/', customers.ChartsCustomer.as_view(), name="charts_customer"),

    # 客户跟进数据url
    url(r'^consult/record/list/(\d+)?/?$', customers.ConsultRecord.as_view(), name="consult_record_list"),
    # 客户跟进信息添加url
    url(r'^consult/record/add/', customers.ConsultRecordAddEdit.as_view(), name="consult_record_add"),
    # 客户跟进信息编辑url
    url(r'^consult/record/edit/(\d+)/', customers.ConsultRecordAddEdit.as_view(), name="consult_record_edit"),
    # 客户跟进信息删除url
    url(r'^consult/record/del/(\d+)/', customers.ConsultRecordDel.as_view(), name="consult_record_del"),


    # 报名客户信息展示
    url(r'^enrollment/list/', customers.Enrollment.as_view(), name="enrollment"),
    # 测试路径
    url(r'^test/', customers.Test.as_view(), name="test"),
    # charts图表测试
    url(r'^charts/test', customers.chartstest, name="chartstest"),

]
