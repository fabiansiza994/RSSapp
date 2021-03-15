from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from mainapp.models import CreateRss
from mainapp.forms import RegisterForm
from io import open
from datetime import date
from datetime import datetime
import pathlib
import feedparser

# Create your views here.
def index(request):
    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        register_form.save()

    ruta = str(pathlib.Path().absolute()) + '/log.txt'
    archivo = open(ruta, "a+")
    now = datetime.now()
    datosdb = CreateRss.objects.filter(public=True)
    respuestadata = {}
    for i in range(len(datosdb)):
        con = 0
        while True:
            try:
                respuesta = feedparser.parse(datosdb[i].url)
                print(respuesta['feed']['title'])
                datosdb[i].respuesta = respuesta.entries
                datosdb[i].isError = False
                error = ""
                break
            except Exception as e:
                archivo.write("** A ocurrido un error: "+type(e).__name__+" "+str(now)+"\n")
                con = con+1
                error = "A ocurrido un error al cargrar el feed"
                datosdb[i].isError = True
                datosdb[i].error = error
                if con >= 3:
                    break

    return render(request, 'index.html',{
        'register_form':register_form,
        'datos':datosdb,
        'error':error
        })


@login_required(login_url="login")
def detail(request, id):
    datosdb = CreateRss.objects.get(id=id)
    respuesta = feedparser.parse(datosdb.url)
    return render(request, 'detail.html',{
        'datos':datosdb,
        'entradas': respuesta.entries
    })
def register_page(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Te has registrado correctamente!')
            return redirect('index')
    return render(request, 'users/register.html',{
        'title':'Registro',
        'register_form':register_form
    })

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Datos incorrectos')
    return render(request, 'users/login.html',{
        'title':'Ingresar'
    })

def logout_user(request):
    logout(request)
    return redirect('index')

def save_rss(request):
    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['rss']
        public = request.POST['public']

        Rss = CreateRss(
            title = title,
            url = url,
            public = public
        )

        Rss.save()
        messages.success(request, 'RSS guardado!!')
        return redirect('index')
    else:
        messages.warning(request, 'Error al guardar!!')
        return redirect('index')

def delete_rss(request, id):
    rss = CreateRss.objects.get(id=id)  
    rss.delete()
    messages.success(request, 'RSS Eliminado!!')
    return redirect('index')

