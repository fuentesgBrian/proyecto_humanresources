from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)

from .forms import UserRegisterForm
from .models import Employee

# Create your views here.

def inicio(request):
    return render(request, 'humanresources/inicio.html')

def employee_search(request):
    nationalidnumber = request.GET.get('nationalidnumber', '')
    fecha_inicio = request.GET.get('fechainicio')
    fecha_termino = request.GET.get('fechatermino')

    if not (nationalidnumber or fecha_inicio or fecha_termino):
        employees = Employee.objects.all()
    elif nationalidnumber:
        employees = Employee.objects.filter(nationalidnumber__startswith=nationalidnumber)
    elif fecha_inicio and fecha_termino:
        employees = Employee.objects.filter(hiredate__range=[fecha_inicio,fecha_termino])
    
    if nationalidnumber and fecha_inicio and fecha_termino:
        employees = Employee.objects.filter(
            hiredate__range=[fecha_inicio,fecha_termino],
            nationalidnumber__startswith=nationalidnumber
        )

    context = {
        'nationalidnumber':nationalidnumber,
        'fechainicio': fecha_inicio,
        'fechatermino': fecha_termino,
        'employees': employees,
    }
    return render(request, 'humanresources/filtrolista.html', context)

@login_required(login_url='/login/')
def filter_view(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'humanresources/filtrolista.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'registrado satisfactoriamente')
        else:
            messages.error(request, 'Registro invalido. Algunos datos ingresados son incorrectos.')
        return HttpResponseRedirect('/')

    form = UserRegisterForm()
    context = {'register_form':form}
    return render(request, 'humanresources/registro.html', context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"iniciaste sesión como: {username}.")
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "username o password incorrectos.")
                return HttpResponseRedirect('/login')
        else:
            messages.error(request, "username o password incorrectos.")
            return HttpResponseRedirect('/login')
    form = AuthenticationForm()
    context = {'login_form': form}
    return render(request, 'humanresources/login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'Se ha cerrado la sesión satisfactoriamente.')
    return HttpResponseRedirect('/')