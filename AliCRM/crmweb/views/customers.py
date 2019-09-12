from django.shortcuts import render, redirect, reverse
from crmweb.forms import formAuth
from crmweb import models
from django.contrib.auth.decorators import login_required
from django import views
from django.utils.decorators import method_decorator
from utils.customPaginator import Paginator
from django.db.models import Q, Count

from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./CrmWeb/templates/charts"))

from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Timeline
from example.commons import Faker
from pyecharts.globals import ThemeType


# 主页展示
class Index(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request):
        all_customers = models.Customer.objects.filter(consultant__isnull=True)
        # 获取分页所有数据量
        data_counts = all_customers.count()

        # 生成一个分页对象
        paginator = Paginator(request, data_counts, 10)

        # 获取当前页展示数据的范围
        all_customers = all_customers[paginator.start:paginator.end]

        # 获取分页的标签
        paginator_tag = paginator.paginate()  # 调用定义好的分页方法

        return render(request, "index.html", {"all_customers": all_customers, "paginator_tag": paginator_tag})


# 公户（私户）数据展示
class CommonData(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request):
        # 判断请求是公户数据还是私户数据
        if request.path == reverse("common"):
            flag = True
            all_customers = models.Customer.objects.filter(consultant__isnull=True, status="unregistered").order_by(
                "-pk")
        else:
            flag = False
            all_customers = models.Customer.objects.filter(consultant=request.user, status="unregistered").order_by(
                "-pk")

        # 使用Q查询拼接查询条件
        condition = request.GET.get("condition", "")  # 获取搜索的条件分类
        query = request.GET.get("q", "")  # 获取搜索的条件
        if condition and query:  # 如果有查询调参数，两个参数都有，根据查询参数查询后找到数据
            condition = condition + "__contains"
            q = Q()  # Q实例化生成q对象，q对象可以帮我们拼接字符串为 condition__contians= xx的关键字参数传到filter中。
            q.children.append((condition, query))
            all_customers = all_customers.filter(q)

        # 开始分页展示
        data_counts = all_customers.count()  # 获取分页的总数据数量

        # 生成一个分页对象
        paginator = Paginator(request, data_counts, 10)

        # 获取当前页展示数据的范围
        try:  # 异常是否查到了数据，查到了才切片，不然会报错
            all_customers = all_customers[paginator.start:paginator.end]
        except Exception:
            pass

        # 获取分页的标签
        paginator_tag = paginator.paginate()  # 调用定义好的分页方法

        # 获取跳转页的标签
        jump_tag = paginator.jump_page()  # 调用定义好的跳转页方法获取跳转页标签
        jump_js = paginator.jump_js()  # 调用定义好的跳转页方法获取跳转页js代码

        name_str = None
        if "*customer*" in request.path:
            name_list = request.path.split("*customer*")[1:]
            name_str = ','.join(name_list)

        return render(request, "customers_common_list.html",
                      {"flag": flag, "all_customers": all_customers, "paginator_tag": paginator_tag,
                       "jump_tag": jump_tag, "jump_js": jump_js, "name_str": name_str})

    def post(self, request):
        operate = request.POST.get("operate")
        if operate:
            if hasattr(self, operate):
                func = getattr(self, operate)
                if callable(func):
                    ret = func(request)
                    if ret:  # 函数有返回值，也就是有被别的销售提前选走的客户
                        info = ""
                        for obj in ret:
                            info = info + "*customer*" + obj.__str__()
                        url = request.path + info
                        return redirect(url)
                    return redirect(request.path)
                else:
                    return HttpResponse("访问地址有误！")
            return HttpResponse("访问地址有误！")
        return redirect("common")

    def batch_delete(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        models.Customer.objects.filter(pk__in=choose_list).delete()

    def batch_update(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        models.Customer.objects.filter(pk__in=choose_list).update(status="studying")

    def batch_c2p(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        customer_list = models.Customer.objects.filter(pk__in=choose_list)

        has_choosed = []  # 定义一个列表
        for customer_obj in customer_list:
            if customer_obj.consultant:  # 如果客户被别人选了，加进去
                has_choosed.append(customer_obj)
            else:
                # 如果还没有备选则保存
                customer_obj.consultant = request.user
                customer_obj.save()
        return has_choosed

    def batch_p2c(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        models.Customer.objects.filter(pk__in=choose_list).update(consultant=request.user)


# 私户数据展示（作废）
class PrivateData(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request):
        condition = request.GET.get("condition", "")
        query = request.GET.get("q", "")
        condition = condition + "__contains"
        q = Q()  # Q实例化生成q对象，q对象可以帮我们拼接字符串为 condition__contians= xx的关键字参数传到filter中。
        q.children.append((condition, query))

        if condition and query:  # 如果有查询调参数，两个参数都有，根据查询参数查询后找到数据
            all_customers = models.Customer.objects.filter(q, consultant=request.user).order_by("-pk")
        else:  # 判断有没有查询参数，只有有一个没有参数，就查询所有公户数据
            all_customers = models.Customer.objects.filter(consultant=request.user).order_by("-pk")

        # 开始分页展示
        data_counts = all_customers.count()

        # 生成一个分页对象
        paginator = Paginator(request, data_counts, 10)

        # 获取当前页展示数据的范围
        try:  # 异常是否查到了数据，查到了才切片，不然会报错
            all_customers = all_customers[paginator.start:paginator.end]
        except Exception:
            pass

        # 获取分页的标签
        paginator_tag = paginator.paginate()  # 调用定义好的分页方法

        # 获取跳转页的标签
        jump_tag = paginator.jump_page()  # 调用定义好的跳转页方法

        return render(request, "customers_common_list.html",
                      {"all_customers": all_customers, "paginator_tag": paginator_tag, "jump_tag": jump_tag})

    def post(self, request):
        operate = request.POST.get("operate")
        if operate:
            if hasattr(self, operate):
                func = getattr(self, operate)
                if callable(func):
                    func(request)
                    return redirect("private")
                else:
                    return HttpResponse("访问地址有误！")
            return HttpResponse("访问地址有误！")
        return redirect("private")

    def batch_delete(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        models.Customer.objects.filter(pk__in=choose_list).delete()

    def batch_update(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        models.Customer.objects.filter(pk__in=choose_list).update(status="studying")

    def batch_p2c(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        models.Customer.objects.filter(pk__in=choose_list).update(consultant=request.user)


# 添加公共（私有）客户记录
class CustomerAdd(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request):
        form_obj = formAuth.CustomerAddMF()
        return render(request, "customers_add.html", {"form_obj": form_obj})

    def post(self, request):
        form_obj = formAuth.CustomerAddMF(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("common")
        else:
            return render(request, "customers_add.html", {"form_obj": form_obj})


# 修改公共（私有）客户记录
class CustomerEdit(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request, n):
        customer_obj = models.Customer.objects.filter(pk=n).first()
        form_obj = formAuth.CustomerAddMF(instance=customer_obj)
        return render(request, "customers_add.html", {"form_obj": form_obj})

    def post(self, request, n):
        customer_obj = models.Customer.objects.filter(pk=n).first()
        form_obj = formAuth.CustomerAddMF(request.POST, instance=customer_obj)
        if form_obj.is_valid():
            form_obj.save()
            # 判断修改的是公户还是私户
            if customer_obj.consultant:
                # 私户跳转私户界面
                return redirect("private")
            else:
                # 公户跳转公户界面
                return redirect("common")

        else:
            return render(request, "customers_add.html", {"form_obj": form_obj})


# 删除公共（私有）客户记录
class CustomerDel(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request, n):
        customer_obj = models.Customer.objects.filter(pk=n)
        # 判断删除的是公户还是私户
        if customer_obj.first().consultant:
            customer_obj.delete()
            return redirect("private")
        else:
            customer_obj.delete()
            return redirect("common")


# 客户数据分析
class ChartsCustomer(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    analyse = [  # 配置分析类别表
        (1, "course_analyse", "课程咨询分析"),
        (2, "source_analyse", "客户来源分析"),
        (3, "time_analyse", "客户月流量分析"),
    ]

    def get(self, request, n):
        try:
            n = int(n)
        except Exception:
            n = 1
        else:
            if not n in range(1, len(self.analyse) + 1):
                n = 1
        title = self.analyse[n - 1][2]
        if hasattr(self, self.analyse[n - 1][1]):
            func = getattr(self, self.analyse[n - 1][1])
            if callable(func):
                content = func()
            else:
                content = "没有相关分析表！"
        else:
            content = "没有相关分析表！"
        return render(request, "customers_charts.html", {"title": title, "content": content})

    def course_analyse(self):
        """咨询课程分析"""
        course_info = models.Customer.objects.values("course").annotate(num=Count("pk"))  # queryset
        course_list = []
        course_amounts = []

        for course in course_info:
            course_list.append(course['course'])
            course_amounts.append(course["num"])
        print(course_list)
        print(course_amounts)

        # 替换课程名称对应的中文名
        for i in range(len(course_list)):
            for j in range(len(models.course_choices)):
                for n in range(len(course_list[i])):
                    if course_list[i][n] == models.course_choices[j][0]:
                        course_list[i][n] = models.course_choices[j][1]

        # print(course_list)  #
        list_single = []  # 定义单门课程列表
        list_multi = []  # 定义多门课程列表

        for i in course_list:
            if len(i) > 1:
                list_multi.append(i)
            else:
                list_single.append(i)

        # 选择多门课，拆分，统计课程数量
        for m in range(len(list_multi)):
            for n in range(len(list_single)):
                if list_multi[m] == list_single[n]:
                    course_amounts[n] += 1
        # print(list_single)
        # print(list_multi)

        # 清洗单门课程的数量，去除选择多门课程的数量
        course_list = list_single
        course_amounts = course_amounts[:len(list_single)]

        bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                .add_xaxis(course_list)
                .add_yaxis("咨询数量", course_amounts)
                .set_global_opts(title_opts=opts.TitleOpts(title="课程咨询分析", subtitle="客户咨询课程数量的分析整理"))
        )
        content = bar.render_embed()
        return content

    def source_analyse(self):
        """客户来源分析"""
        source_info = models.Customer.objects.values_list("source").annotate(num=Count("pk"))  # queryset

        # 替换来源称对应的中文名
        source_list = list(source_info)  # [('baidu',28)],source_type = (("qq","qq"),)
        source_list = [list(i) for i in source_list]
        for i in range(len(source_list)):
            for j in range(len(models.source_type)):
                if source_list[i][0] == models.source_type[j][0]:
                    source_list[i][0] = models.source_type[j][1]
        source_list = [tuple(i) for i in source_list]
        print(source_list)
        pie = (
            Pie()
                .add(
                "客户来源",
                source_list,
                radius=["30%", "75%"],
                center=["50%", "50%"],
                rosetype="area",
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="客户来源分析")
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(formatter="{b}: {c}")
            )
        )
        content = pie.render_embed()
        return content

    def time_analyse(self):
        """客户来源分析"""

        def get_month_data(search, condition="month"):
            # 获取每个月的数据

            q = Q()
            condition = "date__" + condition
            # print(condition,search)
            q.children.append((condition, search))
            source_info = models.Customer.objects.filter(q).values_list("source").annotate(num=Count("pk"))  # queryset

            # 替换来源称对应的中文名
            source_list = list(source_info)  # [('baidu',28)],source_type = (("qq","qq"),)
            source_list = [list(i) for i in source_list]
            for i in range(len(source_list)):
                for j in range(len(models.source_type)):
                    if source_list[i][0] == models.source_type[j][0]:
                        source_list[i][0] = models.source_type[j][1]
            source_list = [tuple(i) for i in source_list]
            # print(source_list)
            pie = (
                Pie()
                    .add(
                    "客户来源",
                    source_list,
                    radius=["30%", "75%"],
                    center=["50%", "50%"],
                    rosetype="area",
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="2019年客户月流量分析", )
                )
                    .set_series_opts(
                    label_opts=opts.LabelOpts(formatter="{b}: {c}")
                )
                    .set_global_opts(
                    toolbox_opts=opts.ToolboxOpts(orient="vertical")
                )
            )
            return pie

        # 获取饼图列表
        pie_list = []
        for i in range(1, 13):
            pie = get_month_data(i, "month")
            pie_list.append(pie)

        # 设置时间线展示
        line = (
            Timeline()
                .add(pie_list[0], "1月")
                .add(pie_list[1], "2月")
                .add(pie_list[2], "3月")
                .add(pie_list[3], "4月")
                .add(pie_list[4], "5月")
                .add(pie_list[5], "6月")
                .add(pie_list[6], "7月")
                .add(pie_list[7], "8月")
                .add(pie_list[8], "9月")
                .add(pie_list[9], "10月")
                .add(pie_list[10], "11月")
                .add(pie_list[11], "12月")
        )
        content = line.render_embed()
        return content


# 客户跟进信息展示
class ConsultRecord(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request, n=None):
        if n:  # 如果指定了某一个客户的跟进记录，就先过滤
            all_records = models.ConsultRecord.objects.filter(consultant=request.user, customer_id=n).order_by("-pk")
            print(n)
        else:
            all_records = models.ConsultRecord.objects.filter(consultant=request.user).order_by("-pk")

        condition = request.GET.get("condition", "")
        query = request.GET.get("q", )

        if query:  # 如果有查询调参数，两个参数都有，根据查询参数查询后找到数据
            q = Q()  # Q实例化生成q对象，q对象可以帮我们拼接字符串为 condition__contians= xx的关键字参数传到filter中。
            if condition == "status":  # 判断如果查询条件是status，那么先去匹配是哪个状态
                status_info = models.seek_status_choices
                status_list = []  # 定义一个存储查询状态的列表，里面放 A或B或...的状态码
                for i in range(len(status_info)):
                    # print(i, query, status_info[i][1])
                    if query in status_info[i][1]:
                        status_list.append(status_info[i][0])
                condition = condition + "__in"
                q.children.append((condition, status_list))
                all_records = all_records.filter(q)  # 根据搜索条件查询
            else:  # 查询条件不是status，直接模糊匹配
                condition = condition + "__qq_name__contains"
                q.children.append((condition, query))
                all_records = all_records.filter(q)

        # 开始分页展示
        data_counts = all_records.count()

        # 生成一个分页对象
        paginator = Paginator(request, data_counts, 10)

        # 获取当前页展示数据的范围
        try:  # 异常是否查到了数据，查到了才切片，不然会报错
            all_records = all_records[paginator.start:paginator.end]
        except Exception:
            pass

        # 获取分页的标签
        paginator_tag = paginator.paginate()  # 调用定义好的分页方法

        # 获取跳转页的标签
        jump_tag = paginator.jump_page()  # 调用定义好的跳转页方法获取跳转标签
        jump_js = paginator.jump_js()  # 调用定义好的跳转页方法获取跳转页js代码

        return render(request, "consult_record_list.html",
                      {"all_records": all_records, "paginator_tag": paginator_tag, "jump_tag": jump_tag,
                       "jump_js": jump_js, "customer_id": n})


# 增加（修改）客户跟进信息
class ConsultRecordAddEdit(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request, n=None):
        # 没有传递n是请求展示增加页面，传递了n是请求展示修改页面
        record_obj = models.ConsultRecord.objects.filter(pk=n).first()
        form_obj = formAuth.ConsultRecodeAddMF(request, instance=record_obj)
        return render(request, "consult_record_add.html", {"form_obj": form_obj, "n": n})

    def post(self, request, n=None):
        # 没有传递n是请求确认增加页面，传递了n就是请求确认修改页面
        record_obj = models.ConsultRecord.objects.filter(pk=n).first()
        print(record_obj)
        form_obj = formAuth.ConsultRecodeAddMF(request, request.POST,
                                               instance=record_obj)  # 实例化的传递request，是为了在modelform中筛选出当前销售的客户和跟进人，具体看modelform信息。
        if form_obj.is_valid():
            form_obj.save()
            return redirect("consult_record")
        else:
            return render(request, "consult_record_add.html", {"form_obj": form_obj})


# 删除客户跟进记录
class ConsultRecordDel(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request, n):
        models.ConsultRecord.objects.filter(pk=n).delete()
        return redirect("consult_record")


# 报名信息展示
class Enrollment(views.View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        return res

    def get(self, request):
        all_customers = models.Enrollment.objects.all().order_by("-pk")
        # 使用Q查询拼接查询条件
        condition = request.GET.get("condition", "")  # 获取搜索的条件分类
        query = request.GET.get("q", "")  # 获取搜索的条件
        if condition and query:  # 如果有查询调参数，两个参数都有，根据查询参数查询后找到数据
            condition = condition + "__contains"
            q = Q()  # Q实例化生成q对象，q对象可以帮我们拼接字符串为 condition__contians= xx的关键字参数传到filter中。
            q.children.append((condition, query))
            all_customers = all_customers.filter(q)

        # 开始分页展示
        data_counts = all_customers.count()  # 获取分页的总数据数量

        # 生成一个分页对象
        paginator = Paginator(request, data_counts, 10)

        # 获取当前页展示数据的范围
        try:  # 异常是否查到了数据，查到了才切片，不然会报错
            all_customers = all_customers[paginator.start:paginator.end]
        except Exception:
            pass

        # 获取分页的标签
        paginator_tag = paginator.paginate()  # 调用定义好的分页方法

        # 获取跳转页的标签
        jump_tag = paginator.jump_page()  # 调用定义好的跳转页方法获取跳转页标签
        jump_js = paginator.jump_js()  # 调用定义好的跳转页方法获取跳转页js代码

        return render(request, "enrollment_list.html",
                      {"all_customers": all_customers, "paginator_tag": paginator_tag, "jump_tag": jump_tag,
                       "jump_js": jump_js})

    # def post(self, request):
    #     operate = request.POST.get("operate")
    #     if operate:
    #         if hasattr(self, operate):
    #             func = getattr(self, operate)
    #             if callable(func):
    #                 ret = func(request)
    #                 if ret:  # 函数有返回值，也就是有被别的销售提前选走的客户
    #                     info = ""
    #                     for obj in ret:
    #                         info = info + "*customer*" + obj.__str__()
    #                     url = request.path + info
    #                     return redirect(url)
    #                 return redirect(request.path)
    #             else:
    #                 return HttpResponse("访问地址有误！")
    #         return HttpResponse("访问地址有误！")
    #     return redirect("common")
    #
    # def batch_delete(self, request, *args, **kwargs):
    #     choose_list = request.POST.getlist("choose")
    #     models.Customer.objects.filter(pk__in=choose_list).delete()
    #
    # def batch_update(self, request, *args, **kwargs):
    #     choose_list = request.POST.getlist("choose")
    #     models.Customer.objects.filter(pk__in=choose_list).update(status="studying")
    #
    # def batch_c2p(self, request, *args, **kwargs):
    #     choose_list = request.POST.getlist("choose")
    #     customer_list = models.Customer.objects.filter(pk__in=choose_list)
    #
    #     has_choosed = []  # 定义一个列表
    #     for customer_obj in customer_list:
    #         if customer_obj.consultant:  # 如果客户被别人选了，加进去
    #             has_choosed.append(customer_obj)
    #         else:
    #             # 如果还没有备选则保存
    #             customer_obj.consultant=request.user
    #             customer_obj.save()
    #     return has_choosed

    def batch_p2c(self, request, *args, **kwargs):
        choose_list = request.POST.getlist("choose")
        models.Customer.objects.filter(pk__in=choose_list).update(consultant=request.user)


# 测试路径
def test1(request):
    return HttpResponse("ok")

# 测试视图类
class Test(views.View):
    def get(self, request):
        return render(request, "test.html")

    def post(self, request):
        print(request.POST)
        print(request.body)
        if request.POST.get("username") == "alex" and request.POST.get("password") == "alex":
            return HttpResponse("ok")
        else:
            return redirect("test")


# 图表测试路名
def chartstest(request):
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(Faker.choose(), Faker.values())],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-Radius"),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    content = c.render_embed()

    return render(request, "customers_charts.html", {"content": content})
