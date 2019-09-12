from django import views
from django.shortcuts import (
    render,reverse,redirect,HttpResponse
)
from rbac import models

class PermissionDistribute(views.View):

    def get(self,request):
        uid = request.GET.get('uid')
        user = models.UserInfo.objects.filter(id=uid)
        rid = request.GET.get('rid')

        # 获取所有用户
        all_user = models.UserInfo.objects.all()
        # 获取所有角色
        all_role = models.Role.objects.all()

        # 获取所有权限
        all_permission = models.Permission.objects.all().order_by("pk")
        if uid:  # 如果用户选中了用户id
            all_role_list = models.UserInfo.objects.get(pk=uid).role.values_list("pk")
            all_role_list = [i[0] for i in all_role_list]  # 转换成列表
            if rid:
                # 如果选中了角色，查找该角色的所有权限
                all_permission_list = models.Role.objects.filter(pk=rid).values_list("permission__pk")
            else:
                # 如果没有选中角色，就查找该用户的所有角色的所有权限，并去重
                all_permission_list = models.UserInfo.objects.get(pk=uid).role.values_list("permission__pk").distinct()
            all_permission_list = [i[0] for i in all_permission_list]  # 转换为列表
        else:
            if rid:
                all_permission_list = models.Role.objects.filter(pk=rid).values_list("permission__pk")
                all_permission_list = [i[0] for i in all_permission_list]  # 转换为列表

        return render(request,"permission_distribute.html",locals())

    def post(self,request):
        uid = request.GET.get('uid')
        user = models.UserInfo.objects.filter(id=uid)
        rid = request.GET.get('rid')

        postType = request.POST.get("postType")
        if postType == "role":
            role_list = request.POST.getlist("role_id")
            user.first().role.set(role_list)

        if postType == "permission":
            permission_list = request.POST.getlist("permission_id")
            print(permission_list)
            models.Role.objects.filter(pk=rid).first().permission.set(permission_list)

        url = reverse("distribute") + f"?uid={uid}&rid={rid}"
        return redirect(url)
