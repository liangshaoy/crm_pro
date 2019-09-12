from django.test import TestCase

# Create your tests here.


class Base(object):  # 定义类Base
    def __init__(self,val):
        self.val = val

    def func(self):
        self.test()
        print(self.val)

    def test(self):
        print("Base.test")

class Foo(Base):  # 定义类Foo
    def test(self):
        print("FOO.test")

    # def func(self):
    #     print(self.val,666)
    # 有就执行自己的，没有就执行父类的
class Bar(object):
    def __init__(self):
        self._register = {}

    def register(self,a,b=None):
        if not b:
            b=Base
        self._register[a] = b(a)  #函数，类，对象

obj = Bar()  #实例化就会去执行它自己的__init__方法，并获取到一个对象b,b就可以调用里面的属性和方法了

obj.register(1,Foo)  # _register属性中存的是1:Foo类，且Foo.val=1
obj.register(2)  # 又增加了一个2:Base类的实例，且Base.val=2
print(obj._register)  # {1: <__main__.Foo object at 0x0000000002213160>, 2: <__main__.Base object at 0x0000000002213198>}
# obj._register[1] == Foo(1)

obj._register[1].func()  # Foo的对象 打印结果：FOO.test     1
obj._register[2].func()  # Base的对象 打印结果：Base.test     2
