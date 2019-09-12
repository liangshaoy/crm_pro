from django import forms
from crmweb import models
from rbac.models import UserInfo
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# 注册form认证
class RegForm(forms.Form):
    username = forms.CharField(
        label = "用户名",
        max_length=18,
        error_messages={
            "required":"内容不能为空",
            "invalid":"格式错误",
            "max_length":"用户名最长不超过18位"
        },
        widget=forms.TextInput(attrs={"class":"forms-control"})
    )

    password = forms.CharField(
        min_length=6,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "min_length": "密码不能少于6位"
        }
    )

    r_password = forms.CharField(
        min_length=6,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "min_length": "密码不能少于6位"
        }
    )

    email = forms.CharField(
        label="邮箱",
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
        },
        validators=[RegexValidator(r"^\w+@\w+\.com$", "邮箱格式不正确")]
    )

    phone = forms.CharField(
        label="电话",
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
        },
        validators=[RegexValidator(r"^[0-9]{4,11}$","请输入正确的号码")]
    )



    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password.isdecimal():
            raise ValidationError("密码不能为纯数字！")
        return password

    def clean_r_password(self):
        r_password = self.cleaned_data.get("r_password")
        if r_password.isdecimal():
            raise ValidationError("密码不能为纯数字！")
        return r_password

    def clean(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("r_password"):
            self.add_error("r_password","两次密码输入不一致！")
        else:
            return self.cleaned_data


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"forms-control"})


# 修改密码form认证
class ChangeForm(forms.Form):
    """更改密码的form"""
    password = forms.CharField(
        label="原始密码",
        min_length=6,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "min_length": "密码不能少于6位"
        },
        widget=forms.TextInput()
    )
    new_password = forms.CharField(
        label="新密码",
        min_length=6,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "min_length": "密码不能少于6位"
        },
        widget=forms.PasswordInput()
    )

    r_new_password = forms.CharField(
        label="确认新密码",
        min_length=6,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "min_length": "密码不能少于6位"
        },
        widget=forms.PasswordInput()
    )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"forms-control"})


# 顾客添加form认证
class CustomerAddMF(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            if field != "course":
                self.fields[field].widget.attrs.update({"class":"forms-control",})


# 客户跟进信息form认证
class ConsultRecodeAddMF(forms.ModelForm):
    """客户跟进记录表"""
    class Meta:
        model = models.ConsultRecord
        fields = "__all__"
        exclude = ["delete_status",]

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 过滤数据展示时，客户选项中只展示当前用户的客户
        self.fields["customer"].queryset = models.Customer.objects.filter(consultant=request.user)

        # 过滤数据展示时，跟进人只显示当前销售的名称
        self.fields["consultant"].queryset = UserInfo.objects.filter(pk=request.user.id)

        for key,field in self.fields.items():
            self.fields[key].widget.attrs.update({"class":"forms-control",})