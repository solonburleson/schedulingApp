from django.urls import path

from . import views

app_name = 'wo'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard),
    path('workers', views.workers),
    path('workers/new', views.newworker),
    path('workers/add', views.addworker),
    path('workers/<int:id>/edit', views.editworker),
    path('workers/<int:id>/send', views.editworkersend),
    path('workers/<int:id>/delete', views.deleteworker),
    path('clients', views.clients),
    path('clients/new', views.newclient),
    path('clients/add', views.addclient),
    path('clients/<int:id>/edit', views.editclient),
    path('clients/<int:id>/send', views.editclientsend),
    path('clients/<int:id>/delete', views.deleteclient),
    path('newjob', views.newjob),
    path('jobs', views.jobs),
    path('jobs/add', views.addjob),
    path('jobs/<int:id>', views.viewjob),
    path('jobs/<int:id>/edit', views.editjob),
    path('jobs/<int:id>/send', views.editjobsend),
    path('jobs/<int:id>/delete', views.deletejob),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]