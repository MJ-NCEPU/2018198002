from django.http import HttpResponse
from django.shortcuts import render
from teacher.models import Homework, Teacher_Students


def myhomework(request):
    myhomew = Homework.objects.all()
    snum = request.session['snum']  # 获取学号进一步获取班级
    strs = ''
    i = 0
    for s in str(snum):
        if (i <= 6):
            strs = strs + s
            i = i + 1
    # 获取这个班级所对应的是哪个老师
    ob_t = Teacher_Students.objects.filter(classnum=strs).filter(status=1)
    flag = 0
    tgnumlist = []  # 存储老师工号，判断作业文件是否对应
    for s in ob_t:
        tgnumlist.append(s.tgnum)
    for a in myhomew:
        if a.tgnum in tgnumlist:
            flag = 1
            break
    context = {"myhomew": myhomew, 'tgnumlist': tgnumlist, 'flag': flag}
    return render(request, 'students/myhomework/myhomework.html', context)
