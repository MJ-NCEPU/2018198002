# 老师信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from myadmin.models import Salary


def index(request, pIndex=1):
    '''浏览信息'''
    smod = Salary.objects
    slist = smod.filter(status__lt=9)
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        slist = slist.filter(tname__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(slist, 5)  # 以每页5条数据分页
    maxpages = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"salarylist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/salary/index.html", context)


def add(request):
    '''加载信息添加表单'''
    return render(request, "myadmin/salary/add.html")


def insert(request):
    '''执行信息添加'''
    try:
        ob = Salary()
        ob.tname = request.POST['tname']
        ob.tgnum = request.POST['tgnum']
        ob.basicsalary = request.POST['basicsalary']
        ob.carsubsidy = request.POST['carsubsidy']
        ob.roomsubsidy = request.POST['roomsubsidy']
        ob.award = request.POST['award']
        ob.sum = int(ob.basicsalary)+int(ob.carsubsidy)+int(ob.roomsubsidy)+int(ob.award)
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.status = 1
        ob.save()
        context = {'info': "添加成功！"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, sid=0):
    '''执行信息删除'''
    try:
        ob = Salary.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, sid=0):
    '''加载信息编辑表单'''
    try:
        ob = Salary.objects.get(id=sid)
        context = {'salary': ob}
        return render(request, "myadmin/salary/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, sid):
    '''执行信息编辑'''
    try:
        ob = Salary.objects.get(id=sid)
        ob.tname = request.POST['tname']
        ob.tgnum = request.POST['tgnum']
        ob.basicsalary = request.POST['basicsalary']
        ob.carsubsidy = request.POST['carsubsidy']
        ob.roomsubsidy = request.POST['roomsubsidy']
        ob.award = request.POST['award']
        ob.sum = int(ob.basicsalary) + int(ob.carsubsidy) + int(ob.roomsubsidy) + int(ob.award)
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
    return render(request, "myadmin/info.html", context)
