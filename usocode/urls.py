"""usocode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import index_view, guias_prg1, compilador,admin_guias,guardarGuia,desLogueo,admin_curso,guardarCurso,guardaInscritos,editorGuias,guardarEjercicios,guardarEnviar,codigoEjer,guias_prg1_calificar

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index_view),
    url(r'^guias/prg/(\d{1,2})/(\d{1,2})/$',guias_prg1),
    url(r'^guias/prg/(\d{1,2})/(\d{1,2})/(\d{1,2})/$',guias_prg1_calificar),
    url(r'^compilador/$',compilador),
    url(r'^guardarEnviar/$',guardarEnviar),
    url(r'^codigoEjer/$',codigoEjer),
    url(r'^adminguias/(\d{1,2})/$',admin_guias),
    url(r'^guardarguia/$',guardarGuia),
    url(r'^guardaInscritos/$',guardaInscritos),
    url(r'^admincurso/$',admin_curso),
    url(r'^guardarCurso/$',guardarCurso),
    url(r'^guardarEjercicios/$',guardarEjercicios),
    url(r'^editorguias/(\d{1,2})/(\d{1,2})/$',editorGuias),
    url(r'^logout/$',desLogueo),

]

handler404 = 'mysite.views.index_view'
