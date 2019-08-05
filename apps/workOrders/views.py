from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import date

today = date.today()

def index(request):
    if 'id' in request.session and request.session['id'] != "":
        return redirect('/dashboard')
    User.objects.initialize(request.session)
    return render(request, 'workOrders/index.html')

def dashboard(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        unassigned = Job.objects.filter(status="unassigned", date_assigned=today)
        workers = Worker.objects.all()
        assigned = Job.objects.filter(status="assigned")
        context = {
            'unassigned': unassigned,
            'workers': workers,
            'assigned': assigned
        }
        return render(request, 'workOrders/dashboard.html', context)

def workers(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        workers = Worker.objects.all()
        context = {
            'workers': workers
        }
        return render(request, 'workOrders/workers.html', context)

def newworker(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        return render(request, 'workOrders/newworker.html')

def editworker(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        worker = Worker.objects.get(id=id)
        context = {
            'worker': worker,
        }
        return render(request, 'workOrders/editworker.html', context)

def editworkersend(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        Worker.objects.filter(id=id).update(first_name=request.POST['fname'], last_name=request.POST['lname'], phone_number=request.POST['phone_num'], commission=request.POST['commission'], max_jobs=request.POST['max_jobs'], job_types=request.POST['job_types'])
        return redirect('/workers')

def addworker(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        Worker.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], phone_number=request.POST['phone_num'], commission=request.POST['commission'], job_types=request.POST['job_types'], max_jobs=request.POST['max_jobs'])
        return redirect('/workers')

def deleteworker(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        Worker.objects.filter(id=id).delete()
        return redirect('/workers')

def clients(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        clients = Client.objects.all()
        context = {
            'clients': clients,
        }
        return render(request, 'workOrders/clients.html', context)

def newclient(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        return render(request, 'workOrders/newclient.html')

def addclient(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        Client.objects.create(name=request.POST['name'], address=request.POST['address'], city=request.POST['city'], phone_number=request.POST['phone_num'])
        return redirect('/clients')

def editclient(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        client = Client.objects.get(id=id)
        context = {
            'client': client,
        }
        return render(request, 'workOrders/editclient.html', context)

def editclientsend(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        Client.objects.filter(id=id).update(name=request.POST['name'], address=request.POST['address'], city=request.POST['city'], phone_number=request.POST['phone_num'])
        return redirect('/clients')

def deleteclient(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        Client.objects.filter(id=id).delete()
        return redirect('/clients')

def jobs(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        assigned = Job.objects.filter(status="assigned")
        completed = Job.objects.filter(status="completed")
        cancelled = Job.objects.filter(status="cancelled")
        rescheduled = Job.objects.filter(status="rescheduled")
        context = {
            'assigned': assigned,
            'completed': completed,
            'cancelled': cancelled,
            'rescheduled': rescheduled
        }
        return render(request, 'workOrders/jobs.html', context)

def newjob(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        clients = Client.objects.all()
        workers = Worker.objects.all()
        context = {
            'clients': clients,
            'workers': workers
        }
        return render(request, 'workOrders/newjob.html', context)

def addjob(request):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        if request.POST['worker_id'] == "0":
            client = Client.objects.get(id=request.POST['client_id'])
            Job.objects.create(prop=client, request_by=request.POST['request_by'], job_type=request.POST['job_type'], add_info=request.POST['add_info'], status="unassigned", date_assigned=request.POST['date'])
        else:
            client = Client.objects.get(id=request.POST['client_id'])
            worker = Worker.objects.get(id=request.POST['worker_id'])
            user = User.objects.get(id=request.session['id'])
            Job.objects.create(prop=client, request_by=request.POST['request_by'], employee=worker, job_type=request.POST['job_type'], add_info=request.POST['add_info'], status="assigned", date_assigned=request.POST['date'], assigned_by=user)
        return redirect('/jobs')

def viewjob(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        job = Job.objects.get(id=id)
        context = {
            'job': job,
        }
        return render(request, 'workOrders/viewjob.html', context)


def editjob(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        job = Job.objects.get(id=id)
        print(job.date_assigned)
        clients = Client.objects.exclude(id=job.prop.id)
        if job.employee is not None:
            workers = Worker.objects.exclude(id=job.employee.id)
        else:
            workers = Worker.objects.all()
        context = {
            'clients': clients,
            'workers': workers,
            'job': job,
        }
        return render(request, 'workOrders/editjob.html', context)

def editjobsend(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        if request.POST['worker_id'] == "0":
            client = Client.objects.get(id=request.POST['client_id'])
            Job.objects.filter(id=id).update(prop=client, request_by=request.POST['request_by'], job_type=request.POST['job_type'], add_info=request.POST['add_info'])
        else:
            client = Client.objects.get(id=request.POST['client_id'])
            worker = Worker.objects.get(id=request.POST['worker_id'])
            user = User.objects.get(id=request.session['id'])
            if request.POST['status'] == "0":
                Job.objects.filter(id=id).update(prop=client, request_by=request.POST['request_by'], employee=worker, job_type=request.POST['job_type'], add_info=request.POST['add_info'], status="assigned", date_assigned=request.POST['date'], assigned_by=user)
            else:
                Job.objects.filter(id=id).update(prop=client, request_by=request.POST['request_by'], employee=worker, job_type=request.POST['job_type'], add_info=request.POST['add_info'], status=request.POST['status'], date_assigned=request.POST['date'], assigned_by=user)
        return redirect('/jobs')

def deletejob(request, id):
    if 'id' not in request.session or request.session['id'] == "":
        return redirect('/')
    else:
        Job.objects.filter(id=id).delete()
        return redirect('/jobs')

def register(request):
    errors = User.objects.validation(request.POST, request.session)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        user = User.objects.get(email=request.POST['email'])
        logged_in(request, user)
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login(request.POST)
    if errors is not None:
        for key, value in errors.items():
            messages.warning(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')

def logged_in(request, user):
    request.session['id'] = user.id
    request.session['fname'] = user.first_name
    request.session['lname'] = user.last_name
    request.session['email'] = user.email