__author__ = 'JARV'
class orden(object):
    def metodo(self, Tablas_simbolos):
        try:
            elementos = Tablas_simbolos
            numero = len(elementos[0])
            numero2 = len(elementos)
        except:
            elementos = 0
            numero = 0
            numero2 = 0
        lista = []
        lista2 = []
        for co in range(0,numero2):
            el = int(elementos[co][5])
            lista.append(el)
        ord = len(lista)
        lista2 = lista
        i= 0
        contador = 0
        try:
            while (i < ord):
                 contador =+ 1
                 j = i
                 while (j < ord):
                     #por q se da vuelta
                     if(lista2[i] > lista2[j]):
                        temp = lista2[i]
                        lista2[i] = lista2[j]
                        lista2[j] = temp
                     j=j+1
                 i=i+1
        except:
             pass
        lista_order = [ ]
        try:
            a = len(elementos)
        except:
            a = 0
        i = 0
        contador = 0
        try:
            while (i < a):
                j = i
                while (j < a):
                    for m in elementos:
                        e = str(lista2[contador])
                        if e in m:
                            if contador == a:
                                pass
                            else:
                                contador +=1
                                lista_order.append(m)
                        else:
                            pass
                    j=j+1
                i = i+1
        except:
             pass
      #  for x in lista_order:
        return lista_order

# para que retorne el error podriamos  crear esta funcion aparte y  retornar el error
    def existencia(self , pv, Tablas_simbolos):
            lista_order = orden().metodo(Tablas_simbolos)
            Lt = []
            elementob = pv
            l = 0
            cont = 0
            while (l < 1):
                m = l
                while (m < 1):
                    for x in lista_order:
                        if x != elementob:
                            if cont == 0:
                               Lt.append(x)
                        else:
                            if cont == 0:
                                lista_pb = [ ]
                                for y in x:
                                    lista_pb.append(y)
                            cont = 1
                    m=m+1
                l = l+1
            return  Lt

    def Coincidencia(self , pv, Tablas_simbolos):
                lista_order = orden().metodo(Tablas_simbolos)
                Lt = []
                l = 0
                cont = 0
                while (l < 1):
                    m = l
                    while (m < 1):
                        for x in lista_order:
                            if x != pv:
                                if cont == 0:
                                   pass
                                  # Lt.append(x)
                            else:
                                Lt.append(x)
                                cont = 1
                        m=m+1
                    l = l+1
                return  Lt

    def Val_com(self, Lista):
                Lista_ret = [ ]
                for var in Lista:
                    Lista_ret.append(var)
                return Lista_ret
    #ganera la lista1 para verificar si existe o no el valor
    def generaLista1 (self ,Valore_para_coparacion):
        filas =  len (Valore_para_coparacion)
        colummnas = len (Valore_para_coparacion[0])
        lista = [ ]
        for f in range(0, filas):
            a = str(Valore_para_coparacion[f][0])+" "+str(Valore_para_coparacion[f][2])
            lista.append(a)
        return lista

    #ganera la lista2 para verificar si existe o no el valor
    def generaLista2 (self ,Lista_comparar):
        filas =  len (Lista_comparar)
        colummnas = len (Lista_comparar[0])
        lista = [ ]
        for f in range(0, filas):
            a = str(Lista_comparar[f][0])+" "+str(Lista_comparar[f][2])
            b = str(Lista_comparar[f][5])
            c = str(Lista_comparar[f][4])
            lista.append(a)
            lista.append(b)
            lista.append(c)
        return lista
    #error en tipo id = id (que el id este siendo utilizado pero nunca declarado)
    def error(self, Lista_comparar, Valore_para_coparacion):
                lista = [ ]
                if Valore_para_coparacion == [ ]:
                    pass
                else:
                  val_com =  orden().generaLista1(Valore_para_coparacion)
                  li_com =  orden().generaLista2(Lista_comparar)
                  contador = 0
                  for cont in li_com[0].split(" "):
                      contador=contador+1
                  if li_com[0] in val_com:
                      contador = 0
                      for cont in li_com[0].split(" "):
                            contador=contador+1
                      if contador == 3:
                          pass
                      else:
                          l_aux = []
                          var = str(li_com[0])
                          contador = 0
                          final_error = " "
                          for aux in var.split(" "):
                              if contador == 1:
                                 final_error = aux
                              else:
                                  contador = contador+1
                          a = "Linea: "+str(li_com[2])+" error variable: '"+final_error+"' !!doble declaracion!!."
                          lista.append(a)
                  else:
                      pass
                if lista == [ ]:
                    pass
                else:
                    return lista

#-----------------------------------------------------------------------------------------------
#---------------------- modificado  para buscar por linea---------------------------------------
#-----------------------------------------------------------------------------------------------
    #En esta funcion buscamos todos los id declarados antes del que estamos buscando
    def existencia_id(self , pv, Tablas_simbolos):
            lista_order = orden().metodo(Tablas_simbolos)
            Lt = []
            lt_med = []
            lt_p1 = [ ]
            lt_p2 = [ ]
            lt_p3 = [ ]
            elementob = pv
            l = 0
            cont = 0
            #add para prueba 11:48
            cont2 = 0
            while (l < 1):
                m = l
                while (m < 1):
                    for x in lista_order:
                        if x[3] != elementob:
                            todo = str(x[0])
                            todo1 = str(x[2])
                            todo2= str(x[5])
                            lt_p1.append(todo)
                            lt_p2.append(todo1)
                            lt_p3.append(todo2)
                        else:
                            if cont == 0:
                                lista_pb = [ ]
                                for y in x[3]:
                                    lista_pb.append(y)
                            cont = 1
                    lt_med.append(Lt)
                    m=m+1
                l = l+1
            longitud = len(lt_p1)
            a = 0
            while a < longitud:
                lista_temp = [ ]
                parametro = lt_p1[a]
                parametro1 = lt_p2[a]
                parametro2 = lt_p3[a]
                lista_temp.append(parametro)
                lista_temp.append(parametro1)
                lista_temp.append(parametro2)
                if len(lista_temp) == 3:
                    Lt.append(lista_temp)
                a =  a + 1
            return  Lt

    def error_tipo_id_1(self, valor ,Valores_para_coparacion):
                    lista = [ ]
                    longitud =  len(Valores_para_coparacion)
                    a = 0
                    estado = False
                    while longitud > a:
                        if valor in Valores_para_coparacion[a]:
                            estado = True
                        elif valor[1] == Valores_para_coparacion[a][1] and valor[0] == Valores_para_coparacion[a][0]:
                            n1 =  eval(valor[2])
                            n2 =  eval(Valores_para_coparacion[a][2])
                            if n2 <= n1:
                               estado = True
                            else:
                                pass
                        else:
                            pass
                        a =  a + 1
                    if estado == True:
                        pass
                    else:
                        error = str(valor[0])+" "+str(valor[1])
                        lista.append(error)
                    return lista

    def ordenar_lt_global(self,lista):
        lt = [ ]
        f = len(lista)

        for x in range(0,f):
            lt.append(lista[x][2])
        return lt
    def ordenar_lt(self,lista):
        lt = [ ]
        lt2 = [ ]
        resultado = []
        f = len(lista)
        for x in range(0,f):
            var = str(lista[x][0])
            var2 = str(lista[x][2])
            lt.append(var)
            lt2.append(var2)
        longitud = len(lt)
        a = 0
        while  a < longitud:
            lista_temp = [ ]
            p1 = lt[a]
            p2 = lt2[a]
            lista_temp.append(p1)
            lista_temp.append(p2)
            if len(lista_temp) == 2:
                resultado.append(lista_temp)
            a = a + 1
        return resultado

    def crear_listas(self,lista):
        lt = [ ]
        for x in lista:
            for y in x.split(" "):
                listas = [ ]
                listas.append(y)
                if len(listas) == 2:
                    lt.append(listas)
        return lt

