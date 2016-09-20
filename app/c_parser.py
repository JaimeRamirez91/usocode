#.*-coding:utf-8-*-
# me quede en la 1,016
#-----------------------------imports------------------------------------#
from sys import exit
import ply.yacc as yacc
import sys
import os
from Busquedas_reg import Busqueda
import re
import c_lexer
from c_lexer import Lexer
import semantica
from orden_Matrix import orden
from ast import Node
tokens = Lexer.tokens
#---------------------------------------------------------------------------
#**************************************************************************#
#-------------------------------Ambitos------------------------------------#
Tablas_global = [ ]
Tablas_simbolos = [["FUN","TYPE","PLDSH","0","LINEA","0"],]
Tablas_simbolos_funciones_dec = [["FUN","TYPE","PLDSH","0","LINEA","0"],]
funciones = [ ]
funciones_programadas = [ ]
Tabla_verificacion_tipos = [ ]
Tabla_verificacion_tipos_return = [ ]
includes = ["iostream","math.h",]
using_std = ["using namespace std"]
includes_dec = [ ]
using_std_dec = [  ]
includes_verificacion = [ ]
#---------------------verificacion id funciones----------------------------------
lista_de_id_funciones = [ ]
#***************************************************************************#
#--------------------------------Errores------------------------------------#
error_parser = [ ]
#***************************************************************************#
#---------------------------expreciones regulares---------------------------#
id = r'\w+(_\d\w)*'
id2 = r'[a-z]*'
int = r'int+[ ?]*'
char = r'char+[ ?]*'
espacio  = r' '
Linea  = r'Linea'
digito = r'\d*'
igual_int = r'='
ID = r'ID'
#*****************************************************************************#
#------------------------Concatenacion de expreciones-------------------------#
t_buscar_id = str(ID)+str(espacio)+str(id)+str(espacio)+str(digito)
t_var_int = str(int)+str(espacio)+str(id)+str(espacio)+str(igual_int)+str(espacio)+str(digito)+str(espacio)+str(digito)+str(espacio)+str(digito)
t_var_int_id = str(int)+str(id)+str(espacio)+str(igual_int)+str(espacio)+str(id)+str(espacio)+str(Linea)+str(espacio)+str(digito)
#*****************************************************************************#
#-----------Analisis sintactico p1- generacion tabla de simbolos--------------#

def p_programa(p):
    '''programa : encabezado dec_lst funciones
    | encabezado funciones
    | dec_lst funciones
    | funciones
    '''
    if includes_dec == [ ]:
        pass
    else:
        for includ in includes_dec:
            if includ in includes:
                pass
            else:
                error = u"Error: la libreria: "+str(includ)+u" no está implementada en USOCODE o no existe, Librerias soportadas: iostream y math."
                error_parser.append(error)
#--------------funciones_programadas: trae las funciones programadas-----------#
#--------------funciones: trae las funciones declaradas en la cabesera---------#
#--------------Validacion 1) funciones declaradas-programadas------------------#
    for x in funciones:
        if x in funciones_programadas:
            pass
        else:
            if x =="int main();":
                error = u"La función: "+str(x)+u" no se encuentra implemantada y es critica para la ejecución del programa."
                error_parser.append(error)
            else:
                pass
#--------------------validacion 2) funciones programadas repetidas-----------------#
    for x in funciones_programadas:
       try:
           a = 0
           a = funciones_programadas.count(x)
       except:
           pass
       try:
            if a == 0:
                pass
            elif a > 1:
                error = u"La funcion: "+str(x)+u" está programada múltipes ocaciones."
                error_parser.append(error)
            else:
                pass
       except:
            pass

#--------------------validacion 2) funciones declaradasdas repetidas-----------------#
    for x in funciones:
        y = funciones.count(x)
        if y > 1:
           error = u"Error: "+u"doble dacalarión de la funcion: '"+str(x)+u"' , verifique el bloque de declaración de funciones."
           error_parser.append(error)



#--------------------validacion 3) funciones programadas-declaradas-----------------#
    for x in funciones_programadas:
        if x in funciones:
            pass
        else:
            error = u"Error: opción: 1) La función: "+  x  +u" está implementada y no se encuentra declarada <br> 2) número de parametros incorrecto !!int!!."
            error_parser.append(error)
    try:
#----------------------------Captura de declaraciones globales -----------------------------#
        mi_l = [ ]
        contador = 0
        if p[2] is not None or  p[2].type == "dec_lst":
           if p[2].type == "dec_lst":
                contenido = str(p[2])
                for m in re.finditer(t_var_int , contenido):
                    var = '%s' % (m.group(0))

                    for m in re.finditer(id , var):
                         var = '%s' % (m.group(0))
                         if contador == 0:
                             mi_l.append("Global")
                         mi_l.append(var)
                         contador +=1
                         if contador >= 5 :
                               Tablas_global.append(mi_l)
                               contador = 0
                               vacio = [ ]
                               mi_l = vacio
#----------------------mod id =id global--------------------------------------------------
                respuesta_id = Busqueda().buscar_id(contenido,"Global")
                for lista in respuesta_id:
                    Tablas_global.append(lista)

           elif p[1] is not None and  p[1].type == "dec_lst" :
                contenido = str(p[1])
                for m in re.finditer(t_var_int , contenido):
                    var = '%s' % (m.group(0))
                    for m in re.finditer(id , var):
                         var = '%s' % (m.group(0))
                         if contador == 0:
                             mi_l.append("Global")
                         mi_l.append(var)
                         contador +=1
                         if contador >= 5 :
                               Tablas_global.append(mi_l)
                               contador = 0
                               vacio = [ ]
                               mi_l = vacio
#----------------------mod id =id global--------------------------------------------------
                respuesta_id = Busqueda().buscar_id(contenido,"Global")
                for lista in respuesta_id:
                    Tablas_global.append(lista)

           else:
               pass

    except:
          pass



#----------------------------interaccion con la semantica------------------------------------------------------
    if error_parser == [ ]:
       error = semantica.main(Tablas_simbolos,Tablas_global, Tablas_simbolos_funciones_dec,Tabla_verificacion_tipos,Tabla_verificacion_tipos_return)
       try:
          a = error[0]
          error_parser.append(a)
       except:
           pass
#---------------------------------------------------------------------------------------------------------------
def p_dec_lst(p):
    '''dec_lst : dec_lst declaracionfun
    |  declaracionfun
    '''
    try:
        if p[1].type == "dec_lst":
            if p[1] is None:
               sub = str(p[2])
            else:
               sub = str(p[1].sub)+str(p[2])
        else:
            sub = str(p[1])
        p[0] = Node("dec_lst",  sub)
    except:
        pass

def p_funciones(p):
    '''funciones : tipo ID PARENTESISIZQUIERDO  PARENTESISDERECHO  LLAVEIZQUIERDA todo  LLAVEDERECHA
    | tipo ID PARENTESISIZQUIERDO paramdec  PARENTESISDERECHO  LLAVEIZQUIERDA todo  LLAVEDERECHA
    '''
    if p[1] == "int":
        if len(p) == 8:
        #-----------------------------captura de funciones--------------------------------------------------#
            add = str(p[1])+" "+str(p[2])+str(p[3])+str(p[4])+";"
            funciones_programadas.append(add)
        #---------------------------------------Reclolectando Int id = numero ;---------------------------------------------
            contenido = str(p[6])
            funcion = str(p[2])
            respuesta = Busqueda().buscar_int(contenido, funcion)
            for recorrido in respuesta:
                Tablas_simbolos.append(recorrido)
        #---------------------------------------------------------------------------------------------------------------------
        #---------------------------------------Reclolectando string = id y  string = numero ;---------------------------------------------
            respuesta_str_id_1 = Busqueda().buscar_str_id(contenido, funcion)
            for recorrido in respuesta_str_id_1:
                Tablas_simbolos.append(recorrido)
        #---------------------------------------Reclolectando int = id ;---------------------------------------------
            respuesta_id = Busqueda().buscar_id(contenido, funcion)
            for recorrido in respuesta_id:
                Tablas_simbolos.append(recorrido)
        #---------------------------------------Verificando todos los id individuales------------------------------------------------------
            respuesta_ID = Busqueda().buscar_ID(contenido, funcion)
            for recorrido in respuesta_ID:
                    Tablas_simbolos.append(recorrido)
        #---------------------------------------------------------------------------------------------------------------------
            funcion_name = str(p[1])+" "+str(p[2])+str(p[3])+str(p[4])+str(p[5])
            p[0] = Node("Funcion",  contenido, funcion_name)
        #--------------------------------verificacion de tipos-------------------------------------------------------------------
            operaciones = Busqueda().buscar_op(contenido,funcion)
            for op in operaciones:
                Tabla_verificacion_tipos.append(op)

        #--------------------------------verificacion de tipos return-------------------------------------------------------------------
            operacion = Busqueda().busqueda_return(contenido,funcion)
            for ops in operacion:
                Tabla_verificacion_tipos_return.append(ops)
        else:
                #-----------------------------captura de funciones--------------------------------------------------#
        #-----------------------------sustitucion de declaraciones por id-----------------------------------#
            add_lst_final = [ ]
            add_lst = [ ]
            variables = [ ]
            linea = [ ]
            global cont
            cont  = str(p[4])
            cont2 = cont
            cont2 = cont2.replace("int"," ")
            cont2 = cont2.replace(","," ")
            for m in re.finditer(digito, cont2):
                var = '%s' % (m.group(0))
                if var.isdigit() == True:
                    linea.append(var)
            numero = linea[0]
            cont2 = cont2.replace(numero," ")
            for m in re.finditer(id, cont2):
                var = '%s' % (m.group(0))
                variables.append(var)
            variable_count = 0
            variable_len =len(variables)
            while variable_len > variable_count:
                x = variables[variable_count]
                comparacion =  variables.count(x)
                if comparacion > 1 :
                   pass
                   error = "Linea: "+str(linea[0])+", el id: "+str(variables[variable_count])+"  está declarada multilpes ocaciones en el mismo ambito."
                   error_parser.append(error)
                variable_count= variable_count+1
        #------------------------------------------------------------------
        #----------------Creacion del ambito de declaracion de funciones---
            concatenacion = ""
            variable_fin = [ ]
            buscar_int_auxiliar = [ ]
            for v in variables:
               if str(v).isdigit():
                   variable_fin = variable_fin
               else:
                    variable_fin.append(v)
                    concatenacion = concatenacion +" "+str(p[2])+" "+" int "+v+" = 0  0 "+linea[0]
            funcion = str(p[2])
            resp = Busqueda().buscar_int_fun_dec(concatenacion , funcion)
            for add in resp:
                Tablas_simbolos_funciones_dec.append(add)

            l = len(variable_fin)-1
            code_plus = 0;
            parametro =""
            for var in variable_fin:
                if code_plus == l:
                    parametro = parametro+"int"
                else:
                    parametro = parametro+"int"+","
                code_plus = code_plus + 1
            add = str(p[1])+" "+str(p[2])+str(p[3])+str(parametro)+str(p[5])+";"

            funciones_programadas.append(add)
        #-------------------------------------------fin captura de funciones-----------------------------------#
        #----------------------------------------------------------------------------------------------------
            mi_l = [ ]
            contador = 0
            contenido = str(p[7])
            funcion = str(p[2])
            respuesta = Busqueda().buscar_int(contenido, funcion)
            for recorrido in respuesta:
                Tablas_simbolos.append(recorrido)

        #---------------------------------------Reclolectando string = id  y string = 0;---------------------------------------------
            respuesta_str_id = Busqueda().buscar_str_id(contenido, funcion)
            for recorrido in respuesta_str_id:
                Tablas_simbolos.append(recorrido)

        #---------------------------------------------------------------------------------------------------------------------
        #---------------------------------------Reclolectando int = id ;---------------------------------------------
            respuesta_id = Busqueda().buscar_id(contenido, funcion)
            for recorrido in respuesta_id:
                Tablas_simbolos.append(recorrido)

        #---------------------------------------Verificando todos los id individuales------------------------------------------------------
            respuesta_ID = Busqueda().buscar_ID(contenido, funcion)
            for recorrido in respuesta_ID:
                    Tablas_simbolos.append(recorrido)
        #---------------------------------------------------------------------------------------------------------------------
            funcion_name = str(p[1])+" "+str(p[2])+str(p[3])+str(p[4])+str(p[5])+str(p[6])+str(p[7])+str(p[8])
            p[0] = Node("Funcion",  funcion_name)
        #--------------------------------verificacion de tipos-------------------------------------------------------------------
            operaciones = Busqueda().buscar_op(contenido,funcion)
            for op in operaciones:
                Tabla_verificacion_tipos.append(op)

        #--------------------------------verificacion de tipos return-------------------------------------------------------------------
            operacion = Busqueda().busqueda_return(contenido,funcion)
            for ops in operacion:
                Tabla_verificacion_tipos_return.append(ops)




    else:
         error = "Linea: "+str(p.lineno(2))+u" error: tipo ' %s' no valido para funciones en usocode o el tipo no existe." % p[1]
         error_parser.append(error)
         p[0] = Node("Funcion", error )


def p_funciones_1(p):
    """funciones : funciones  tipo ID PARENTESISIZQUIERDO  PARENTESISDERECHO LLAVEIZQUIERDA todo LLAVEDERECHA
    """
#-----------------------------captura de funciones--------------------------------------------------#
    add = str(p[2])+" "+str(p[3])+str(p[4])+str(p[5])+";"
    funciones_programadas.append(add)
#----------------------------------------------------------------------------------------------------

    mi_l = [ ]
    contador = 0
    contenido = str(p[7])
    funcion = str(p[3])
    respuesta = Busqueda().buscar_int(contenido, funcion)
    for recorrido in respuesta:
        Tablas_simbolos.append(recorrido)

#---------------------------------------Reclolectando string = id ; y string = 0  ---------------------------------------------
    respuesta_str_id = Busqueda().buscar_str_id(contenido, funcion)
    for recorrido in respuesta_str_id:
        Tablas_simbolos.append(recorrido)

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------Reclolectando int = id ;---------------------------------------------
    respuesta_id = Busqueda().buscar_id(contenido, funcion)
    for recorrido in respuesta_id:
        Tablas_simbolos.append(recorrido)
#---------------------------------------Reclolectando string = id ; y string = 0  ---------------------------------------------
    respuesta_str_id = Busqueda().buscar_str_id(contenido, funcion)
    for recorrido in respuesta_str_id:
        Tablas_simbolos.append(recorrido)
#---------------------------------------Verificando todos los id individuales------------------------------------------------------
    respuesta_ID = Busqueda().buscar_ID(contenido, funcion)
    for recorrido in respuesta_ID:
            Tablas_simbolos.append(recorrido)
#---------------------------------------------------------------------------------------------------------------------
    funcion_name = str(p[2])+" "+str(p[3])+str(p[4])+str(p[5])+str(p[6])

#--------------------------------verificacion de tipos-------------------------------------------------------------------
    operaciones = Busqueda().buscar_op(contenido,funcion)
    for op in operaciones:
        Tabla_verificacion_tipos.append(op)

#--------------------------------verificacion de tipos return-------------------------------------------------------------------
    operacion = Busqueda().busqueda_return(contenido,funcion)
    for ops in operacion:
        Tabla_verificacion_tipos_return.append(ops)

    p[0] = Node("Funcion",  contenido, funcion_name)

def p_funciones_2(p):
    '''funciones : funciones tipo ID PARENTESISIZQUIERDO paramdec  PARENTESISDERECHO  LLAVEIZQUIERDA todo  LLAVEDERECHA
    '''
#-----------------------------captura de funciones--------------------------------------------------#
#-----------------------------sustitucion de declaraciones por id-----------------------------------#
    if p[2] == "int":
        add_lst_final = [ ]
        add_lst = [ ]
        variables = [ ]
        linea = [ ]
        global cont
        cont  = str(p[5])
        cont2 = cont
        cont2 = cont2.replace("int"," ")
        cont2 = cont2.replace(","," ")
        for m in re.finditer(digito, cont2):
            var = '%s' % (m.group(0))
            if var.isdigit() == True:
                linea.append(var)
        numero = linea[0]
        cont2 = cont2.replace(numero," ")
        for m in re.finditer(id, cont2):
            var = '%s' % (m.group(0))
            variables.append(var)
        variable_count = 0
        variable_len =len(variables)
        while variable_len > variable_count:
            x = variables[variable_count]
            comparacion =  variables.count(x)
            if comparacion > 1 :
               pass
               error = "Linea: "+str(linea[0])+", el id: "+str(variables[variable_count])+"  está declarada multilpes ocaciones en el mismo ambito."
               error_parser.append(error)
            variable_count= variable_count+1
        concatenacion = ""
        variable_fin = [ ]
        buscar_int_auxiliar = [ ]
        for v in variables:
           if str(v).isdigit():
               variable_fin = variable_fin
           else:
                variable_fin.append(v)
                concatenacion = concatenacion +" "+str(p[3])+" "+" int "+v+" = 0  0 "+linea[0]
        funcion = str(p[3])
        resp = Busqueda().buscar_int_fun_dec(concatenacion , funcion)
        for add in resp:
            Tablas_simbolos_funciones_dec.append(add)

        l = len(variable_fin)-1
        code_plus = 0;
        parametro =""
        for var in variable_fin:
            if code_plus == l:
                parametro = parametro+"int"
            else:
                parametro = parametro+"int"+","
            code_plus = code_plus + 1
        add = str(p[2])+" "+str(p[3])+str(p[4])+str(parametro)+str(p[6])+";"
        funciones_programadas.append(add)
    #-------------------------------------------fin captura de funciones-----------------------------------#
    #----------------------------------------------------------------------------------------------------
        mi_l = [ ]
        contador = 0
        contenido = str(p[8])
        funcion = str(p[3])
        respuesta = Busqueda().buscar_int(contenido, funcion)
        for recorrido in respuesta:
            Tablas_simbolos.append(recorrido)
    #---------------------------------------------------------------------------------------------------------------------
    #---------------------------------------Reclolectando int = id ;---------------------------------------------
        respuesta_id = Busqueda().buscar_id(contenido, funcion)
        for recorrido in respuesta_id:
            Tablas_simbolos.append(recorrido)

    #---------------------------------------Verificando todos los id individuales------------------------------------------------------
        respuesta_ID = Busqueda().buscar_ID(contenido, funcion)
        for recorrido in respuesta_ID:
                Tablas_simbolos.append(recorrido)
    #---------------------------------------------------------------------------------------------------------------------
#---------------------------------------Reclolectando string = id ; y string = 0  ---------------------------------------------
        respuesta_str_id = Busqueda().buscar_str_id(contenido, funcion)
        for recorrido in respuesta_str_id:
            Tablas_simbolos.append(recorrido)
    #--------------------------------verificacion de tipos-------------------------------------------------------------------
        operaciones = Busqueda().buscar_op(contenido,funcion)
        for op in operaciones:
            Tabla_verificacion_tipos.append(op)

#--------------------------------verificacion de tipos return-------------------------------------------------------------------
        operacion = Busqueda().busqueda_return(contenido,funcion)
        for ops in operacion:
            Tabla_verificacion_tipos_return.append(ops)






        funcion_name = str(p[1])+" "+str(p[2])+str(p[3])+str(p[4])+str(p[5])+str(p[6])+str(p[7])+str(p[8])+str(p[9])
        p[0] = Node("Funcion",  funcion_name)


    else:
         error = "Linea: "+str(p.lineno(3))+u" error: tipo ' %s' no valido para funciones en usocode o el tipo no existe." % p[2]
         error_parser.append(error)
         p[0] = Node("Funcion", error )



def p_parametros(p):
    """parametros : parametros COMA ID
                  | parametros COMA NUMBER
                  | ID
                  | NUMBER
                  """
    try:
        a = p[3]
        var = p[3]
        sub = str(p[1])+","+(p[3])
    except:
        try:
           a = p[1]
           sub = str(p[1])
        except:
            pass
    p[0] = Node("parametrosfun", sub)

def p_pram_dec(p):
    """paramdec : paramdec COMA tipo ID
                  | paramdec COMA tipo NUMBER
                  | tipo ID
                  | tipo NUMBER
                  """
    try:
        a = p[4]
        if p[3] == "int":
            sub = str(p[1])+","+str(p[3])+" "+str(p[4])
        else:
            sub = " "
            error = "Linea: "+str(p.lineno(4))+u" tipo: ' %s ' invalido o no implementado en USOCODE para pasar parametros." % p[3]
            error_parser.append(error)
    except:
        try:
            a= p[2]
            if p[1] == "int":
               sub = str(p[1])+" "+str(p[2])
            else:
               sub = " "
               error = "Linea: "+str(p.lineno(2))+u" tipo: ' %s ' invalido o no implementado en USOCODE para pasar parametros." % p[1]
               error_parser.append(error)
        except:
            pass
    sub = sub+" "+str(p.lexer.lineno)
    p[0] = Node("parametrosfun", sub)

#----------------------------------Declaraciones validas de funciones--------------------------------------------------
def p_pram_declaracion(p):
    """paramdeclaraciones : paramdeclaraciones COMA tipo
                  | tipo
                  """
    try:
        a = p[3]
        sub = str(p[1])+","+str(p[3])
    except:
        try:
            a= p[1]
            sub = str(p[1])
        except:
            pass
    p[0] = Node("parametrosfun", sub)

#-------------------------------------------new----------------------------------
def p_pram_declaracion_1(p):
    """paramcallfun : paramcallfun COMA ID
                  | paramcallfun COMA NUMBER
                  | ID
                  | NUMBER
                  """
    try:
        a = p[3]
        sub = str(p[1])+","+str(p[3])
    except:
        try:
            a= p[1]
            sub = str(p[1])
        except:
            pass
    p[0] = Node("parametrosfun", sub)

#----------------------end mod--------------------------------------------------------
def p_funciones_ERROR(p):
    '''funciones : funciones tipo ID PARENTESISIZQUIERDO  PARENTESISDERECHO  LLAVEIZQUIERDA   LLAVEDERECHA
    |  tipo ID PARENTESISIZQUIERDO  PARENTESISDERECHO  LLAVEIZQUIERDA   LLAVEDERECHA
    '''
    try:
        a = p[7]
        pass
        er = u"Linea: "+str(p.lineno(3))+u" Funcion: '"+str(p[3])+u"', estado: vacio, (no contiene declaraciones-instrucciones), <br> opciones: elimine la función o programe instrucciones."
        error_parser.append(er)
    except:
        pass
        er = u"Linea: "+str(p.lineno(2))+u" Funcion: '"+str(p[2])+u"', estado:  vacio, (no contiene declaraciones-instrucciones). <br> opciones: elimine la función o programe instrucciones."
        error_parser.append(er)

    #exit(1)

def p_todo(p):
    ''' todo : todo cout
    | todo declaracion
    | todo cin
    | todo dec
    | todo inc
    | todo seleccion
    | todo iteracion
    | todo repeticion
    | todo operaciones
    | todo callfun
    | todo return
    | todo powgen
    | powgen
    | declaracion
    | cout
    | cin
    | dec
    | inc
    | seleccion
    | iteracion
    | repeticion
    | operaciones
    | callfun
    | return
    '''
    if p[1].type == "todo":
        if p[1] is None:
           sub = str(p[2])
        else:
           sub = str(p[1].sub)+str(p[2])
    else:
        sub = str(p[1])
    p[0] = Node("todo",  sub)
#-----------------------------------------------------------------------------------------
def p_encabezado(p):
    'encabezado : encabezado lib'
    p[0] = Node("encabezado",p[2])
#---------------------------------llamada de funciones declaradas-------------------------$

def p_call_fun(p):
    '''callfun : callfun ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    | ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    '''
    try:
        exit = p[5]
        buscar = "int "+str(p[2])+str(p[3])+str(p[4])+str(p[5])
        if buscar in funciones:
            pass
        else:
            error =u"Linea: "+str(p.lineno(2))+u" error: la funcion recibe un número distinto de paramatros o la función:"+buscar+u" no está declarada"
            error_parser.append(error)
    except:
         buscar = "int "+str(p[1])+str(p[2])+str(p[3])+str(p[4])
         if buscar in funciones:
            pass
         else:
            error =u"Linea: "+str(p.lineno(1))+u" error: la función recibe un número distinto de paramatros o la función:"+buscar+u" no está declarada"
            error_parser.append(error)
def p_call_fun_2(p):
    '''callfun : callfun ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO PUNTOYCOMA
    | ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO PUNTOYCOMA
    '''

    try:
        list_aux = [ ]
        variables =""
        contador = 0

        exit = p[6]
        parametro =""
        AUXILIAR = str(p[4])
        for au in AUXILIAR.split(","):
           aux = au.replace(au,"int")
           list_aux.append(aux)
           var = "ID "+au+" "+str(p.lexpos(2))
           parametro = parametro+var
        local_len = len(list_aux)-1
        for aux in list_aux:
             if contador < local_len:
                variables = variables+aux+","
             else:
                 variables = variables+aux
             contador = contador + 1

        buscar = "int "+str(p[2])+str(p[3])+str(variables)+str(p[5])+str(p[6])
        if buscar in funciones:
            p[0] = str(p[1])+" "+parametro
            pass
        else:
            error =u"Linea: "+str(p.lineno(2))+u" Error la función: "+buscar+u" no está declarada, o verifique la cantidad de parametros, cantidad invalida(verifique la cantidad)."
            error_parser.append(error)
    except:
        try:
             list_aux = [ ]
             exit = p[5]
             parametro =""
             variables =""
             contador = 0
             AUXILIAR = str(p[3])
             for au in AUXILIAR.split(","):
                 aux = au.replace(au,"int")
                 list_aux.append(aux)
                 var = "ID "+au+" "+str(p.lexpos(1))
                 parametro = parametro+var
             local_len = len(list_aux)-1
             for aux in list_aux:
                 if contador < local_len:
                     variables = variables+aux+","
                 else:
                     variables = variables+aux
                 contador = contador + 1
             buscar = "int "+str(p[1])+str(p[2])+str(variables)+str(p[4])+str(p[5])
             if buscar in funciones:
                p[0] = Node("ID",parametro)
             else:
                error =u"Linea: "+str(p.lineno(1))+u" Error la función:"+buscar+u" no está declarada, o verifique la cantidad de parametros invalida(verifique la cantidad)."
                error_parser.append(error)
        except:
            pass
#-----------------------------------------------------------------mod opvaaaa--------------------------------------------------------------------------------------------
def p_callcout(p):
    '''callcout : callcout pow
    | pow
    '''
    if len(p)== 3:
        todo = str(p[1])+str(p[2])
    elif len(p)==2:
        todo = str(p[1])
    p[0] = Node("parametros", todo, p[1])


def p_callcout_1(p):
    '''callcout : callcout ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO
    | ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO
    '''
    try:
        a = p[5]
        error = u"Liena: "+str(p.lineno(2))+u" error: formato invalido "+str(p[2])+u"("+str(p[4])+u")" u"no es valido dentro de cout, utiliza << antes de cada llamada de una función o parametro."
        error_parser.append(error)
        var = " "
    except:
        try:
            list_aux = [ ]
            a = p[4]
            var = ""
            auxiliar =""
            auxiliar_2 =""
            cont = 0
            for busqueda in str(p[3]).split(","):
                list_aux .append(busqueda)
            longuitud = len(list_aux)-1
            for busqueda in list_aux:
                if len(list_aux) == 1:
                   auxiliar = auxiliar +"int"
                else:
                    if cont < longuitud:
                        auxiliar = auxiliar +"int,"
                    else:
                        auxiliar = auxiliar +"int"
                cont = cont + 1
            buscar = "int "+str(p[1])+str(p[2])+str(auxiliar)+");"
            c = 0
            bandera = False
            while len(funciones) > c:
                if buscar == funciones[c]:
                   bandera = True
                c=c+1
            if bandera == False:
               error =u"Linea: "+str(p.lineno(1))+u" error: la funcion recibe un número distinto de paramatros o la función:"+buscar+u" no está declarada"
               error_parser.append(error)
            for busqueda in  list_aux:
                    auxiliar_2 = auxiliar_2+" ID "+str(busqueda)+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" "
            var = auxiliar_2
        except:
            pass
    p[0] = Node("ID",var)

def p_callcout_2(p):
    '''callcout : callcout ID PARENTESISIZQUIERDO PARENTESISDERECHO
    | ID PARENTESISIZQUIERDO PARENTESISDERECHO
    '''
    try:
        exit = p[4]
        buscar = "int "+str(p[2])+str(p[3])+str(p[4])+";"
        if buscar in funciones:
            pass
        else:
            error =u"Linea: "+str(p.lineno(2))+u" error: la funcion recibe un número distinto de paramatros o la función:"+buscar+u" no está declarada"
            error_parser.append(error)
    except:
         exit = p[3]
         buscar = "int "+str(p[1])+str(p[2])+str(p[3])+";"
         if buscar in funciones:
            pass
         else:
            error =u"Linea: "+str(p.lineno(1))+u" error: la función recibe un número distinto de paramatros o la función:"+buscar+u" no está declarada"
            error_parser.append(error)
#---------------------------------------------------------------------end mod opva------------------------------------------------------------------------------
def p_encabezado_2(p):
    'encabezado : lib'
    p[0] =Node("encabezado",p[1])

def p_lib(p):
    '''lib : NUMERAL INCLUDE MENORQUE ID MAYORQUE
     | NUMERAL INCLUDE MENORQUE ID MATH MAYORQUE
     | NAMESPACE_MOD PUNTOYCOMA
    '''
    try:
         a= p[6]
         if p[4] == "math":
             var = "math.h"
             includes_dec.append(var)
         else:
            includes_dec.append(var)
         count_includes_math = includes_dec.count("math.h")
         if count_includes_math == 1 :
            pass
         elif count_includes_math > 1:
             error = u"Linea: "+str(p.lineno(1))+ u" advertencia: math.h está siendo usado en más de una ocación."
             error_parser.append(error)
    except:
        try:
            a = p[5]
            includes_dec.append(p[4])
            count_includes = includes_dec.count("iostream")
            if count_includes == 1 :
                 pass
            elif count_includes > 1:
                 error = u"Linea: "+str(p.lineno(1))+ u" advertencia: iostream está siendo usado en más de una ocación."
                 error_parser.append(error)
            elif count_includes < 1 :
                error = u"Linea: "+str(p.lineno(1))+ u" advertencia: para utilizar 'using namespace std' incluya la libreria iostream, antes de invocar using namespace std; "
                error_parser.append(error)
        except:
                var = str(p[1])
                using_std_dec.append(var)

    p[0] = Node("encabezado",p[1])

#--------------------------------------------------------------------------------------
def p_contenidos(p):
    ''' contenidos : contenidos cout
    | contenidos cin
    | contenidos seleccion
    | contenidos iteracion
    | contenidos repeticion
    | contenidos operaciones
    | contenidos inc
    | contenidos dec
    | inc contenidos
    | dec contenidos
    | inc
    | dec
    | cout
    | cin
    | seleccion
    | iteracion
    | repeticion
    | operaciones
    | return
    | contenidos return
    | contenidos powgen
    | contenidos pow
    | powgen
    | pow
    '''
    if p[1].type == "todo":
        if p[1] is None:
           sub = str(p[2])
        else:
           sub = str(p[1].sub)+str(p[2])
    else:
        sub = str(p[1])
    p[0] = Node("todo",  sub)

def p_declaracion(p):
    '''declaracion : tipo ID IGUAL NUMBER PUNTOYCOMA
    '''
    if p[1] == "int":
        todo =  str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p.lineno(2))+" "+str(p.lexpos(2))
        p[0] = Node("parametros", todo, p[1])
    elif p[1] == "string":
           error = u'Linea: '+str(p.lineno(2))+u' error de formato, el formato válido es:  %s  %s = "contenido";'  % (p[1],p[2])
           error_parser.append(error)
           p[0] =Node("parametros", " ")

    else :
       error = u"Linea: "+str(p.lineno(2))+u" tipo no implemetado: ' %s ' en USOCODE o no existe en c++." % p[1]
       error_parser.append(error)
       p[0] = Node("parametros", " ")

def p_declaracion_1(p):
    '''declaracion : tipo ID PUNTOYCOMA
    '''
    if p[1] == "int":
       todo =  str(p[2])+" "+"= 0 "+str(p.lineno(2))+" "+str(p.lexpos(2))
       p[0] = Node("parametros", todo, p[1])
    elif p[1] == "string":
        todo =  str(p[2])+" "+"= 0 "+str(p.lineno(2))+" "+str(p.lexpos(2))
        p[0] = Node("parametros", todo,p[1])

    else:
        error = u"Linea: "+str(p.lineno(2))+u" tipo no implemetado: ' %s ' en USOCODE o no existe en c++." % p[1]
        error_parser.append(error)
        p[0] = Node("parametros", ' ')


def p_declaracion_2(p):
    '''declaracion : tipo ID IGUAL ID PUNTOYCOMA
    '''
    error = u'Linea: '+str(p.lineno(2))+u' el formato Tipo id = id; no está disponible en la implementación de USOCODE.'
    error_parser.append(error)
    p[0] =Node("parametros", " ")

def p_declaracion_3(p):
    '''declaracion : tipo ID IGUAL STRING PUNTOYCOMA
    '''
    var = str(p[2])+u" = "+str(0)+" "+str(p.lineno(2))+" "+str(p.lexpos(2))+" "
    p[0] = Node("parametros", var,p[1])





#--------------------------Declaraciones globales-------------------------------#
def p_declaracion_f(p):
    '''declaracionfun :  tipo ID IGUAL NUMBER PUNTOYCOMA
    '''
    if p[1] == "int":
        todo =  str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p.lineno(2))+" "+str(p.lexpos(2))
        p[0] = Node("parametros", todo,p[1])
    elif p[1] == "string":
        error = u"Linea:"+str(p.lineno(2))+u" el tipo 'string' no esda disponible para las declaraciones globales en la implementación de USOCODE, error en el formato para string."
        error_parser.append(error)
        p[0] = Node("parametros", " ", " ")
    else:
        error = u"Linea:"+str(p.lineno(2))+u" Tipo no implemetado: ' %s ' en USOCODE o no existe en c++." % p[1]
        error_parser.append(error)
        p[0] = Node("parametros", " ")


def p_declaracion_f_1(p):
    '''declaracionfun : tipo ID PUNTOYCOMA
    '''
    if p[1] == "int":
       todo =  str(p[2])+" "+"= 0"+" "+str(p.lineno(2))+" "+str(p.lexpos(2))
       p[0] = Node("parametros", todo,p[1])
    elif p[1] == "string":
        error = u"Linea:"+str(p.lineno(2))+u" el tipo 'string' no esda disponible para las declaraciones globales en la implementación de USOCODE."
        error_parser.append(error)
        p[0] = Node("parametros"," "," ")
    else:
        error = u"Linea:"+str(p.lineno(2))+u" Tipo no implemetado: ' %s ' en USOCODE o no existe en c++." % p[1]
        error_parser.append(error)
        p[0] = Node("parametros", " ")


def p_declaracion_f_2(p):
    '''declaracionfun : tipo ID IGUAL ID PUNTOYCOMA
    '''
    error = u'Linea: '+str(p.lineno(2))+u' el formato Tipo id = id; no está disponible en la implementación de USOCODE.'
    error_parser.append(error)
    p[0] =Node("parametros", " ")

# -----------------Validacion para id = id  y id en ambas pocisiones es igual----#
   # if p[1] == "int":
    #    if p[2] == p[4]:
     #      p[4] = "0"
      #  todo = str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p.lineno(4))+" "+str(p.lexpos(4))+" "+" ID "+str(p[4])+" "+str(p.lineno(4))+" "+str(p.lexpos(4))+" "
       # p[0] = Node("parametros",todo, p[1] )
   # else:
    #    error = u"Linea:"+str(p.lineno(2))+u" Tipo no implemetado: ' %s ' en USOCODE o no existe en c++." % p[1]
     #   error_parser.append(error)
      #  p[0] = Node("parametros", " ")

       # ['main', 'int', 'i', '0', 'Linea', '3']
       # todo = "global"+str(p[1])+" "+str(p[4])+" Linea "+str(p.lexer.lineno-1)
        #p[0] = Node("parametros",todo, p[1] )
def p_declaracion_f_4_1(p):
    '''declaracionfun : tipo ID IGUAL STRING PUNTOYCOMA
    '''
    error = u'Linea: '+str(p.lineno(2))+u" error de formato, el tipo string no está implementado en el hambito global."
    error_parser.append(error)
    p[0] =Node("parametros", " ")





#********************************************************************************#
# -------------------------Declaracion de las fucciones--------------------------#
def p_declaracion_f_3(p):
    '''declaracionfun : tipo ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    | tipo ID PARENTESISIZQUIERDO paramdeclaraciones PARENTESISDERECHO PUNTOYCOMA
    '''
#-------------------validacion de tipos en funciones-----------------------------#
    try:
        exit = p[6]
        if p[1] != "int":
           if  p[1] == "char":
               error = u"Linea: "+str(p.lineno(2))+u" Error: '"+str(p[1])+ u"' no es un tipo valido para declarar funciones.!!"
               error_parser.append(error)
           if  p[1] == "void":
               error = u"Linea: "+str(p.lineno(2))+u" Error: '"+str(p[1])+ u"' !!no soportado en la implementación de USOCODE!!"
               error_parser.append(error)
        else:
            todo = str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])
            global cont2
            cont2 = str(p[4])
            for m in re.finditer(id, cont2):
                var = '%s' % (m.group(0))
                if var == "int":
                   cont2 = cont2.replace(var, var)
                else:
                    error = u"Linea:"+str(p.lineno(2))+u" no se admite el tipo: "+str(var)+u" como parametro en la implementación de USOCODE, utilice int"
                    error_parser.append(error)
            todos = str(p[1])+" "+str(p[2])+str(p[3])+str(cont2)+str(p[5])+str(p[6])

#-----------------------------------validacion de id de funciones repetidos---------------------------------------------
            if lista_de_id_funciones.count(p[2]) == 0:
               lista_de_id_funciones.append(p[2])
            else:
                error = u"Linea: "+str(p.lineno(2))+u" error: la función "+str(p[2])+u" está declarada en más de una ocación."
                error_parser.append(error)
            funciones.append(todos)
            p[0] = Node("parametros",todo, p[2] )
    except:
        try:
            exit = p[5]
            if p[1] != "int":
               if  p[1] == "char":
                   error = "Linea: "+str(p.lexpos(2))+" Error: '"+str(p[1])+ "' no es un tipo valido para declarar funciones.!!"
                   error_parser.append(error)
               if  p[1] == "void":
                   error = "Linea: "+str(p.lexpos(2))+" Error: '"+str(p[1])+ "' !!no soportado en la implementacion de USOCODE!!"
                   error_parser.append(error)
            else:
                todo = str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])
                todo2 = str(p[1])+" "+str(p[2])+str(p[3])+str(p[4])+str(p[5])
                p[0] = Node("parametros",todo, p[2] )
                funciones.append(todo2)
        except:
            pass
#*********************************************************************************#
def p_declaracion_error(p):
    '''declaracionfun : tipo ID PARENTESISIZQUIERDO paramdec PARENTESISDERECHO PUNTOYCOMA '''
    error =  "Linea:"+str(p.lineno(2))+" Error: El formato utilizado no es valido en la implemantacion de USOCODE, <br> formato valido: int funcion(int, int); o int funcion(tipo, tipo);"
    error_parser.append(error)
#-------------------validacion de tipos en funciones-----------------------------#


def p_tipo(p):
    '''tipo : INT
            | CHAR
            | STRINGJC
            | VOID
    '''
    p[0] = p[1]
#-------------------------------inicia la modificacion del cout-----------------------------------------------------------------
def p_cout(p):
    '''cout : COUT DOBLEMENORQUE repcout PUNTOYCOMA
    '''
    if  includes_dec.count("iostream") == 1:
        if using_std_dec.count("using namespace std") == 1:
           p[0] = Node("cout", p[3])
        elif using_std_dec.count("using namespace std") == 0:

             error = u"Linea: "+str(p.lineno(1))+u" error: para usar los objetos: cin y cout de forma directa es necesatio incluir using namespace std; formato : sección de includ(librerias)" +u" using namespace std; int variables_globales = 0; Funciones_declaración(); int main(){ }"
             error_parser.append(error)
             p[0] = Node("cout", " ")
        elif using_std_dec.count("using namespace std") > 1:

            error = u"Linea: "+str(p.lineno(1))+u" error:  using namespace std; invocado en multiples ocaciones."
            error_parser.append(error)
            p[0] = Node("cout", " ")
    else:

       error = u"Linea: "+str(p.lineno(1))+u" error: para usar: cin y cout es necesario incluir la libreria iostream, formato : sección de includ(librerias)" +u" using namespace std; int variables_globales = 0; Funciones_declaración(); int main(){ }"
       error_parser.append(error)
       p[0] = Node("cout", " ")


def p_repcout(p):
    '''repcout : repcout cout1 '''
    variable = str(p[1])+" "+str(p[2])
    p[0] = Node("cout",variable)

def p_repcout_1(p):
    '''repcout : cout1 '''
    p[0] = Node("cout",p[1])

def p_cout1(p):
    '''cout1 : DOBLEMENORQUE general '''
    p[0] = Node("cout", p[2])

def p_cout2(p):
    '''cout1 :  general repcout '''
    var = str(p[1])+" "+str(p[2])
    p[0] = Node("cout", var)

def p_cout3(p):
    '''cout1 : general '''
    p[0] = Node("cout", p[1])

def p_general_1(p):
    '''general : STRING '''
    p[0] = Node("cout"," ")

def p_general_2(p):
    '''general : ID '''
    var = " ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" "
    p[0] = Node("cout", var)

def p_general_3(p):
    '''general : NUMBER '''
    p[0] = Node("cout"," ")

def p_general_4(p):
    '''general :  DOBLEMENORQUE STRING
    '''
    p[0] = Node("cout"," ")
def p_general_5(p):
    '''general : DOBLEMENORQUE ID
    '''
    var = " ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))+" "
    p[0] = Node("cout", var)
def p_general_6(p):
    '''general : DOBLEMENORQUE NUMBER
    '''
    p[0] = Node("cout"," ")
def p_general_7(p):
    '''general : NUMBER DOBLEMENORQUE '''

    p[0] = Node("cout"," ")

def p_general_8(p):
    '''general : STRING DOBLEMENORQUE general '''
    p[0] = Node("cout",p[3])

def p_general_9(p):
    '''general : ID DOBLEMENORQUE general '''
    var = " ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" "+str(p[3])+" "
#    var = str(p[1])+" "+str(p[3])
    p[0] = Node("cout",var)

def p_general_10(p):
    '''general : STRING DOBLEMENORQUE STRING '''
    p[0] = Node("cout"," ")

def p_general_11(p):
    '''general : ID DOBLEMENORQUE ID '''
    var = " ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" "+" ID "+str(p[3])+" "+str(p.lexpos(3))+" "+str(p.lineno(3))+" "
#    var = str(p[1])+" "+str(p[3])
    p[0] = Node("cout",var)

def p_general_12(p):
    '''general : NUMBER DOBLEMENORQUE NUMBER '''
    p[0] = Node("cout"," ")

def p_general_13(p):
    '''general : ENDL '''
    p[0] = Node("cout"," ")

#----------------------------------------------------------- mod opva--------------------------------------------------------------------------------------

def p_general_14(p):
    '''general : callcout '''

    p[0] = Node("cout", p[1])

def p_general_15(p):
    '''general : callcout DOBLEMENORQUE general'''
    var = " "+str(p[1])+" "+str(p[3])+" "
    p[0] = Node("cout", var)

def p_general_16(p):
    '''general : callcout DOBLEMENORQUE callcout'''
    var = " "+str(p[1])+" "+str(p[3])+" "
    p[0] = Node("cout",var)

def p_general_17(p):
    '''general : DOBLEMENORQUE callcout'''
    p[0] = Node("cout",p[2])

def p_general_18(p):
    '''general : DOBLEMENORQUE ENDL
    '''
    p[0] = Node("cout"," ")

def p_general_19(p):
    '''general : general DOBLEMENORQUE callcout
    '''
    var = " "+str(p[1])+" "+str(p[3])+" "
    p[0] = Node("cout", var)


def p_general_20(p):
    '''general : ENDL DOBLEMENORQUE general '''
    p[0] = Node("cout", p[3])

def p_general_21(p):
    '''general : ENDL DOBLEMENORQUE ENDL '''
    p[0] = Node("cout"," ")

#-----------------------------------------------------------end mod opva---------------------------------------------------------------

#-------------------------------Termina la modificacion del cout-----------------------------------------------------------------
#-------------------------------inicia la modificacion del cin-----------------------------------------------------------------
def p_cin (p):
    ''' cin : CIN DOBLEMAYORQUE repcin PUNTOYCOMA
    '''
    if  includes_dec.count("iostream") == 1:
        if using_std_dec.count("using namespace std") == 1:

           p[0] = Node("cin", p[3])
        elif using_std_dec.count("using namespace std") == 0:

             error = u"Linea: "+str(p.lineno(1))+u" error: para usar los objetos: cin y cout de forma directa es necesatio incluir using namespace std; formato : sección de includ(librerias)" +u" using namespace std; int variables_globales = 0; Funciones_declaración(); int main(){ }"
             error_parser.append(error)
             p[0] = Node("cin", " ")
        elif using_std_dec.count("using namespace std") > 1:

            error = u"Linea: "+str(p.lineno(1))+u" error:  using namespace std; invocado en multiples ocaciones."
            error_parser.append(error)
            p[0] = Node("cin", " ")
    else:

       error = u"Linea: "+str(p.lineno(1))+u" error: para usar: cin y cout es necesario incluir la libreria iostream, formato : sección de includ(librerias)" +u" using namespace std; int variables_globales = 0; Funciones_declaración(); int main(){ }"
       error_parser.append(error)
       p[0] = Node("cin", " ")



def p_repcin(p):
    '''repcin : repcin cin1
    | cin1
    '''
    if len(p) == 3:
        p[0] = str(p[2])
    elif len(p) == 2:
        p[0] = str(p[1])

def p_cin_1(p):
    '''cin1 :  generalcin repcin '''
    var = " "+str(p[1])+" "+str(p[2])+" "
    p[0] = Node("cin", var)
def p_cin_2(p):
    '''cin1 : DOBLEMAYORQUE generalcin '''
    p[0] = Node("cin", p[2])
def p_cin_3(p):
    '''cin1 : generalcin '''
    p[0] = Node("cin", p[1])


def p_generalcin_1(p):
    '''generalcin : ID '''
    var = " ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))
    p[0] = Node("cin",var)
def p_generalcin_2(p):
    '''generalcin : ID DOBLEMAYORQUE generalcin '''
    var = " ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" "+str(p[3])
    p[0] = Node("cin",var)
def p_generalcin_3(p):
    '''generalcin : ID DOBLEMAYORQUE ID '''
    var = " ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" "+" ID "+str(p[3])+" "+str(p.lexpos(3))+" "+str(p.lineno(3))

    p[0] = Node("cin",var)
def p_generalcin_4(p):
    '''generalcin : DOBLEMAYORQUE ID '''
    var = " ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))
    p[0] = Node("cin", var)
def p_generalcin_5(p):
    '''generalcin : generalcin '''
    p[0] = Node("cin",p[1])
#-------------------------------Termina la modificacion del cin-----------------------------------------------------------------
def p_inc (p):
    ''' inc : ID PLUS PUNTOYCOMA
    '''
    retorno = " RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT "
    p[0] = Node("inc", retorno)

def p_inc_1 (p):
    ''' inc : PLUS ID PUNTOYCOMA
    '''
    retorno = " RT# ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))+" #LT  "
    p[0] = Node("inc" ,retorno)

def p_dec (p):
    ''' dec : ID MENOSMENOS PUNTOYCOMA
    '''
    retorno = " RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  "
    p[0] = Node("dec", retorno)

def p_dec (p):
    ''' dec : MENOSMENOS ID PUNTOYCOMA
    '''
    retorno = " RT# ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))+" #LT "
    p[0] = Node("inc" ,retorno)

   # no permite declaraciones, DOBLE IGUAL AGREGADO.

def p_ciclos_1_2(p):
    '''ciclos : ID IGUAL NUMBER
    | ID DOBLEIGUAL NUMBER
    | ID MENORQUE NUMBER
    | ID MAYORQUE NUMBER
    | ID MENOROIGUAL NUMBER
    | ID MAYOROIGUAL NUMBER
    | ID DISTINTODE NUMBER
    '''
    todo = " RT# ID"+" "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT "
    p[0] = Node("ciclos", todo)

def p_ciclos_1_3(p):
     '''ciclos : ID IGUAL ID
     | ID DOBLEIGUAL ID  '''
     todo = " init#   ID"+" "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+"  "+" ID "+str(p[3])+" "+str(p.lexpos(3))+" "+str(p.lineno(3))+" #endl  "
     p[0] = Node("ciclos", todo)
def p_ciclos_1_4(p):
     '''ciclos : ID MENORQUE ID
     | ID MAYORQUE ID
     | ID MENOROIGUAL ID
     | ID MAYOROIGUAL ID
     | ID DISTINTODE ID
     '''
     todo = " init# RT# ID"+" "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+"  #LT "+" RT# ID "+str(p[3])+" "+str(p.lexpos(3))+" "+str(p.lineno(3))+" #LT   #endl  "
     p[0] = Node("ciclos", todo)



def p_ciclos_1(p):
    '''ciclos : ID PLUS
    | ID MENOSMENOS
    | ID DOBLEIGUAL
    | ID DISTINTODE
    | ID
    '''
    if len(p) == 2:
        todo = "  RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  "
    elif len(p) == 3:
        todo = " RT#  ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT "
    p[0] = Node("ciclos", todo)


def p_seleccion(p):
    '''seleccion : IF PARENTESISIZQUIERDO ciclos PARENTESISDERECHO LLAVEIZQUIERDA contenidos LLAVEDERECHA
    | IF PARENTESISIZQUIERDO ciclos PARENTESISDERECHO  LLAVEIZQUIERDA contenidos LLAVEDERECHA ELSE  LLAVEIZQUIERDA contenidos LLAVEDERECHA
    '''
    try:
        a = p[11]
        contenido = str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "+str(p[7])+" "+str(p[8])+" "+str(p[9])+" "+str(p[10])+" "+str(p[11])
    except:
        try:
            a = p[7]
            contenido = str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+str(p[5])+str(p[6])+str(p[7])
        except:
            pass
    p[0] = Node("if", contenido, contenido)

def p_seleccion_error(p):
    '''seleccion : IF PARENTESISIZQUIERDO ciclos PARENTESISDERECHO LLAVEIZQUIERDA LLAVEDERECHA '''
    contenido = str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "
    p[0] = Node("if", contenido, " ")

def p_iteracion(p):
    '''iteracion : WHILE PARENTESISIZQUIERDO ciclos PARENTESISDERECHO  LLAVEIZQUIERDA  contenidos LLAVEDERECHA
    '''
    contenido = str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+str(p[5])
    todo = str(p[6])+" "+str(p[7])
    p[0] = Node("while", todo, contenido)


def p_iteracion_ERROR(p):
    '''iteracion : WHILE PARENTESISIZQUIERDO ciclos PARENTESISDERECHO  LLAVEIZQUIERDA  LLAVEDERECHA
    '''
    contenido = str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+str(p[5])
    p[0] = Node("while",contenido , " ")

def p_repeticion(p):
    '''repeticion : FOR PARENTESISIZQUIERDO ciclos PUNTOYCOMA  ciclos PUNTOYCOMA ciclos PARENTESISDERECHO LLAVEIZQUIERDA contenidos LLAVEDERECHA
    '''
    lista = []

    try:

        contenido = " "+str(p[1])+""+str(p[2])+" "+str(p[3])+" "+str(p[4])+str(p[5])+str(p[6])+str(p[7])+str(p[8])+str(p[10])

        todo = str(p[6])+" "+str(p[7])

        p[0] = Node("for", contenido, contenido)

    except:
        pass
#--------------------Mod-------------------------------
def p_repeticion_error(p):
    '''repeticion : FOR PARENTESISIZQUIERDO ciclos PUNTOYCOMA  ciclos PUNTOYCOMA ciclos PARENTESISDERECHO LLAVEIZQUIERDA  LLAVEDERECHA
    '''
    contenido = " "+str(p[1])+""+str(p[2])+" "+str(p[3])+" "+str(p[4])+str(p[5])+str(p[6])+str(p[7])+str(p[8])+str(p[10])
    p[0] = Node("for", contenido, " ")


def p_operadores(p):
    '''
    operadores : MAS ID
    | MENOS ID
    | ASTERISCO ID
    | DIVISION ID
    | PORCENTAJE ID
    | PORCENTAJE NUMBER
    | MAS NUMBER
    | MENOS NUMBER
    | ASTERISCO NUMBER
    | DIVISION NUMBER
    | MAS callcout
    | MENOS callcout
    | ASTERISCO callcout
    | DIVISION callcout
    | PORCENTAJE callcout
    '''
    if str(p[2]).isdigit() == True:
        var =  "  RT# ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))+"  #LT "
    else:
        var = " RT#  ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))+"  #LT "
    p[0] = Node("ID", var)

def p_ope_list(p):
    'ope_list : ope_list operadores'
    if str(p[1]) == "[]":
        var = str(p[2])
    else:
        var =  str(p[1])+" "+str(p[2])
    p[0] = Node("ID", var)

def p_ope_list_1(p):
    'ope_list : empty'
    p[0] = Node("ID"," ")

def p_operaciones(p):
    ''' operaciones : ID IGUAL ID ope_list PUNTOYCOMA
    | ID IGUAL NUMBER ope_list PUNTOYCOMA
    | ID IGUAL ID PUNTOYCOMA
    | ID IGUAL NUMBER PUNTOYCOMA
    | ID IGUAL ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    | ID IGUAL ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO ope_list PUNTOYCOMA
    '''
    try:
        list_aux = [ ]
        a = p[8]
        var = ""
        auxiliar =""
        auxiliar_2 =""
        longuitud = len(list_aux) + 1
        cont = 0
        for busqueda in str(p[5]).split(","):
            list_aux .append(busqueda)
        for busqueda in list_aux:
            if len(list_aux) == 1:
               auxiliar = auxiliar +"int"
            else:
                if cont < longuitud:
                    auxiliar = auxiliar +"int,"
                else:
                    auxiliar = auxiliar +"int"
            cont = cont + 1
        buscar = "int "+str(p[3])+str(p[4])+str(auxiliar)+str(p[6])+str(p[7])+";"
        c = 0
        bandera = False
        while len(funciones) > c:
            if buscar == funciones[c]:
               bandera = True
            c=c+1
        if bandera == False:
           error =u"Linea: "+str(p.lineno(3))+u" error: la funcion recibe un número distinto de paramatros o la función:"+buscar+u" no está declarada"

        id1 =" RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  "
        for busqueda in  list_aux:
                auxiliar_2 = auxiliar_2+" RT# ID "+str(busqueda)+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  "
        var = id1+auxiliar_2
    except:
        try:
            a = p[6]
            var = ""
            exit = p[6]
            buscar = "int "+str(p[3])+str(p[4])+str(p[5])+str(p[6])

            if buscar in funciones:
                pass
            else:
                error =u"Linea: "+str(p.lineno(3))+u" error: la funcion recibe un número distinto de paramatros o la función:"+buscar+u" no está declarada"
                error_parser.append(error)
            contenido = " RT# ID " +str(p[1])+ " "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT "
            var = contenido
        except:
            try:
                 a = p[5]
                 if str(p[3]).isdigit() == True:
                    var = " init# RT#  ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT "+str(p[4])+" #endl "
                 else:
                     var = " init#  RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT "+" RT# ID "+str(p[3])+" "+str(p.lexpos(3))+" "+str(p.lineno(3))+" #LT "+str(p[4])+" #endl "
            except:
                try:
                    if str(p[3]).isdigit() == True:
                        var = " init# RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  #endl "
                    else:
                        var = " init# RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  RT#   "+"ID "+str(p[3])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT   #endl "
                except:
                    var = " "
    p[0] = Node("ID", var)

#-----------------------------------------------------------------------------------------------

def p_return(p):
    '''return : RETURN NUMBER PUNTOYCOMA'''
    p[0] = Node("return"," ")


def p_return_1(p):
    '''return : RETURN ID PUNTOYCOMA'''
    retorno = " RT#  ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))+" #LT   "
    p[0] = Node("return",retorno)

#-----------------------------------------mod opva-----------------------------------------------
def p_idnumpow(p):
    '''idnumpow : idnumpow ID
    | idnumpow NUMBER
    | ID
    | NUMBER
    '''
    try:
        a = p[2]
        if str(p[2]).isdigit():
            retorno = ""
        else:
            retorno = " RT#  ID "+str(p[2])+" "+str(p.lexpos(2))+" "+str(p.lineno(2))+" #LT "
    except:
        a = p[1]
        if str(p[1]).isdigit():
           retorno = ""
        else:
            retorno = " RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  "
        p[0] = Node("pow", retorno,"")

def p_pow(p):
    '''pow : POW PARENTESISIZQUIERDO idnumpow COMA idnumpow PARENTESISDERECHO
    | SIN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    | COS PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    | TAN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    | SQRT PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    '''
    if  includes_dec.count("math.h") == 1:
        pass
    else:
       error = u"Linea: "+str(p.lineno(1))+u" error: para usar: SIN, COS, TAN, SQRT Y POW es necesario incluir la libreria math.h, formato : sección de includ(librerias)" +u" using namespace std; int variables_globales = 0; Funciones_declaración(); int main(){ }"
       error_parser.append(error)
    try:
        a = p[7]
        retorno =" "+str(p[3])+" "+str(p[5])+" "
    except:
        a = p[4]
        retorno = " "+str(p[3])+" "
    p[0] = Node("pow", retorno)

def p_powgen(p):
    '''powgen : POW PARENTESISIZQUIERDO idnumpow COMA idnumpow PARENTESISDERECHO PUNTOYCOMA
    | SIN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | COS PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | TAN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | SQRT PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | ID IGUAL pow ope_list PUNTOYCOMA
    | ID IGUAL powgen

    '''
    if  includes_dec.count("math.h") == 1:
        pass
    else:
       error = u"Linea: "+str(p.lineno(1))+u" error: para usar: SIN, COS, TAN, SQRT Y POW es necesario incluir la libreria math.h, formato : sección de includ(librerias)" +u" using namespace std; int variables_globales = 0; Funciones_declaración(); int main(){ }"
       error_parser.append(error)
    try:
        a = p[7]
        retorno =" "+str(p[3])+" "+str(p[5])+" "
    except:
        try:
            a = p[5]
            if str(p[1]) != "sin" and str(p[1]) != "cos" and str(p[1]) != "tan" and str(p[1]) != "sqrt":
                retorno = " RT# ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  "+str(p[3])+"   "
            else:
                retorno = " "+str(p[3])+" "
        except:
            a = p[3]
            retorno = " RT#  ID "+str(p[1])+" "+str(p.lexpos(1))+" "+str(p.lineno(1))+" #LT  "+str(p[3])+" "
    p[0] = Node("pow", retorno)
#-----------------------------------------end mod opva----------------------------------------

def p_empty(p):
    'empty :'
    pass
def p_error(p):
    if p is None:
        error = u"Excepción: opciones: 1) No encontro el token ' } ' al final del código, 2) no existe código para procesar."
        error_parser.append(error)
    else:
        error = u"Linea %d:  error, se esperaba una instrucción diferente en la linea del : token: ' %s '   ." % (p.lineno, p.value)
        error_parser.append(error)

def parse(data, debug = False):
    lexer = Lexer()
    lexer.build()
#    yacc.yacc()
    yacc.yacc(optimize=1,debug=False, write_tables=False)
    return yacc.parse(data, lexer=lexer.lexer)

def main(data):
    while len(lista_de_id_funciones) > 0:lista_de_id_funciones.pop()
    while len(Tabla_verificacion_tipos_return) > 0:Tabla_verificacion_tipos_return.pop()
    while len(Tabla_verificacion_tipos) > 0:Tabla_verificacion_tipos.pop()
    while len(using_std_dec) > 0:using_std_dec.pop()
    while len(includes_dec) > 0:includes_dec.pop()
    while len(includes_verificacion) > 0:includes_verificacion.pop()
    while len(funciones) > 0:funciones.pop()
    while len(funciones_programadas) > 0:funciones_programadas.pop()
    while len(Tablas_global) > 0:Tablas_global.pop()
    while len(Tablas_simbolos) > 1:Tablas_simbolos.pop()
    while len(error_parser) > 0:error_parser.pop()
    #---------------------------validacion de funcion int main--------------------#
    funciones.append("int main();")
    #******************************************************************************#
    respuesta = { }
    parse(data)
    if error_parser == [ ]:
        respuesta['estado'] = 'error'
        respuesta['codigo'] = 'Analisis 1, Lexer OK.'
    else:
        try:
            respuesta['codigo'] = error_parser[0]
            respuesta['estado'] = 'error'
        except:
            respuesta['codigo'] = error_parser
            respuesta['estado'] = 'error'
    return respuesta


