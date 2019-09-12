from student.views import students
from django.conf.urls import url

urlpatterns = [
    # 班级学习记录展示
    url(r'^class/study/record/list/', students.ClassStudyRecord.as_view(), name="class_study_record"),

    # 学员学习记录展示
    url(r'^student/study/record/list/(\d+)?/?', students.StudentStudyRecord.as_view(), name="student_study_record"),
]