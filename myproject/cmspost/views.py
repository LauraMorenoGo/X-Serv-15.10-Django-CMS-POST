from django.shortcuts import render
from .models import Pages
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import get_template
from django.template import Context

formulario = """

<form action="" method="POST">
 Página: <input type="text" name="pag"><br>
 Url: <input type="text" name="url"><br>
 <input type="submit" name="Enviar">
</form>

"""

def autentificar(request):

    logged = ""
    
    if request.user.is_authenticated():
        logged = "Logged in as " + request.user.username + '<br><a href="/admin/logout/">Logout</a><br><a href="/admin/">Añadir o modificar páginas</a><br>'
    else:
        logged = "Not logged in.<br><a href='/admin/login/'>Login</a><br>"
    return logged


def process(request, rec):

    logged = autentificar(request)

    if request.method == "GET":
        try:
            lista = Pages.objects.get(name=rec)
            print (lista.page)
            return HttpResponse(logged + "<br>" + lista.page)
        except Pages.DoesNotExist:
            return HttpResponseNotFound(logged + "<br>La página /" + rec + "no ha sido encontrada en la base de datos")
    elif request.method == "PUT":
        if request.user.is_authenticated():
            try:
                cuerpo = request.body
                lista = Pages.objects.create(name=rec, page=cuerpo)
                lista.save()
                return HttpResponse("Nueva lista creada")
            except:
                return HttpResponseNotFound("Se ha producido un error")
        else:
            return HttpResponseNotFound("Debe autentificarse para continuar")


def process_templates(request, rec):

    respuesta = ""
    logged = autentificar(request)

    if request.method == "GET":
        try:
            lista = Pages.objects.get(name=rec)
            respuesta += lista.page
            plant = get_template('index.html')
            p = Context({'title': logged, 'contenido': respuesta})
            renderiz = plant.render(p)
            return HttpResponse(renderiz)
        except Pages.DoesNotExist:
            return HttpResponseNotFound(respuesta + "<br>La página /" + rec + "no ha sido encontrada en la base de datos")
            
def edit(request, rec):
    
    respuesta = ""
    logged = autentificar(request)
    
    if request.method == "GET":
        try:
            lista = Pages.objects.get(name=rec)
            respuesta += formulario
            return HttpResponse(respuesta)       
        except Pages.DoesNotExist:
            return HttpResponseNotFound(respuesta + "<br>La página /" + rec + "no ha sido encontrada en la base de datos")


def cms_post(request):
    respuesta = ""
    logged = autentificar(request)
    objetos = Pages.objects.all()
    for lista in objetos:
        respuesta += lista.name + " "
        respuesta += lista.page + "<br>"
    plant = get_template('index.html')
    p = Context({'title': logged, 'contenido': respuesta})
    renderiz = plant.render(p)
    return HttpResponse(renderiz)
