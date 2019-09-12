import re
from django import template

register = template.Library()  # register名字是固定的，不能改变


@register.inclusion_tag("menu.html")
def get_menu(request):
    """
    自定义生成菜单标签，根据session中的menus_list数据结构（列表套字典套）
    :param request: request请求
    :return: 返回menus_list
    """
    menus_list = request.session.get("menus_list")

    for menu in menus_list:
        if menu["url"] == request.path:
            menu["class"] = "active"
        else:
            if menu.get("children"):
                for child in menu["children"]:
                    if re.match(child["url"],request.path) or request.show_id == child["pk"]:
                        menu["class"] = "active"
                        child["class"] = "active"

    return {"menus_list": menus_list}


@register.filter
def has_permission(url,request):
    """
    分配不是菜单的按钮的权限
    :param url: 某个按钮的url
    :param request: request请求
    :return: 如果有该权限，返回True，否则返回False
    """
    permissions_list = request.session.get("permissions_list")
    for permission in permissions_list:
        reg = f"^{permission['url']}"
        if re.search(reg,url):
            return True
    return False

@register.simple_tag
def get_role_url(request,rid):
    params = request.GET.copy()  # 调用querydict的copy方法
    params._mutable = True  # 改变querydict的可变属性为True
    params["rid"] = rid  # 给querydict赋值一个键值对
    return params.urlencode()  # 使用urlencode解码为 uid=1的形式字符串