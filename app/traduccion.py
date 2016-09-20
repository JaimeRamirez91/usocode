import ply.yacc as yacc
from c_lexer import Lexer
from ast import Node
import re
tokens = Lexer.tokens
traduccion = [ ]

def p_programa(p):
    '''programa : encabezado dec_lst funciones
    | encabezado funciones
    | dec_lst funciones
    | encabezado dec_lst funciones dec_lst funciones
    | funciones
    '''
    tra_aux = [ ]
    if len(p) == 2:
       p[0] = '$("#consola").html("");'+str(p[1])
    elif len(p) == 3:
        p[0] = '$("#consola").html("");'+str(p[1])+str(p[2])
    elif len(p) == 4:
        p[0] = '$("#consola").html("");'+str(p[1])+str(p[2])+str(p[3])
    elif len(p) == 6:
        p[0] ='$("#consola").html("");'+str(p[1])+str(p[2])+str(p[3])+str(p[4])+str(p[5])
    p[0] = Node("todo", p[0])
    traduccion.append(p[0])


def p_dec_lst(p):
    '''dec_lst : dec_lst declaracionfun
    |  declaracionfun
    '''

    if p[1].type == "todo":
        if p[1] is None:
           sub = str(p[2])
        else:
          sub = str(p[1].sub)+str(p[2])
    else:
        sub = str(p[1])
    p[0] = Node("todo",  sub)

def p_funciones(p):
    '''funciones : tipo ID PARENTESISIZQUIERDO  PARENTESISDERECHO  LLAVEIZQUIERDA todo  LLAVEDERECHA
       | tipo ID PARENTESISIZQUIERDO paramdec  PARENTESISDERECHO  LLAVEIZQUIERDA todo  LLAVEDERECHA
    '''
    try:
        a = p[7]
        todo = str (p[2])+str(p[3])+str(p[4])+str(p[5])+str(p[6])+str(p[7])
        p[1] = "function"
    except:
        a = p[8]
        todo = str (p[2])+str(p[3])+str(p[4])+str(p[5])+str(p[6])+str(p[7])+str(p[8])
        p[1] = "function"
    p[0] = Node("Funcion",todo, p[1])


def p_funciones_1(p):
    '''funciones : funciones  tipo ID PARENTESISIZQUIERDO  PARENTESISDERECHO LLAVEIZQUIERDA todo LLAVEDERECHA
    '''
    todo = ("function Ejem_" +str (p[3])+str (p[4])+str (p[5])+str (p[6])+str (p[7])+str (p[8]))
    p[0] = Node("Funcion",todo, p[1])


def p_funciones_2(p):
    '''funciones : funciones tipo ID PARENTESISIZQUIERDO paramdec  PARENTESISDERECHO  LLAVEIZQUIERDA todo  LLAVEDERECHA'''
    todo = ("function Ejem_"+str (p[3])+str (p[4])+str (p[5])+str (p[6])+str (p[7])+str (p[8])+str (p[9]))
    p[0] = Node("Funcion",todo, p[1])


#***********************************************************************************************************************

def p_parametros(p):
    """parametros : parametros COMA ID
                  | parametros COMA NUMBER
                  | ID
                  | NUMBER
                  """
    try:
        a = p[3]
        var = p[3]
        if var.isdigit == True:
            sub = str(p[1])+","+(p[3])
        else:
            sub = str(p[1])+", Ejem_"+(p[3])
    except:
        try:
           a = p[1]
           var = p[1]
           if var.isdigit == True:
               sub = str(p[1])
           else:
               sub = "Ejem_"+str(p[1])
        except:
            pass
    p[0] = Node("parametrosfun", sub)
def p_pram_dec(p):
    """paramdec : paramdec COMA tipo ID
                  | paramdec COMA tipo NUMBER
                  | tipo ID
                  | tipo NUMBER """
    try:
        a = p[4]
        var = p[4]
        if var.isdigit == True:
            sub = str(p[1])+","+str(p[4])
        else:
            sub = str(p[1])+", Ejem_"+str(p[4])
    except:
        try:
            a = p[2]
            var = p[2]
            if var.isdigit == True:
                sub = str(p[2])
            else:
                sub = "Ejem_"+str(p[2])
        except:
            pass
    p[0] = Node("parametrosfun", sub)

#-------------------Declaraciones validas de funciones------------------------------
def p_pram_declaracion(p):
    """paramdeclaraciones : paramdeclaraciones COMA tipo
                  | tipo
                  """
    try:
        a= p[3]
        sub = ""
        pass
    except:
        try:
            a= p[1]
            sub = ""
        except:
            pass
    p[0] = Node("parametrosfun", sub)

def p_pram_declaracion_1(p):
    """paramcallfun : paramcallfun COMA ID
                  | paramcallfun COMA NUMBER
                  | ID
                  | NUMBER"""
    try:
        a= p[3]
        if str(p[3]).isdigit() == True:
            sub = str(p[1])+","+str(p[3])
        else:
            sub = str(p[1])+", Ejem_"+str(p[3])
    except:
        try:
            a= p[1]
            if str(p[1]).isdigit() == True:
                sub = str(p[1])
            else:
                sub = "Ejem_"+str(p[1])
        except:
            pass
    p[0] = Node("parametros", sub)
#***********************************************************************************************************************

def p_funciones_ERROR(p):
    '''funciones : tipo ID PARENTESISIZQUIERDO  PARENTESISDERECHO  LLAVEIZQUIERDA   LLAVEDERECHA
    '''
    p[0] = Node("error","")

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
    | return
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
    '''
    if p[1].type == "todo":
        if p[1] is None:
           sub = str(p[2])
        else:
           try: 
          	 sub = str(p[1])+str(p[2])
	   except:
                sub = str(p[1])
    else:
        sub = str(p[1])
    p[0] = Node("todo",sub)

#-----------------------------------------------------------------------------------------
def p_encabezado(p):
    'encabezado : encabezado lib'
    p[0] = " "

def p_encabezado_2(p):
    'encabezado : lib'
    p[0] = " "

def p_lib(p):
    '''lib : NUMERAL INCLUDE MENORQUE ID MAYORQUE
    | NUMERAL INCLUDE MENORQUE ID MATH MAYORQUE
    | NAMESPACE_MOD PUNTOYCOMA
    '''
    p[0] = " "

def p_callfun(p):
    '''callfun : callfun ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    | ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    '''
    if len(p) == 6:
        todo = str(p[1])+"Ejem_"+str(p[2])+str(p[3])+str(p[4])+str(p[5])
    elif len(p) == 5:
        todo = "Ejem_"+str(p[1])+str(p[2])+str(p[3])+str(p[4])
    p[0] = Node("parametros", todo)

def p_call_fun_2(p):
    '''callfun : callfun ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO PUNTOYCOMA
    | ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO PUNTOYCOMA
    '''
    if len(p)== 7:
        todo = str(p[1])+" Ejem_"+str(p[2])+str(p[3])+str(p[4])+str(p[5])+str(p[6])
    elif len(p)==6:
        todo = "Ejem_"+str(p[1])+str(p[2])+str(p[3])+str(p[4])+str(p[5])
    p[0] = Node("parametros", todo)

def p_callcout(p):
    '''callcout : callcout pow
    | pow
    '''
    if len(p)== 3:
        todo = str(p[2])
    elif len(p)==2:
        todo = ""
    p[0] = Node("parametros", todo, p[1])

def p_callcout_1(p):
    '''callcout : callcout ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO
    | ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO
    '''
    if len(p)== 6:
        todo = str(p[2])+str(p[3])+str(p[4])+str(p[5])
    elif len(p)==5:
        todo = str(p[2])+str(p[3])+str(p[4])
    p[0] = Node("parametros", todo, p[1])

def p_callcout_2(p):
    '''callcout : callcout ID PARENTESISIZQUIERDO PARENTESISDERECHO
    | ID PARENTESISIZQUIERDO PARENTESISDERECHO
    '''
    if len(p)== 5:
        todo = str(p[2])+str(p[3])+str(p[4])
    elif len(p)==4:
        todo = str(p[2])+str(p[3])
    p[0] = Node("parametros", todo, p[1])
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
    | cout
    | cin
    | seleccion
    | iteracion
    | repeticion
    | operaciones
    | inc
    | dec
    | return
    | contenidos return
    | contenidos powgen
    | contenidos pow
    | powgen
    | pow
    '''
    if len(p) == 3:
        p[0] = str(p[1])+str(p[2])
        sub = p[0]
    elif len(p) ==2:
        p[0] = p[1]
        sub = p[0]
    p[0] = Node("todo",  sub)


#-----------------------------------------------------------------------------------------------------------------------
# DECLARACIONES GLOBALES
def p_declaracion_f(p):
    '''declaracionfun : tipo ID IGUAL NUMBER PUNTOYCOMA
    '''
    try:
        a = p[5]
        p[1] = "var"
        todo = " Ejem_"+str(p[2])+str(p[3])+str(p[4])+str(p[5])
    except:
        pass
    p[0] = Node("parametros", todo, p[1])

def p_declaracion_f_1(p):
    '''declaracionfun : tipo ID PUNTOYCOMA
    '''
    try:
        a = p[3]
        p[1] = "var"
        todo = " Ejem_"+str(p[2])+"= 0"+str(p[3])
    except:
        pass
    p[0] = Node("parametros", todo, p[1])

def p_declaracion_f_2(p):
    '''declaracionfun : tipo ID IGUAL ID PUNTOYCOMA
    '''
    try:
        a = p[5]
        p[1] = "var"
        todo = " Ejem_"+str(p[2])+str(p[3])+"Ejem_"+str(p[4])+str(p[5])
    except:
        pass
    p[0] = Node("parametros", todo, p[1])

def p_declaracion_f_3(p):
    '''declaracionfun : tipo ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    | tipo ID PARENTESISIZQUIERDO paramdeclaraciones PARENTESISDERECHO PUNTOYCOMA
    '''
    p[1] = ""
    todo = ""
    p[0] = Node("parametros", todo, p[1])

#-----------------------------------------------------------------------------------------------------------------------

def p_declaracion(p):
    '''declaracion : tipo ID IGUAL NUMBER PUNTOYCOMA
    '''
    todo = "Ejem_"+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])
    p[1] = 'var'
    p[0] = Node("parametros", todo, p[1])

def p_declaracion_1(p):
    '''declaracion : tipo ID PUNTOYCOMA
    '''
    if p[1] == "int":
       todo =  "Ejem_"+str(p[2])+" "+"= 0"+" "+str(p[3])
       p[1] = 'var'
       p[0] = Node("parametros", todo, p[1])
    elif p[1] == "char":
       comillas = '"'
       todo =  "Ejem_"+str(p[2])+" "+"= "+comillas+" "+comillas+" "+str(p[3])
       p[1] = 'var'
       p[0] = Node("parametros", todo)
    elif p[1] == "string":
        p[1] = 'var'
        var = "Ejem_"+str(p[2])+" "+"= 0"+" "+str(p[3])
        p[0] = Node("parametros", var, p[1])
    else:
        print "falta aun ven a declaraciones"

def p_declaracion_2(p):
    '''declaracion : tipo ID IGUAL ID PUNTOYCOMA
    '''
    if p[1] == "int":
        todo = "Ejem_"+str(p[2])+" "+str(p[3])+" Ejem_"+str(p[4])+" "+str(p[5])
    elif p[1] == "string":
        if p[2] == p[4]:
            p[4] = "0"
            todo = "Ejem_"+str(p[2])+" "+str(p[3])+" "+str(p[4])+str(p[5])
            p[0] = Node("parametros",todo, p[1] )
        else:
            todo = " Ejem_"+str(p[2])+str(p[3])+" Ejem_"+str(p[4])+str(p[5])
            p[0] = Node("parametros",todo, p[1] )
    p[0] = Node("parametros",todo)

def p_declaracion_3(p):
    '''declaracion : tipo ID IGUAL STRING PUNTOYCOMA
    '''
    todo = "Ejem_"+str(p[2])+" "+str(p[3])+str(p[4])+" "+str(p[5])
    p[0] = Node("parametros", todo)


def p_tipo(p):
    '''tipo : INT
            | CHAR
            | VOID
            | STRINGJC
    '''
    p[0] = p[1]


#**************************************************************************************************

a = [ ]
def p_cout(p):
    '''cout : COUT DOBLEMENORQUE repcout PUNTOYCOMA
    '''
    p[0] = p[3]
    listacout = [ ]
    listacout2 = [ ]
    listacout3 = [ ]
    for x in p[0].split("<<"):
        i = 0
        listacout.append(x)
        comillas = '"'
        endl = "endl"
        ejem = "None + "
        id = r'\w+(_\d\w)*'
        while i < len(listacout):
                if listacout[i].isdigit() == True:
                    stcout = "$("+comillas+"#consola"+comillas+").append("
                    todo =  stcout+str(listacout[i])+'); $("#consola").append(" ");'
                    listacout2 = todo
                else:
                    b = comillas in listacout[i]
                    if b == True:
                        stcout = "$("+comillas+"#consola"+comillas+").append("
                        todo =  stcout+str(listacout[i])+'); $("#consola").append(" ");'
                        listacout2 = todo
                    else:
                            a = endl in listacout[i]
                            if a == True:
                                listacout2 = '$("#consola").append("<br>");'
                            else:
                                c = ejem in listacout[i]
                                if c == True:
                                    d = listacout[i].replace("None + ","$("+comillas+"#consola"+comillas+").append(")
                                    listacout2 = d + ");"
                                else:
                                        stcout = "$("+comillas+"#consola"+comillas+").append("
                                        todo =  stcout+"Ejem_"+str(listacout[i])+'); $("#consola").append(" ");'
                                        todo = todo.replace(" ","")
                                        listacout2 = todo
                i = i+1
        listacout3.append(listacout2)
        cadena = ''
        l = len(listacout3)
        for x in range(0,l):
            cadena = cadena+listacout3[x]
        p[0] = Node("cout",cadena)



def p_repcout(p):
    '''repcout : repcout cout1
    | cout1
    '''
    if len(p) == 3:
        p[0] = str(p[2])
    elif len(p) == 2:
        p[0] = str(p[1])

def p_cout1(p):
    '''cout1 :  general repcout
    | DOBLEMENORQUE general
    | general
    '''
    if len(p) == 2:
        p[0] = str(p[1])
    elif len(p) == 3:
        p[0] = str(p[1])+str(p[2])
    elif len(p) == 4:
        p[0] = str(p[1])+str(p[2])+str(p[3])


def p_general(p):
    '''general : STRING
    | ID
    | NUMBER
    | callcout
    | ENDL
    | STRING DOBLEMENORQUE general
    | ID DOBLEMENORQUE general
    | NUMBER DOBLEMENORQUE general
    | callcout DOBLEMENORQUE general
    | ENDL DOBLEMENORQUE general
    | STRING DOBLEMENORQUE STRING
    | ID DOBLEMENORQUE ID
    | NUMBER DOBLEMENORQUE NUMBER
    | callcout DOBLEMENORQUE callcout
    | ENDL DOBLEMENORQUE ENDL
    | DOBLEMENORQUE STRING
    | DOBLEMENORQUE ID
    | DOBLEMENORQUE NUMBER
    | DOBLEMENORQUE callcout
    | DOBLEMENORQUE ENDL
    | general
    '''
    if len(p) == 4:
        p[0] = str(p[1])+str(p[2])+str(p[3])
    elif len(p) == 3:
        p[0] = str(p[1])+str(p[2])
    elif len(p) == 2:
        p[0] = str(p[1])



def p_cin (p):
    ''' cin : CIN DOBLEMAYORQUE repcin PUNTOYCOMA
    '''
    p[0] = p[3]
    listacin = [ ]
    listacin2 = [ ]
    listacin3 = [ ]

    for x in p[0].split(">>"):
        i = 0
        listacin.append(x)
        while i < len(listacin):
            comillas = '"'
            cin = "$("+comillas+"#consola"+comillas+").append("+"Ejem_"
            todo = cin+listacin[i]+"=prompt('Inserte el dato:',''));$('#consola').append('<br>');"
            #Ejem_"+listacin[i]+"=parseInt(Ejem_"+listacin[i]+"); if(isNaN("+ "Ejem_"+listacin[i]+")==true) "+ "Ejem_"+listacin[i]+" = 0; $('#consola').append('<br>');"
            listacin2 = todo
            i = i+1
        listacin3.append(listacin2)
        cadena = ''
        l = len(listacin3)
        for x in range(0,l):
            cadena = cadena+listacin3[x]
        p[0] = Node("cin",cadena)

def p_repcin(p):
    '''repcin : repcin cin1
    | cin1
    '''
    if len(p) == 3:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]

def p_cin1(p):
    '''cin1 :  generalcin repcin
    | DOBLEMAYORQUE generalcin
    | generalcin
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = str(p[1])+str(p[2])
    elif len(p) == 4:
        p[0] = str(p[1])+str(p[2])+str(p[3])


def p_generalcin(p):
    '''generalcin : ID
    | ID DOBLEMAYORQUE generalcin
    | ID DOBLEMAYORQUE ID
    | DOBLEMAYORQUE ID
    | generalcin
    '''
    if len(p) == 4:
        p[0] = str(p[1])+str(p[2])+str(p[3])
    elif len(p) == 3:
        p[0] = str(p[1])+str(p[2])
    elif len(p) == 2:
        p[0] = p[1]


def p_inc (p):
    ''' inc : ID PLUS PUNTOYCOMA
    '''
    p[0] = " Ejem_"+str(p[1])+str(p[2])+str(p[3])

def p_inc_1 (p):
    ''' inc : PLUS ID PUNTOYCOMA
    '''
    p[0] = str(p[1])+" Ejem_"+str(p[2])+str(p[3])

def p_dec (p):
    ''' dec : ID MENOSMENOS PUNTOYCOMA
    '''
    p[0] = " Ejem_"+str(p[1])+str(p[2])+str(p[3])

def p_dec (p):
    ''' dec : MENOSMENOS ID PUNTOYCOMA
    '''
    p[0] = str(p[1])+" Ejem_"+str(p[2])+str(p[3])



   # no permite declaraciones, DOBLE IGUAL AGREGADO.
def p_ciclos(p):
    '''ciclos :  ID IGUAL NUMBER
    | ID DOBLEIGUAL NUMBER
    | ID MENORQUE NUMBER
    | ID MAYORQUE NUMBER
    | ID MENOROIGUAL NUMBER
    | ID MAYOROIGUAL NUMBER
    | ID IGUAL ID
    | ID DOBLEIGUAL ID
    | ID MENORQUE ID
    | ID MAYORQUE ID
    | ID MENOROIGUAL ID
    | ID MAYOROIGUAL ID
    | ID DISTINTODE NUMBER
    | ID DISTINTODE ID
    '''
    if len(p) == 4:
        if str(p[3]).isdigit():
            todo = str(p[1])+str(p[2])+str(p[3])
            id = str(p[1])
        else:
            todo = str(p[1])+str(p[2])+" Ejem_"+str(p[3])
            id = str(p[1])
    elif len(p)== 3:
        todo = str(p[1])++str(p[2])+str(p[3])
        id = str(p[1])
    p[0] = Node("ciclos", todo , id)


def p_ciclos_1(p):
    '''ciclos : ID PLUS
    | ID MENOSMENOS
    | ID DOBLEIGUAL
    | ID DISTINTODE
    | ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = "Ejem_"+str(p[1])+str(p[2])


def p_seleccion(p):
    '''seleccion : IF PARENTESISIZQUIERDO ciclos PARENTESISDERECHO LLAVEIZQUIERDA contenidos LLAVEDERECHA
    | IF PARENTESISIZQUIERDO ciclos PARENTESISDERECHO  LLAVEIZQUIERDA contenidos LLAVEDERECHA ELSE  LLAVEIZQUIERDA contenidos LLAVEDERECHA
    '''
    try:
        a = p[11]
        contenido = str(p[1])+" "+str(p[2])+" Ejem_"+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "+str(p[7])+" "+str(p[8])+" "+str(p[9])+" "+str(p[10])+" "+str(p[11])
    except:
        try:
            a = p[7]
            contenido = str(p[1])+" "+str(p[2])+" Ejem_"+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "+str(p[7])
        except:
            pass
    p[0] = Node("if",contenido, contenido)



def p_iteracion(p):
    'iteracion : WHILE PARENTESISIZQUIERDO ciclos PARENTESISDERECHO  LLAVEIZQUIERDA contenidos  LLAVEDERECHA'
    contenido = str(p[1])+" "+str(p[2])+" Ejem_"+str(p[3])+" "+str(p[4])+str(p[5])+str(p[6])+str(p[7])
    p[0] = Node("while", contenido)


def p_repeticion(p):
    '''repeticion : FOR PARENTESISIZQUIERDO ciclos PUNTOYCOMA  ciclos PUNTOYCOMA ciclos PARENTESISDERECHO LLAVEIZQUIERDA contenidos LLAVEDERECHA
    '''
    contenido = str(p[1])+str(p[2])+"Ejem_"+str(p[3])+str(p[4])+" Ejem_"+str(p[5])+str(p[6])+str(p[7])+str(p[8])+str(p[9])+str(p[10])+str(p[11])
    p[0] = Node("for", contenido)



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
    try:
        a = p[2]
        if str(p[2]).isdigit() == True:
            p[0] = str(p[1])+str(p[2])
        else:
            p[0] = str(p[1])+"parseInt( Ejem_"+str(p[2])+")"
    except:
        pass



def p_ope_list(p):
    'ope_list : ope_list operadores'
    p[0] = str(p[1])+str(p[2])

def p_ope_list_1(p):
    'ope_list : empty'
    p[0] = ""


def p_operaciones(p):
    '''
    operaciones : ID IGUAL ID ope_list PUNTOYCOMA
    | ID IGUAL NUMBER ope_list PUNTOYCOMA
    | ID IGUAL ID PUNTOYCOMA
    | ID IGUAL NUMBER PUNTOYCOMA
    | ID IGUAL ID PARENTESISIZQUIERDO PARENTESISDERECHO PUNTOYCOMA
    | ID IGUAL ID PARENTESISIZQUIERDO paramcallfun PARENTESISDERECHO ope_list PUNTOYCOMA
    '''
    try:
        a = p[8]
        todo = "Ejem_"+str(p[1])+str(p[2])+"( Ejem_"+str(p[3])+str(p[4])+str(p[5])+str(p[6])+str(p[7])+")"+str(p[8])
        todo = todo.replace("None","")
        todo = todo.replace(" ","")
    except:
        try:
            a = p[6]
            todo = "Ejem_"+str(p[1])+str(p[2])+" Ejem_"+str(p[3])+str(p[4])+str(p[5])+str(p[6])
        except:
            try:
                a = p[5]
                if str(p[3]).isdigit() == True:
                    todo = "Ejem_"+str(p[1])+str(p[2])+str(p[3])+str(p[4])+str(p[5])
                else:
                    todo = "Ejem_"+str(p[1])+str(p[2])+"parseInt(Ejem_"+str(p[3])+")"+str(p[4])+str(p[5])
            except:
                a = p[4]
                if str(p[3]).isdigit() == True:
                    todo = "Ejem_"+str(p[1])+str(p[2])+str(p[3])+str(p[4])
                else:
                    todo = "Ejem_"+str(p[1])+str(p[2])+"Ejem_"+str(p[3])+str(p[4])
    p[0] = Node("todo", todo)



def p_return(p):
    '''return : RETURN NUMBER PUNTOYCOMA'''
    todo = str(p[1])+str(p[2])+str(p[3])
    p[0] = Node("return", todo)


def p_return_1(p):
    '''return : RETURN ID PUNTOYCOMA'''
    todo = str(p[1])+" Ejem_"+str(p[2])+str(p[3])
    p[0] = Node("return", todo)

def p_idnumpow(p):
    '''idnumpow : idnumpow ID
    | idnumpow NUMBER
    | ID
    | NUMBER
    '''
    try:
        a = p[2]
        if str(p[2]).isdigit():
            retorno = str(p[2])
        else:
            retorno =" Ejem_" + str(p[2])
    except:
        a = p[1]
        if str(p[1]).isdigit():
            retorno = str(p[1])
        else:
            retorno =" Ejem_" + str(p[1])
        p[0] = Node("pow", retorno)

def p_pow(p):
    '''pow : POW PARENTESISIZQUIERDO idnumpow COMA idnumpow PARENTESISDERECHO
    | SIN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    | COS PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    | TAN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    | SQRT PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO
    '''
    retorno = ""
    p[0] = Node("pow", retorno)
    sin = "sin"
    cos = "cos"
    tan = "tan"
    sqrt = "sqrt"
    try:
        a = p[6]
        retorno ="+ Math.pow" + str(p[2])+str(p[3])+str(p[4])+str(p[5])+str(p[6])
    except:
        a = p[4]
        b = str(p[1])
        if str(p[3]).isdigit():
            retorno ="+ Math.sin" + str(p[2])+str(p[3])+str(p[4])
        else:
            if b == sin:
                retorno ="+ Math.sin" + str(p[2])+str(p[3]) + str(p[4])
            else:
                if b == cos:
                    retorno ="+ Math.cos" + str(p[2])+str(p[3]) + str(p[4])
                else:
                    if b == tan:
                        retorno ="+ Math.tan" + str(p[2])+str(p[3]) + str(p[4])
                    else:
                        if b == sqrt:
                            retorno ="+ Math.sqrt" + str(p[2])+str(p[3]) + str(p[4])
    p[0] = Node("pow", retorno)

def p_powgen(p):
    '''powgen : POW PARENTESISIZQUIERDO idnumpow COMA idnumpow PARENTESISDERECHO PUNTOYCOMA
    | SIN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | COS PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | TAN PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | SQRT PARENTESISIZQUIERDO idnumpow PARENTESISDERECHO PUNTOYCOMA
    | ID IGUAL powgen
    | ID IGUAL pow ope_list PUNTOYCOMA
    '''
    sin = "sin"
    cos = "cos"
    tan = "tan"
    sqrt = "sqrt"
    try:
        a = p[7]
        retorno = "Math.pow" + str(p[2])+str(p[3]) + str(p[4])+str(p[5])+ str(p[6])+ str(p[7])
    except:
        try:
            a = p[5]
            b = str(p[1])
            if b != sin and b != cos and b != tan and b != sqrt:
                retorno = "Ejem_"+str(p[1])+ str(p[2])+str(p[3]) + str(p[4]) + str(p[5])
            else:
                if str(p[3]).isdigit():
                    retorno ="Math.sin" + str(p[2])+str(p[3]) + str(p[4]) + str(p[5])
                else:
                    if b == sin:
                        retorno ="Math.sin" + str(p[2])+str(p[3]) + str(p[4]) + str(p[5])
                    else:
                        if b == cos:
                            retorno ="Math.cos" + str(p[2])+str(p[3]) + str(p[4]) + str(p[5])
                        else:
                            if b == tan:
                                retorno ="Math.tan" + str(p[2])+str(p[3]) + str(p[4]) + str(p[5])
                            else:
                                if b == sqrt:
                                    retorno ="Math.tan" + str(p[2])+str(p[3]) + str(p[4]) + str(p[5])
        except:
            a = p[3]
            retorno = " Ejem_"+str(p[1]) + str(p[2]) + str(p[3])
    p[0] = Node("pow", retorno)

def p_empty(p):
    'empty :'
    pass


def t_error(self,p):
    pass

def parse(data, debug=True):
    lexer = Lexer()
    lexer.build()
#    yacc.yacc()
    yacc.yacc(optimize=1,debug=False, write_tables=False)
    return yacc.parse(data, lexer=lexer.lexer)
def main(data):
    while len(traduccion) > 0:traduccion.pop()
    respuesta = { }
    l = Lexer()
    l.build()
    parse(data)
    #limpiamos la lista
    global tr
    global none
    if traduccion == [ ]:
        respuesta['estado'] = 'correcto'
        respuesta['error']= 'Analisis 4, traduccion OK.'
    else:
        com ="'"
        tr = str(traduccion)
        com = r'None'
        a = tr.replace("None", "")
        a = a.replace("[", " ")
        a = a.replace("]", " ")
        none = a
        respuesta['codigo'] = none
    respuesta['estado'] = 'correcto'
    respuesta['error'] = 'correcto'
    return respuesta
