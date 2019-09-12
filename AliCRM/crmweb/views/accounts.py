from django import views
from rbac import models
from django.contrib import auth
from crmweb.utils import authcode
from crmweb.forms import formAuth
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render, redirect, reverse, HttpResponse
)

from rbac.service.init_permission import init_permission  # 自定义权限注入函数


# create you views here

# 注册视图类
class Register(views.View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        data = request.POST
        form_obj = formAuth.RegForm(data)
        if form_obj.is_valid():  # 验证提交数据的合法性
            valid_data = form_obj.cleaned_data
            username = valid_data.get("username")
            # 判断帐号是否已存在
            if models.UserInfo.objects.filter(username=username):
                # 如果存在，给form中的username字段添加一个错误提示。
                form_obj.add_error("username", "帐号已存在")
                return render(request, "register.html", {"form_obj": form_obj})
            else:
                # 帐号可用，去掉多余密码，在数据库创建记录
                del valid_data["r_password"]
                models.UserInfo.objects.create_user(**valid_data)
                return redirect("login")
        else:
            # 数据验证不通过，返回页面和错误提示，保留数据
            return render(request, "register.html", {"form_obj": form_obj})


# 登录视图类
class Login(views.View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        data = request.POST
        authcode = data.get("authcode")
        username = data.get("username")
        password = data.get("password")
        if request.session.get("authcode").upper() != authcode.upper():
            return JsonResponse({"status": "1"})
        else:
            user = auth.authenticate(username=username, password=password)
            if user:
                # 将用户名存入session中
                request.session["user"] = username

                # 将用户的权限添加到session中
                init_permission(request,username)
                auth.login(request, user)  # 将用户信息添加到session中
                return JsonResponse({"status": "2"})
            else:
                return JsonResponse({"status": "3"})


# 验证码视图类
class GetAuthImg(views.View):
    """获取验证码视图类"""

    def get(self, request):
        data = authcode.get_authcode_img(request)
        print("验证码：",request.session.get("authcode"))
        return HttpResponse(data)


# 注销视图类
class Logout(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request):
        auth.logout(request)
        return redirect("login")


# 个人中心
class Profile(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request):
        username = request.user.username
        form_obj = formAuth.ChangeForm()
        user_info = models.UserInfo.objects.filter(username=username)[0]
        return render(request, "profile.html", {"user_info": user_info, "form_obj": form_obj})


# 修改密码
class ChangePwd(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def post(self, request):
        form_obj = formAuth.ChangeForm(request.POST)
        # print(request.POST)
        authcode = request.session.get("authcode")
        if request.POST.get("authcode").upper() == authcode.upper():
            if form_obj.is_valid():
                data = form_obj.cleaned_data
                password = data.get("password")
                new_password = data.get("new_password")
                r_new_password = data.get("r_new_password")
                if request.user.check_password(password):
                    if new_password == r_new_password:
                        request.user.set_password(new_password)
                        request.user.save()
                        return JsonResponse({"status": 1000, "info": reverse("login")})
                    else:
                        return JsonResponse({"status": 1001, "info": "两次密码输入不一致！"})
                else:
                    return JsonResponse({"status": 1002, "info": "密码输入错误！"})
            else:
                return JsonResponse({"status": 1003, "info": "输入内容有误！"})
        else:
            return JsonResponse({"status": 1004, "info": "验证码输入有误！"})
