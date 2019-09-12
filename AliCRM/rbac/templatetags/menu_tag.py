from rbac import models
from django import template  # 导入template模块
from django.utils.safestring import mark_safe  # 导入安全输入的模块


register = template.Library()  # register的名字是固定的,不可改变


@register.simple_tag  # 装饰自定义过滤器
def make_menus_html(request, parent_id=None, current_parent_id=None):
    """
    根据用户提供的请求，提取菜单权限数据，递归生成多级菜单。
    menus = Menus.objects.all()
    :param request: request请求对象，包含当前路径，和当前用户信息系
    :param parent_id: 父级菜单ID，指定当前菜单从属福安息
    :param current_parent_id: 当前父级菜单ID
    :return: 返回生成的多级菜单标签（mark_safe安全生成）
    """
    user = request.session.get("user")
    menus = models.Permission.objects.filter(identity__userinfo__username=user)
    make_html = ""  # 定义一个菜单标签字符串
    for menu in menus:  # 遍历所有菜单
        child_menu_flag = "treeview"  # 如果有子菜单，设置类为treeview
        menu_right_flag = '<span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span>'  # 设置菜单左侧的图表样式

        # 拼接第二层子菜单标签2
        child_menu_html = '<ul class="treeview-menu">{make_child_menu_html}</ul>'  # 子菜单列表外层的ul标签
        child_menu = '<li class="{active}"><a href="{menu_url}"><i class="fa fa-circle-o"></i> {menu_name}</a></li>'  # 设置子菜单列表的li标签，带样式

        # 设置第一层菜单标签
        master_menu_html = """
        <li class="{child_menu_flag} {active}">
            <a href="{menu_url}"><i class="fa {menu_icon}"></i> <span>{menu_name}</span>{menu_right_flag}</a>
            <ul class="treeview-menu">
            {children_menu_html}
            </ul>
        </li>"""

        # 设置第二层子菜单标签1
        children_menu_html = """
        <li class="treeview">
            <a href="{menu_url}"><i class="fa fa-circle-o"></i> <span>{menu_name}</span>{menu_right_flag}</a>
            {child_menu_html}
        </li>"""

        parent = menu.parent  # 获取当前菜单的父级菜单
        if current_parent_id == menu.id or (not parent and current_parent_id) or not menu.show:
            continue  # 如果当前父级菜单ID是自己的id 或 没有父级菜单且有当前父级ID则跳过本次循环

        # 如果没有父级菜单且当前父级ID是None  # 生成一级菜单
        if not parent and current_parent_id is None:
            make_children_menu_html = make_menus_html(request, parent_id=parent_id, current_parent_id=menu.id)  # 获取子菜单

            # 判断这个一级菜单有没有子菜单，没有的话，说明只有一层，去掉左尖角符<，并添加样式
            if not make_children_menu_html:
                menu_right_flag = ''
                child_menu_flag = ''
            # 设置菜单左侧的图标样式
            menu_icon = "fa-eye"
            if hasattr(menu, 'icon'):
                menu_icon = menu.icon
            # print(menu.url, request.path_info)
            if menu.url == request.path_info:
                active_menu = 'active'
            else:
                for i in menu.permission_set.all():
                    if i.url == request.path:
                        active_menu = 'active'
                        break
                else:
                    active_menu = ""

            # 拼接菜单的标签
            make_master_menu_html = master_menu_html.format(
                child_menu_flag=child_menu_flag,
                active=active_menu,
                menu_url=menu.url,
                menu_icon=menu_icon,
                menu_name=menu.name,
                menu_right_flag=menu_right_flag,
                children_menu_html=make_children_menu_html
            )
            make_html += make_master_menu_html


        # 如果有父级且当前父级ID是自己的父级ID
        elif parent and current_parent_id == parent.id:
            make_child_menu_html = make_menus_html(
                request,
                parent_id=current_parent_id,
                current_parent_id=menu.id
            )

            if make_child_menu_html:  # 如果子菜单还有孙子菜单，
                child_menu_html = child_menu_html.format(
                    make_child_menu_html=make_child_menu_html
                )

                children_menu_html = children_menu_html.format(
                    menu_url=menu.url,
                    menu_name=menu.name,
                    menu_right_flag=menu_right_flag,
                    child_menu_html=child_menu_html
                )
            else:  # 子菜单没有孙子菜单，拼接子菜单列表，多个li标签
                # print(menu.url, request.path_info)
                if menu.url == request.path_info:
                    active_menu = 'active'
                else:
                    active_menu = ''
                children_menu_html = child_menu.format(
                    active=active_menu,
                    menu_url=menu.url,
                    menu_name=menu.name
                )
            make_html += children_menu_html
        else:
            continue
    return mark_safe(make_html)
