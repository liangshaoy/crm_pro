from django.contrib import admin
from crmweb import models

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id',"name","qq","qq_name"]
    list_filter = ['id']
    list_editable = ["name","qq","qq_name"]
    search_fields = ('id',"name","qq_name")

    # # 定制搜索列表
    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super(CustomerAdmin, self).get_search_results(request, queryset, search_term)
    #     try:
    #         search_term_as_int = int(search_term)
    #         queryset |= self.model.objects.filter(pk=search_term_as_int)
    #     except:
    #         pass
    #     return queryset, use_distinct


admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
