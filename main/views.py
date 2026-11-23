from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_sameorigin
import datetime
from datetime import date, timedelta

from .decorators import *
from .models import *

# Create your views here.
def task_count(request):
    if not request.user.is_authenticated:
        return {'task_count': 0}

    return {'task_count': Task.objects.filter(user=request.user).count()}

def calendar_status(request):
    if not request.user.is_authenticated:
        return {'calendar_status': 'success'}

    today = date.today()
    pending = Task.objects.filter(
        user=request.user,
        completed=False,
        deadline__isnull=False,
    )

    if pending.filter(deadline__lt=today).exists():
        status = 'error'
    elif pending.filter(deadline__gte=today, deadline__lte=today + timedelta(days=7)).exists():
        status = 'warning'
    else:
        status = 'success'

    return {'calendar_status': status}


def index(request):
    return render(request, 'index.html')

def manual(request):
    return render(request, 'manual.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {
                'message': 'Invalid credentials.'
            })
    else:
        return render(request, 'login.html')


@logedout_forbidden
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if len(password) < 8:
            return render(request, 'register.html', {
                'message': 'Password too short.'
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return redirect('manual')
    else:
        return render(request, 'register.html')
@logedout_forbidden
def applications(request):
    return render(request, 'applications.html',{
        'applications': Application.objects.filter(user=request.user)
    })
@logedout_forbidden
def newapl(request):
        id = request.GET['id']
        course = Course.objects.get(pk=id)
        return render(request, 'aplshop.html',{
            'course':course,
            'id':id,
        })
@logedout_forbidden
def aplshop(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'remove':
            id = request.POST['id']
            a = Application.objects.get(pk=id)
            if request.user == a.user:
                a.delete()
            return redirect('applications')
        elif action == 'status':
            id = request.POST['id']
            status = request.POST['status']
            a = Application.objects.get(pk=id)
            a.status = status
            a.save()
            return redirect('applications')
        else:
            status = request.POST['status']
            note = request.POST['note']
            documents = Document.objects.filter(pk__in=request.POST.getlist('documents'))
            if action == 'new':
                course = Course.objects.get(pk=request.POST['id'])
                a = Application.objects.create(user=request.user,course=course, status=status, note=note)
                for doc in documents:
                    a.documents.add(doc)
                a.save()
                return redirect(reverse('applications', query={'q': course.name + course.university.name}))
            elif action == 'edit':
                id = request.POST['id']
                a = Application.objects.get(pk=id)
                a.status = status
                a.note = note
                for doc in documents:
                    if doc not in a.documents.all():
                        a.documents.add(doc)
                for doc in a.documents.all():
                    if doc not in documents:
                        a.documents.remove(doc)
                a.save()
                return redirect(reverse('applications', query={'q': a.course.name + a.course.university.name}))
    elif request.method == 'GET':
        id = request.GET['id']
        a = Application.objects.get(pk=id)
        return render(request, 'aplshop.html',{
            'id': id,
            'action': 'edit',
            'course': a.course,
            'status': a.status,
            'doc_ids': list(a.documents.values_list('id', flat=True)),
            'editnote': a.note,
        })
@logedout_forbidden
def documents(request):
    return render(request, 'documents.html',{
        'documents': Document.objects.filter(user=request.user)
    })
@logedout_forbidden
def newdoc(request):
        return render(request, 'docshop.html')
@logedout_forbidden
def docshop(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'remove':
            id = request.POST['id']
            d = Document.objects.get(pk=id)
            if request.user == d.user:
                d.delete()
            return redirect('documents')
        else:
            title = request.POST['title']
            content = request.POST['content']
            try:
                document = request.FILES['document']
            except:
                document = None
            if action == 'new':
                d = Document.objects.create(user=request.user, title=title, content=content, document=document)
                d.save()
                return redirect(reverse('documents', query={'q': title}))
            elif action == 'edit':
                id = request.POST['id']
                d = Document.objects.get(pk=id)
                d.title = title
                d.content = content
                if document:
                    d.document.delete()
                    d.document = document
                d.save()
                return redirect(reverse('documents', query={'q': title}))
    elif request.method == 'GET':
        id = request.GET['id']
        d = Document.objects.get(pk=id)
        return render(request, 'docshop.html',{
            'id': id,
            'action': 'edit',
            'edittitle': d.title,
            'editcontent': d.content,
        })
@logedout_forbidden
def calendar(request):
    return render(request, 'calendar.html',{
        'calendar': Task.objects.filter(user=request.user)
    })
@logedout_forbidden
def tasks(request):
    return render(request, 'tasks.html',{
        'tasks': Task.objects.filter(user=request.user)
    })
@logedout_forbidden
def newtask(request):
    target = request.GET['target']
    id = request.GET['id']
    document = None if target != 'document' else Document.objects.get(pk=id)
    application = None if target != 'application' else Application.objects.get(pk=id)
    return render(request, 'taskshop.html',{
        'id': id,
        'target': target,
        'document': document,
        'application': application,
    })
@logedout_forbidden
def taskshop(request):
    if request.method == 'POST':
        id = request.POST['id']
        action = request.POST['action']
        if action == 'toggle':
            t = Task.objects.get(pk=id)
            if request.user == t.user:
                t.completed = not t.completed
                t.save()
            return redirect('tasks')
        elif action == 'remove':
            t = Task.objects.get(pk=id)
            if request.user == t.user:
                t.delete()
            return redirect('tasks')
        else:
            title = request.POST['title']
            content = request.POST['content']
            try:
                deadline = datetime.strptime(request.POST['deadline'], '%Y-%m-%d').date()
            except:
                deadline = None
            try:
                file = request.FILES['document']
            except:
                file = None
            if action == 'new':
                target = request.POST['target']
                if target == 'document':
                    d = Document.objects.get(pk=id)
                    a = None
                elif target == 'application':
                    a = Application.objects.get(pk=id)
                    d = None
                else:
                    a = None
                    d = None
                t = Task.objects.create(user=request.user, title=title, content=content, deadline=deadline, file=file, document=d, application = a)
                t.save()
                return redirect(reverse('tasks', query={'q': title}))
            elif action == 'edit':
                t = Task.objects.get(pk=id)
                t.title = title
                t.content = content
                t.deadline = deadline
                if file:
                    t.file.delete()
                    t.file = file
                t.save()
                return redirect(reverse('tasks', query={'q': title}))
    elif request.method == 'GET':
        id = request.GET['id']
        t = Task.objects.get(pk=id)
        if t.document:
            target = 'document'
        elif t.application:
            target = 'application'
        else:
            target = 'task'
        document = t.document
        application = t.application
        return render(request, 'taskshop.html',{
            'id': id,
            'target': target,
            'action': 'edit',
            'edittitle': t.title,
            'editcontent': t.content,
            'editdeadline': t.deadline,
            'document': document,
            'application': application,
        })
def universities(request):
    if request.user.is_authenticated:
        return render(request, 'universities.html',{
            'universities': University.objects.all()
        })
    else:
        return render(request, 'universities.html',{'universities': University.objects.all(),})
@only_super
def newuni(request):
        return render(request, 'unishop.html')
@only_super
def unishop(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'remove':
            id = request.POST['id']
            u = University.objects.get(pk=id)
            u.delete()
            return redirect('universities')
        else:
            name = request.POST['name']
            country = request.POST['country']
            city = request.POST['city']
            portal_link = request.POST['portal']
            note = request.POST['note']
            if action == 'new':
                u = University.objects.create(name=name,country=country,city=city,portal_link=portal_link, note=note)
                u.save()
                return redirect(reverse('universities', query={'q': name}))
            elif action == 'edit':
                id = request.POST['id']
                u = University.objects.get(pk=id)
                u.name = name
                u.country = country
                u.city = city
                u.portal_link = portal_link
                u.note = note
                u.save()
                return redirect(reverse('universities', query={'q': name}))
    elif request.method == 'GET':
        id = request.GET['id']
        u = University.objects.get(pk=id)
        return render(request, 'unishop.html',{
            'id': id,
            'action': 'edit',
            'edittitle': u.name,
            'editcontent': u.note,
            'editcity': u.city,
            'editcountry': u.country,
            'editportal': u.portal_link,
        })
def courses(request):
    if request.user.is_authenticated:
        return render(request, 'courses.html',{
            'courses': Course.objects.all()
        })
    else:
        return render(request, 'courses.html',{'courses': Course.objects.all(),})
@only_super
def newcrs(request):
        id = request.GET['id']
        uni = University.objects.get(pk=id)
        return render(request, 'crsshop.html',{
            'id':id,
            'university': uni
        })
@only_super
def crsshop(request):
    if request.method == 'POST':
        id = request.POST['id']
        action = request.POST['action']
        if action == 'remove':
            c = Course.objects.get(pk=id)
            c.delete()
            return redirect('courses')
        else:
            name = request.POST['name']
            docs = request.POST['docs']
            portal = request.POST['portal']
            try:
                scholar = request.POST['scholar']
                scholar = True
                detail = request.POST['detail']
            except:
                scholar = False
                detail = None
            fee = request.POST['fee']
            try:
                wave = request.POST['wave']
                wave =True
            except:
                wave = False
            note = request.POST['note']
            if action == 'new':
                uni = University.objects.get(pk=request.POST['university'])
                c = Course.objects.create(
                    university=uni,
                    name=name,
                    has_scholarship=scholar,
                    scholarship_details=detail,
                    application_fees=fee,
                    is_fee_wavabe=wave,
                    required_documents=docs,
                    portal_link = portal,
                    note = note,)
                c.save()
                return redirect(reverse('courses', query={'q': name + uni.name}))
            elif action == 'edit':
                c = Course.objects.get(pk=id)
                c.name = name
                c.has_scholarship = scholar
                c.scholarship_details = detail
                c.application_fees = fee
                c.is_fee_wavabe = wave
                c.required_documents = docs
                c.portal_link = portal
                c.note = note
                c.save()
                return redirect(reverse('courses', query={'q': name + c.university.name}))
    elif request.method == 'GET':
        id = request.GET['id']
        c = Course.objects.get(pk=id)
        return render(request, 'crsshop.html',{
            'id': id,
            'university':c.university,
            'action': 'edit',
            'edittitle': c.name,
            'editdocs': c.required_documents,
            'editnote': c.note,
            'editportal': c.portal_link,
            'editscholar':c.has_scholarship,
            'editdetail':c.scholarship_details,
            'editfee': c.application_fees,
            'editwave':c.is_fee_wavabe
        })
def professors(request):
    if request.user.is_authenticated:
        return render(request, 'professors.html',{
            'professors': Professor.objects.all()
        })
    else:
        return render(request, 'professors.html',{'professors': Professor.objects.all(),})
@only_super
def newprf(request):
        id = request.GET['id']
        uni = University.objects.get(pk=id)
        return render(request, 'prfshop.html',{
            'id':id,
            'university': uni
        })
@only_super
def prfshop(request):
    if request.method == 'POST':
        id = request.POST['id']
        action = request.POST['action']
        if action == 'remove':
            p = Professor.objects.get(pk=id)
            p.delete()
            return redirect('professors')
        else:
            name = request.POST['name']
            field = request.POST['field']
            email = request.POST['email']
            mailling_guide = request.POST['guide']
            note = request.POST['note']
            if action == 'new':
                uni = University.objects.get(pk=request.POST['university'])
                p = Professor.objects.create(
                    university=uni,
                    name=name,
                    field=field,
                    email=email,
                    mailling_guide=mailling_guide,
                    note = note,)
                p.save()
                return redirect(reverse('professors', query={'q': name + uni.name}))
            elif action == 'edit':
                p = Professor.objects.get(pk=id)
                p.name = name
                p.field = field
                p.email = email
                p.mailling_guide = mailling_guide
                p.note = note
                p.save()
                return redirect(reverse('professors', query={'q': name + p.university.name}))
    elif request.method == 'GET':
        id = request.GET['id']
        p = Professor.objects.get(pk=id)
        return render(request, 'prfshop.html',{
            'id': id,
            'university':p.university,
            'action': 'edit',
            'edittitle': p.name,
            'editfield': p.field,
            'editemail': p.email,
            'editguide': p.mailling_guide,
            'editnote': p.note,
        })
@logedout_forbidden
@xframe_options_sameorigin
def media(request, id, filename):
    if not (request.user.id == id or request.user.is_superuser):
        return HttpResponse('Forbidden', status=403)

    media_root = Path(settings.MEDIA_ROOT).resolve()
    file_path = (media_root / (str(id) + "/" + filename)).resolve()

    if media_root != file_path and media_root not in file_path.parents:
        return HttpResponse('Forbidden', status=403)

    if not file_path.is_file():
        return HttpResponse('Not Found', status=404)

    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=False,
        filename=file_path.name,
        )