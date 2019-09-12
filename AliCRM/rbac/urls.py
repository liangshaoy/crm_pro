from rbac.views import permission_distribute
from django.conf.urls import url

urlpatterns = [
    url(r'^permission/distribute/', permission_distribute.PermissionDistribute.as_view(), name="distribute")
]