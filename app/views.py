from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
import json
import prueba
from django.views.decorators.csrf import ensure_csrf_cookie
from ast import lista
from c_lexer import Lexer
import traduccion
from c_parser import c_lexer
import c_parser
from traduccion import main
import semantica
import os
import csv
from django.contrib.auth.models import User
from app.models import Curso, Inscritos, Guia, Guia_User, Ejercicio, Ejer_User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import mark_safe

# Create your views here.
@ensure_csrf_cookie
def index_view(request):
	usuario=''
	passwd=''
	existe=''
	curso=''
	if request.method == 'POST':
			if 'username' in request.POST:
				usuario = request.POST['username']
				passwd = request.POST['pass']	
				user = authenticate(username=usuario, password=passwd)
				if user is not None:
				    if user.is_active:
				    	login(request, user)
				    	if 'next' in request.GET:
				    		return HttpResponseRedirect(request.GET['next'])			    	
				    else:
				        existe="no"
			else:
				if 'salir' in request.POST:
					logout(request)
	if request.user.is_authenticated() and not(request.user.is_staff):
		curso=	Inscritos.objects.filter(Alumno=request.user.id).values()[0]["Curso_id"]
		total = Guia.objects.filter(Curso_id=curso).count()
		muestra=[]
		for num in range(0,total):
			muestra.append("Guia")
		existe=muestra

	return render_to_response('index.html',{'existe':existe,'curso':curso},context_instance=RequestContext(request))

@ensure_csrf_cookie
def desLogueo(request):
	if 'salir' in request.POST:
		logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/')
def guias_prg1(request, curso,	nguia):	
	guias = Guia.objects.filter(Curso_id=curso,Numero_Guia=nguia).values()[0]
	guia=guias["Guiahtml"]
	guia=mark_safe(guia)
	guiaid=	guias["id"]
	idalumno=request.user.id
	return render_to_response('guiasprg.html',{'nguia':nguia,'guia':guia,'guiaid':guiaid,'idalumno':idalumno},context_instance=RequestContext(request))

@login_required(login_url='/')
def guias_prg1_calificar(request, curso,	nguia, idalumno):	
	guias = Guia.objects.filter(Curso_id=curso,Numero_Guia=nguia).values()[0]
	guia=guias["Guiahtml"]
	guia=mark_safe(guia)
	guiaid=	guias["id"]
	return render_to_response('guiasprgcalificar.html',{'nguia':nguia,'guia':guia,'guiaid':guiaid, 'idalumno':idalumno,'curso':	curso},context_instance=RequestContext(request))

@ensure_csrf_cookie
def compilador(request):
	lista1 = [ ]
	lt = [ ]
	semantic = [ ]
	traduc = [ ]
	global comp
	Lexer = c_lexer.lexer(request.POST['codigo'])
	for a in json.dumps(Lexer).split(" "):
	   lista1.append(a)
	if "OK" in lista1[4]:

	   parcer = c_parser.main(request.POST['codigo'])
	   for a in json.dumps(parcer).split(" "):
		   lt.append(a)
	   comp = parcer

	   if 'OK' in lt[4]:
		   comp = Lexer
		   tradu = traduccion.main(request.POST['codigo'])
		   for a in json.dumps(tradu).split(" "):
			   traduc.append(a)
			   comp = tradu
	   else:
			comp = parcer
	else:
		comp = Lexer
	return HttpResponse(json.dumps(comp), content_type='application/json')

@ensure_csrf_cookie
def guardarEnviar(request):
	codigo = request.POST['codigo']
	guiaid =request.POST['guiaid']
	npaso =request.POST['nejercicio']
	if Ejer_User.objects.filter(Alumno=request.user.id,Guia=guiaid,Numero_ej=npaso):
		ejerid=Ejer_User.objects.filter(Alumno=request.user.id,Guia=guiaid,Numero_ej=npaso).values()[0]["id"]
		p = Ejer_User(id=ejerid, Alumno_id=request.user.id, Estado=1, Codigo=codigo, Guia_id=guiaid, Numero_ej=npaso)
		p.save()
		existe=1
	else:
		p = Ejer_User(Alumno_id=request.user.id, Estado=1, Codigo=codigo, Guia_id=guiaid, Numero_ej=npaso)
		p.save()
		existe=0
	response_data = {}
	response_data['estado'] = 'correcto'
	response_data['message'] = existe
	return HttpResponse(json.dumps(response_data), content_type='application/json')

@ensure_csrf_cookie
def codigoEjer(request):
	codigo = request.POST['codigo']
	guiaid =request.POST['guiaid']
	npaso =request.POST['nejercicio']
	idalumno =request.POST['idalumno']
	consulta=Ejer_User.objects.filter(Alumno=idalumno,Guia=guiaid,Numero_ej=npaso)
	response_data = {}
	if consulta:
		existe=consulta.values()[0]["Codigo"]
		response_data['estado'] = 'correcto'
		response_data['message'] = existe
	else:
		response_data['estado'] = 'error'
		response_data['message'] = "noguardado"
		
	return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required(login_url='/')
def admin_curso(request):
	if not(request.user.is_staff):
		return HttpResponseRedirect('/')
	curso= Curso.objects.filter(Instructor=request.user.id).values()
	return render_to_response('admincurso.html',{'curso':curso},context_instance=RequestContext(request))

@ensure_csrf_cookie
def guardarCurso(request):
	if request.POST['op']=="guardar":	
		ciclo = int(request.POST['ciclo'])
		nombre = request.POST['nombre']
		descripcion = request.POST['descripcion']
		idusr = int(request.POST['iduser'])
		p = Curso(Ciclo=ciclo, Nombre_Curso=nombre, Descripcion_Curso=descripcion, Instructor_id=idusr)
		p.save()
		idusuario=p.id
	if request.POST['op']=="actualizar":
		id=	int(request.POST['id'])
		ciclo = int(request.POST['ciclo'])
		nombre = request.POST['nombre']
		descripcion = request.POST['descripcion']
		idusr = int(request.POST['iduser'])
		p = Curso(id=id,Ciclo=ciclo, Nombre_Curso=nombre, Descripcion_Curso=descripcion, Instructor_id=idusr)
		p.save()
	if request.POST['op']=="eliminar":
		id=	int(request.POST['id'])
		p = Curso.objects.get(id=id)
		p.delete()
	return HttpResponseRedirect('/admincurso/')

@login_required(login_url='/')
def admin_guias(request,offset):
	if not(request.user.is_staff):
		return HttpResponseRedirect('/')
	guia= Guia.objects.filter(Curso_id=offset).values()
	inscritos=set()
	p=Inscritos.objects.select_related('Alumno').filter(Curso_id=offset)
	for e in p:
		inscritos.add(e.Alumno)

	return render_to_response('adminguias.html',{'guia':guia,'curso':offset,'inscritos':inscritos},context_instance=RequestContext(request))

@ensure_csrf_cookie
def guardarGuia(request):
	if 'idcurso' in request.POST:
		idcurso1 = request.POST['idcurso']
	if request.POST['op']=="guardar":	
		tema = request.POST['tema']
		descripcion = request.POST['descripcion']
		idcurso = int(request.POST['idcurso'])
		numguia = Guia.objects.filter(Curso_id=idcurso1).count()+1
		html='<span class="nombreGuia">'+tema+'</span><input type="hidden" class="npasos" value="0">';
		p = Guia(Numero_Guia=numguia, Tema_Guia=tema, Descripcion_guia=descripcion, Curso_id=idcurso,Guiahtml=html)
		p.save()
	if request.POST['op']=="actualizar":
		id=	int(request.POST['id'])
		numguia = int(request.POST['numguia'])
		tema = request.POST['tema']
		descripcion = request.POST['descripcion']
		idcurso = int(request.POST['idcurso'])
		html=Guia.objects.filter(id=id).values()[0]["Guiahtml"]
		p = Guia(id=id,Numero_Guia=numguia, Tema_Guia=tema, Descripcion_guia=descripcion, Curso_id=idcurso,Guiahtml=html)
		p.save()
	if request.POST['op']=="eliminar":
		id=	int(request.POST['id'])
		p = Guia.objects.get(id=id)
		p.delete()
	return HttpResponseRedirect('/adminguias/'+idcurso1 + '/')

@ensure_csrf_cookie
def guardaInscritos(request):
	opcion = request.POST['opcion']
	response_data = {}
	response_data['message'] = opcion
	if opcion=="2":
		existe = User.objects.filter(username=request.POST['usuario'])
		if not(existe):	
			idcurso = request.POST['idcurso']
			user=User.objects.create_user(request.POST['usuario'],request.POST['correo'],"abcd1234")
			user.first_name=request.POST['nombre']
			user.last_name=request.POST['apellido']
			user.save()
			p = Inscritos(Estado=1,Alumno_id=user.id,Curso_id=int(idcurso))
			p.save()
			response_data['result'] = 'correcto'
			response_data['message'] = "insertar"
	if opcion=="1":
		usuario=User.objects.get(id=request.POST['idalumno'])
		existe = User.objects.filter(username=request.POST['usuario']).exclude(id=request.POST['idalumno'])
		if not(existe):	
			usuario.username=request.POST['usuario']
		usuario.first_name=request.POST['nombre']
		usuario.last_name=request.POST['apellido']
		usuario.email=request.POST['correo']
		usuario.save()
		response_data['result'] = 'correcto'
		response_data['message'] = request.POST['usuario']
		# modificar

	if opcion=="3":
		usuario=User.objects.get(id=request.POST['idalumno'])
		inscrito=Inscritos.objects.get(Alumno_id=int(request.POST['idalumno']), Curso_id=int(request.POST['idcurso']))
		inscrito.delete()
		response_data['result'] = 'correcto'
		response_data['message'] = "eliminar"
	return HttpResponse(json.dumps(response_data), content_type='application/json')
@login_required(login_url='/')
def editorGuias(request, numguia, curso):
	if not(request.user.is_staff):
		return HttpResponseRedirect('/')
	guia=""
	guia=Guia.objects.filter(Curso_id=curso,Numero_Guia=numguia).values()[0]["Guiahtml"]
	guia=mark_safe(guia)
	return render_to_response('editorguias.html',{'guia':guia,'numguia':numguia,'curso':curso},context_instance=RequestContext(request))

@ensure_csrf_cookie
def guardarEjercicios(request):
	datos = request.POST['codigo']
	numguia=request.POST['numguia']
	curso=request.POST['curso']
	
	guia=Guia.objects.filter(Curso_id=curso,Numero_Guia=numguia).values()[0]
	p = Guia(id=guia["id"],Numero_Guia=numguia, Tema_Guia=guia["Tema_Guia"], Descripcion_guia=guia["Descripcion_guia"], Curso_id=curso,Guiahtml=datos)
	p.save()

	
	response_data = {}
	response_data['result'] = 'correcto'
	response_data['message'] = guia["Tema_Guia"]

	return HttpResponse(json.dumps(response_data), content_type='application/json')
	
