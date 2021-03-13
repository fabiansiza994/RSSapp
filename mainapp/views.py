from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from mainapp.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from mainapp.models import CreateRss
import feedparser

# Create your views here.

def index(request):
    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        register_form.save()

    datosdb = CreateRss.objects.filter(public=True)
    respuestadata = {}
    for i in range(len(datosdb)):
        respuesta = feedparser.parse(datosdb[i].url)
        datosdb[i].respuesta = respuesta.entries
    
    return render(request, 'index.html',{
        'register_form':register_form,
        'datos':datosdb
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
        return HttpResponse(f"Se guardo el RSS {title} {url}")
    else:
        return HttpResponse("Error al guardar")

    return HttpResponse(f"llegue")

# def listar_rss(request):
#     rss = CreateRss.objects.all()
#     render(request, 'index.html',{
#         'rss':rss
#     })