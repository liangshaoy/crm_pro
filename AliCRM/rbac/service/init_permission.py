from rbac import models


def init_permission(request, user):
    """
    在登录函数验证通过后，在session中注入用户权限和用户菜单权限。
    :param request: 用户登录请求时的wsgi请求对象
    :param user: 用户登录验证通过后的用户账号名
    :return: none，
    """
    permissions = models.Permission.objects.filter(role__userinfo__username=user).values("pk", "name", "url","show", "icon", "parent_id", "priority").distinct()

    permissions_list = []  # 定义权限列表
    menus_list = []  # 定义菜单列表

    print("当前用户权限>>>")
    for permission in permissions:  # 遍历权限列表

        # 获取用户权限的数据结构，列表套字典，一个字典代表一个权限
        permissions_list.append({
            "pk": permission["pk"],
            "name": permission["name"],
            "url": permission["url"],
            "parent_id": permission["parent_id"],
        })
        print(permission["name"].center(8," "),":",permission["url"])

        # 获取菜单权限的数据结构，列表套字典，一个字典代表一个菜单
        if not permission["parent_id"] and permission["show"]:
            menu_dict = {
                "name": permission["name"],
                "url": permission["url"],
                "icon": permission["icon"],
                "parent_id": permission["parent_id"],
                "children": []  # 定义一个父级菜单包含所有儿子菜单的空列表
            }
            menus_list.append(menu_dict)  # 添加到列表

            children = models.Permission.objects.filter(parent_id=permission["pk"])  # 自关联一对多的基于对象的反向查询
            if children:  # 如果有儿子菜单，加到儿子菜单列表中
                for child in children:
                    menu_dict["children"].append(
                        {"pk": child.pk, "name": child.name, "url": child.url}
                    )

    # print(permissions_list)
    # print(menus_list)

    # session中注入权限数据
    request.session["permissions_list"] = permissions_list

    # session中注入菜单数据
    request.session["menus_list"] = menus_list
