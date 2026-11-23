
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("manual", views.manual, name="manual"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("applications", views.applications, name="applications"),
    path("applications/new", views.newapl, name="newapl"),
    path("applications/edit", views.aplshop, name="aplshop"),
    path("documents", views.documents, name="documents"),
    path("documents/new", views.newdoc, name="newdoc"),
    path("documents/edit", views.docshop, name="docshop"),
    path("calendar", views.calendar, name="calendar"),
    path("tasks", views.tasks, name="tasks"),
    path("tasks/new", views.newtask, name="newtask"),
    path("tasks/edit", views.taskshop, name="taskshop"),
    path("universities", views.universities, name="universities"),
    path("universities/new", views.newuni, name="newuni"),
    path("universities/edit", views.unishop, name="unishop"),
    path("courses", views.courses, name="courses"),
    path("courses/new", views.newcrs, name="newcrs"),
    path("courses/edit", views.crsshop, name="crsshop"),
    path("professors", views.professors, name="professors"),
    path("professors/new", views.newprf, name="newprf"),
    path("professors/edit", views.prfshop, name="prfshop"),
    path('media/<int:id>/<path:filename>',views.media, name='media')
]