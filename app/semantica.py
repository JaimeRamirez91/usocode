#.*-coding:utf-8-*-
__author__ = 'tesis'
from orden_Matrix import orden
import sys
import os
Tablas_simbolos = [ ]
Tablas_global = [ ]
def Tipos_retorno(tabla_individual, Tablas_simbolos):
    error = [ ]
    tipo = [ ]
    contador = 0
    cont = 0
    cont_aux = 0
    elementos = [ ]
    longitud = len (Tablas_simbolos)-1
    while longitud >= contador:
        for tabla in tabla_individual:
            n1 = eval( Tablas_simbolos[contador][5])
            n2 = eval(tabla[3])
            if tabla[2] == Tablas_simbolos[contador][2] and  n1  <  n2 and Tablas_simbolos[contador][0] == tabla[0]:
               tipo = Tablas_simbolos[contador][1]
               id = tabla[2]
               lexpos = tabla[3]
               linea = tabla[4]
               variable = [tipo,id,lexpos,linea]
               elementos.append(variable)
            else:
                pass
        contador = contador + 1

    for datos in elementos:
        if datos[0] == "int":
           pass
        else:
            datos = u"Linea: "+str(datos[3])+u" error tipo invalido %s: se esperaba un int en la variable '%s' ."  % (datos[0],datos[1])
            error.append(datos)
    return  error


def error_operacion_numero(Matriz):
    respuesta = [ ]
    for lista in Matriz:
        if str(lista[2]).isdigit()==True:
            respuesta.append(lista)
        else:
            pass
    if respuesta == [ ]:
        nula = ['None', 'null', 'null', '0','0']
        respuesta.append(nula)
    return respuesta

def error_tipo(Matriz):
    error_retorno = [ ]
    for lista in Matriz:
        if Matriz [0][0] == lista[0]:
            pass
        else:
       #     error = u"Linea: "+str(lista[3])+u" error: la variable: '"+str(lista[1])+u"' de tipo: "+str(lista[0])+u" no se puede convertir a tipo: "+str(Matriz[0][0])+". "
            error = u"Linea: "+str(lista[3])+u" error: incompatibilidad de tipos entre la variable: '"+str(lista[1])+u"' de tipo: "+str(lista[0])+u" y la variable "+str(Matriz[0][1])+u"  tipo: "+str(Matriz[0][0])+". "
            error_retorno.append(error)
    try:
        return  error_retorno[0]
    except:
        return  error_retorno
   #     tipo_verificacion_numero_string = lista[0]
        error_retorno.append(tipo_verificacion_numero_string)
        return  error_retorno


def burbuja(Matriz):
    lista = [ ]
    long = len(Matriz)
    cont = 0
    while long >= cont:
        try:
            lista.append(Matriz[cont][2])
        except:
            pass
        cont = cont+1
    numero = len(lista)
    i=0
    while i < numero:
        j = i
        while j < numero:
            if lista[i] > lista[j]:
                temp = lista[i]
                lista[i] = lista[j]
                lista[j] = temp
            j = j+1
        i = i+1
#-------------------------- falta------------------------------------------------------------------------
    a = len(Matriz)
    i = 0
    contador = 0
    listaord = []
    lista2 = []
    try:
        while (i < a):
            j = i
            while (j < a):
                for m in Matriz:
                    e = str(lista[contador])
                    if e in m:
                        if contador == a:
                            pass
                        else:
                            contador +=1
                            listaord.append(m)
                    else:
                        pass
                j=j+1
            i = i+1
    except:
        pass
    return listaord



#-------------------  ordenarlas por lista y encontrar el error-----------------------------------------



#----------------------------------------------------------------------
def Tipos(tabla_individual, Tablas_simbolos,):
    tipo = [ ]
    contador = 0
    cont = 0
    cont_aux = 0
    elementos = [ ]
    longitud = len (Tablas_simbolos)-1
    while longitud >= contador:
        for tabla in tabla_individual:
            n1 = eval( Tablas_simbolos[contador][5])
            n2 = eval(tabla[3])
            if tabla[2] == Tablas_simbolos[contador][2] and  n1  <  n2 and Tablas_simbolos[contador][0] == tabla[0]:
               tipo = Tablas_simbolos[contador][1]
               id = tabla[2]
               lexpos = tabla[3]
               linea = tabla[4]
               variable = [tipo,id,lexpos,linea]
               elementos.append(variable)

            else:
                pass
        contador = contador + 1
    auxiliar_error_burbuja = error_operacion_numero(tabla_individual)
    if str(auxiliar_error_burbuja[0][2]).isdigit()==True:
       for a in auxiliar_error_burbuja:
            tipo = 'int'
            id =  a[2]
            lexpos = a[3]
            numero = a[4]
            lista = [tipo,id,lexpos,numero]
            elementos.append(lista)
    else:
        pass
 #   error detected en  burbuja
    elementos = burbuja(elementos)
    elementos = error_tipo(elementos)
    return elementos

#----------------------------------------------------------------------
def semantica(Tablas_simbolos, Tablas_global, Tablas_fundec,Tabla_verificacion_tipos,Tabla_verificacion_tipos_return):
    error_semantico = [ ]
    estado = False
    filas = len(Tablas_simbolos)
    a = 0
    Tablas_simbolos = orden().metodo(Tablas_simbolos)
    a = len(Tablas_simbolos)
    i=0
    c=0
    for x in range(0,filas):
        try:
#-----------------------------------------------------------------------------------------------
            com = orden().existencia(Tablas_simbolos[c],Tablas_simbolos)
            valor_a_comparar = orden().Coincidencia(Tablas_simbolos[c],Tablas_simbolos)
            lista_comparar = orden().Val_com(valor_a_comparar)

#------------------------------------------------------------------------------------------------
#-------------------------aqui se buscan las dobles declaraciones--------------------------------
            error = orden().error(lista_comparar, com)
            if error is None:
                pass
            else:
               error_semantico.append(error)
            if lista_comparar[0][3].isdigit() == True:
                pass
            else:
                a =  str(lista_comparar[0][3])
                line =  str(lista_comparar[0][5])
                funcion = lista_comparar[0][0]
                comb = funcion +" "+ a+" "+line
                id = orden().existencia_id(a ,Tablas_simbolos)
                Global_id_dec = orden().ordenar_lt_global(Tablas_global)
                #-------------------------------------------------------
                #------------------mod----------------------------------
                Fun_id_dec = orden().ordenar_lt(Tablas_fundec)
                lista_comb = [ ]
                for x in comb.split(" "):
                    lista_comb.append(x)
                existencia = orden().error_tipo_id_1(lista_comb,id)
                if existencia == [ ]:
                    pass
                else:
                    if lista_comparar[0][3] in Global_id_dec:
                        pass
#---------------------------------mod----------------------------------------------------------
                    else:
                        estado = False
                        for x in Fun_id_dec:
                         if lista_comparar[0][0] == x [0] and lista_comparar[0][3] == x[1]:
                                estado = True
                        if estado == True:
                            pass
                        else:

                            numero =  eval(lista_comparar[0][4])
                            a = "Linea: "+str(numero)+" Error:  ' "+str(lista_comparar[0][3])+" '  no esta daclarada."
                            error_semantico.append([a])
        except:
            pass
        c=c+1



#-----------------------------------------error tipos----------------------------------------------------------------------------------
    if error_semantico == [ ]:
       error_Numerico_tipo_cadena = ""
       for individual in Tabla_verificacion_tipos:
           a  = Tipos(individual,Tablas_simbolos)
           try:
               b = error_operacion_numero(individual)
               if str(b[0][2]).isdigit() == True and  a[0] == "string":
                   error_semantico.append(["No se permiten enteros en las operaciones de tipo cadena(string)"])
           except:
               pass
           if a == [ ]:
               pass
           else:
               error_semantico.append([a])
#--------------------------------en funcionesverificacion de return---------------------------------------------------------------------------------------

    if error_semantico == [ ]:
       error_return = ""
       a = Tipos_retorno(Tabla_verificacion_tipos_return,Tablas_simbolos)
       if a == [ ]:
           pass
       else:
           for error in a:
               error_semantico.append([error])
    try:
        return error_semantico[0]
    except:
        return error_semantico


def main(Tablas_simbolos,Tablas_global, Tablas_fundec,Tabla_verificacion_tipos,Tabla_verificacion_tipos_return):
    respuesta = [ ]
    vacio = [ ]
    e = semantica(Tablas_simbolos,Tablas_global, Tablas_fundec,Tabla_verificacion_tipos,Tabla_verificacion_tipos_return)
    a = semantica(Tablas_global, vacio, vacio,vacio,vacio)
    if  a == [ ]:
        if  e == [ ]:
            respuesta = [ ]
        else:
            respuesta = e
    else:
        respuesta= a
    return respuesta