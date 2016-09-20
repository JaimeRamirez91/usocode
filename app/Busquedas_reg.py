#.*-coding:utf-8-*-
#-----------------------------------------------------------------------------
#Permite construuir la tabla de simbolos, aqui se realizan los filtros usando
#expreciones regulares
#-----------------------------------------------------------------------------
import re
#----------------------------- Tablas-----------------------------------------
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
string = r'"[( *?)]+[w+_\d\ \w\:\.\,\;]*"|"[w+_\d\ \w\:\.\,\;]*"'
str_aux = r'string'
#*****************************************************************************#
#------------------------Concatenacion de expreciones-------------------------#
#t_buscar_id = str(ID)+str(espacio)+str(id)+str(espacio)+str(digito)
t_buscar_str_id = str(str_aux)+str(espacio)+str(id)+str(espacio)+str(igual_int)+str(espacio)+str(id)+str(espacio)+str(digito)+str(espacio)+str(digito)
#t_buscar_str = str(str_aux)+str(espacio)+str(id)+str(espacio)+str(igual_int)+str(espacio)+str(digito)+str(espacio)+str(digito)+str(espacio)+str(digito)
#t_buscar_str = str(str_aux)+str(espacio)+str(id)+str(espacio)+str(igual_int)
t_buscar_id = str(ID)+str(espacio)+str(id)+str(espacio)+str(digito)+str(espacio)+str(digito)
t_var_int = str(int)+str(espacio)+str(id)+str(espacio)+str(igual_int)+str(espacio)+str(digito)+str(espacio)+str(digito)+str(espacio)+str(digito)
t_var_int_id = str(int)+str(espacio)+str(id)+str(espacio)+str(igual_int)+str(espacio)+str(id)+str(espacio)+str(digito)+str(espacio)+str(digito)
#*****************************************************************************#

class Busqueda:
    # funcion para buscar int id = 0 de lasa funciones cuando int pn(int i, int o);
    def buscar_int_fun_dec(self, cadena, funcion):
        Tablas_simbolos = [ ]
        mi_l = [ ]
        while len(mi_l) > 0: mi_l.pop()
        while len(Tablas_simbolos) > 0: Tablas_simbolos.pop()
        contador = 0
        contenido = cadena
        # Recolectando los enteros igualados a numero
        for m in re.finditer(t_var_int , contenido):
            var = '%s' % (m.group(0))
            final = funcion+" "+var
            for m in re.finditer(id , final):
                var = '%s' % (m.group(0))
                mi_l.append(var)
                contador +=1
                if contador == 5:
                   Tablas_simbolos.append(mi_l)
                   contador = 0
                   vacio = [ ]
                   mi_l = vacio
        return Tablas_simbolos

    # funcion para buscar int id = 0; de forma normal
    def buscar_int(self, cadena, funcion):
        Tablas_simbolos = [ ]
        mi_l = [ ]
        while len(mi_l) > 0: mi_l.pop()
        while len(Tablas_simbolos) > 0: Tablas_simbolos.pop()
        contador = 0
        contenido = cadena
        # Recolectando los enteros igualados a numero
        for m in re.finditer(t_var_int , contenido):
            var = '%s' % (m.group(0))
            final = funcion+" "+var
            for m in re.finditer(id , final):
                var = '%s' % (m.group(0))
                mi_l.append(var)
                contador +=1
                if contador >= 6:
                   Tablas_simbolos.append(mi_l)
                   contador = 0
                   vacio = [ ]
                   mi_l = vacio
        return Tablas_simbolos

    # funcion para buscar int id = id;
    def buscar_id(self, cadena, funcion):
        Tablas_simbolos = [ ]
        mi_l = [ ]
        contador = 0
        while len(mi_l) > 0: mi_l.pop()
        while len(Tablas_simbolos) > 0: Tablas_simbolos.pop()
        for m in re.finditer(t_var_int_id, cadena):
            var = '%s' % (m.group(0))
            lista_validacion = [ ]
            while len(lista_validacion) > 0: lista_validacion.pop()
            for x in var.split(" "):
                lista_validacion.append(x)
            if lista_validacion[3].isdigit():
                pass
            else:
                final = funcion+" "+var
                for m in re.finditer(id , final):
                    var = '%s' % (m.group(0))
                    mi_l.append(var)
                    contador +=1
                    if contador >= 6 :
                       Tablas_simbolos.append(mi_l)
                       contador = 0
                       vacio = [ ]
                       mi_l = vacio
        return Tablas_simbolos

    # funcion para buscar  id;
 #----------------------------------------------modificado-----------------------------hoy
    def buscar_ID(self, cadena, funcion):
        Tablas_simbolos = [ ]
        mi_l = [ ]
        lista = [ ]
        contador = 0
        contador2 = 0
        while len(mi_l) > 0: mi_l.pop()
        while len(Tablas_simbolos) > 0: Tablas_simbolos.pop()
        for m in re.finditer(t_buscar_id, cadena):
            var = '%s' % (m.group(0))
            final = funcion+" "+var
            for m in re.finditer(id , final):
                var = '%s' % (m.group(0))
                mi_l.append(var)
                contador +=1
                if contador >= 5 :
                   temporal = [ ]
                   vacio = " "
                   temporal.append(mi_l[0])
                   temporal.append(vacio)
                   temporal.append(vacio)
                   temporal.append(mi_l[2])
                   temporal.append(mi_l[4])
                   temporal.append(mi_l[3])
                   Tablas_simbolos.append(temporal)
                   contador = 0
                   vacio = [ ]
                   mi_l = vacio
                   temporal = vacio
        return Tablas_simbolos
    def Busqueda_cout_id(self,cadena):
        lista = [ ]
        id = r'\w+(_\d\w\S)*'
        comillas = r'"'
        resul = ""
        variable = ""
        regular = comillas+id+comillas
        cadena = str(cadena)
        if comillas in cadena:
            cadena = ""
        for m in re.finditer(regular, cadena):
            variable = '%s' % (m.group(0))
            cadena = cadena.replace(variable," ")
        for m in re.finditer(id, cadena):
            var = '%s' % (m.group(0))
            lista.append(var)
        for n in lista:
            resul = resul+" "+n
        return resul

    def buscar_str_id(self,cadena,funcion):
         Tablas_simbolos = [ ]
         mi_l = [ ]
         contador = 0
         for x in re.finditer(t_buscar_str_id,cadena):
             var = '%s' %  (x.group(0))
             final = funcion+" "+var
             for m in re.finditer(id , final):
                var = '%s' % (m.group(0))
                mi_l.append(var)
                contador +=1
                if contador >= 6:
                   Tablas_simbolos.append(mi_l)
                   contador = 0
                   vacio = [ ]
                   mi_l = vacio
         return Tablas_simbolos
#----funcion: todas las operaciones bienen aqui para ser insertadas en la matriz de varificacion de tipos----
    def buscar_op(self,cadena,funcion):
         cadena = cadena.replace("["," ")
         cadena = cadena.replace("]"," ")
         initop = r'init#+'
         endop = r'+#endl'
         todo = "["+t_buscar_id
         iterados = r'*]'
         contador = 0
         contador_aux = 0
         lista_1 = [ ]
         Matriz_resultante = [ ]
         lista_1_aux = [ ]
         t_buscar_operaciones = initop+todo+iterados+endop
         Tablas_simbolos = [ ]
         mi_l = [ ]
         for x in re.finditer(t_buscar_operaciones,cadena):
             variables = '%s' %  (x.group(0))
             for x in re.finditer(t_buscar_id, variables):
                var = '%s' %  (x.group(0))
                final = funcion+" "+var
                for lis in re.finditer(id,final):
                    lis = '%s' %  (lis.group(0))
                    lista_1_aux.append(lis)
                    contador +=1
                    if contador == 5:
                       lista_1.append(lista_1_aux)
                       contador = 0
                       vacio = [ ]
                       lista_1_aux = vacio
             Matriz_resultante.append(lista_1)
             lista_1 = [ ]
             contador_aux = contador_aux+1
         return  Matriz_resultante

    def busqueda_return(self,cadena,funcion):
        lista_1 = [ ]
        init = r'RT#+'
        end  = r'+#LT'
        todo = "["+t_buscar_id
        iterados = r'*]'
        contador = 0
        lista_1_aux = [ ]
        t_buscar_operaciones = init+todo+iterados+end
        for x in re.finditer(t_buscar_operaciones,cadena):
             variables = '%s' %  (x.group(0))
             for x in re.finditer(t_buscar_id, variables):
                   var = '%s' %  (x.group(0))
                   final = funcion+" "+var
                   for lis in re.finditer(id,final):
                      lis = '%s' %  (lis.group(0))
                      lista_1_aux.append(lis)
                      contador +=1
                      if contador == 5:
                           lista_1.append(lista_1_aux)
                           contador = 0
                           vacio = [ ]
                           lista_1_aux = vacio
        return lista_1



