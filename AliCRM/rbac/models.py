from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# 身份分类
identity_choices = (
    ("1", "董事"),
    ("2", "CEO"),
    ("3", "销售"),
    ("4", "网咨"),
    ("5", "老师"),
    ("6", "班主任"),
)

# 扩展的用户表
class UserInfo(AbstractUser):
    """用户信息表:老师，助教，销售，班主任"""
    id = models.AutoField(primary_key=True)
    gender_type = (("male", "男"), ("female", "女"))
    gender = models.CharField(choices=gender_type, null=True, max_length=12)
    phone = models.CharField(max_length=11, null=True, unique=True)
    role = models.ManyToManyField("Role")

    def __str__(self):
        return self.username


# 身份表
class Role(models.Model):
    title = models.CharField("职位", choices=identity_choices, max_length=32)
    permission = models.ManyToManyField("Permission")

    def __str__(self):
        return self.title


# 权限表
class Permission(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'菜单名')
    url = models.CharField(
        max_length=300,
        verbose_name=u'权限url地址',
        null=True,
        blank=True,
        help_text=u'是否给菜单设置一个url地址'
    )
    icon = models.CharField(
        max_length=32,
        verbose_name='二级菜单图标',
        null=True,
        blank=True
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=u'父级菜单',
        null=True,
        blank=True,
        help_text=u'如果添加的是子菜单，请选择父菜单'
    )
    show = models.BooleanField(
        verbose_name=u'是否显示',
        default=False,
        help_text=u'菜单是否显示，默认添加不显示'
    )
    priority = models.IntegerField(
        verbose_name=u'显示优先级',
        null=True,
        blank=True,
        help_text=u'菜单的显示顺序，优先级越小显示越靠前'
    )

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        verbose_name = u"权限表"
        verbose_name_plural = u"权限表"
        ordering = ["priority","id"]


