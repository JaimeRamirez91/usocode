# -*- enconding: utf-8 -*-
#!/usr/bin/python
import re
import os

import sys
VERBOSE = 1
add =[ ]
new =[ ]
f = [ ]
def Traductor(data):
    #expresiones de busqueda
    r = r'[a-z]+-?[a-z]+ ?'
    id = r'\w+(_\d\w)*'
    paren = r'\(\)'
    int = r'int+[ ?]*'
    igual =  r'[ ?*] = +[ ?]*'
    cin = r'cin+[ ?]*'
    m = r'[\>\>]+[ ?]*'
    #cout
    cout = r'cout+[ ?]*'
    dobmen = r'[\<\<]+[ ?]*'
    coment = r'["]'
    coutp = str(cout)+str(dobmen)+str(coment)+str(id)+str(coment)

    #------------------------------------------------------------
    # uniones de expreciones
    #-----------------------------------------------------------
    t_funcion = str(int)+str(r)+str(paren)
    t_var_int = str(int)+str(id)
    t_c_in = str(cin)+str(m)+str(id)
    #------------------------------------------------------------
    #text = "int solo (){   int i   int i=9; int i; i=c+b+d cout << cout<<  } INT hh (){} "
    #text = data.replace(r'INT', 'int')

#funciones
    for m in re.finditer(t_funcion, data):
       tx=data
       a = '%s' % (m.group(0))
       x = a.replace(r'int ', 'function ')
      # print x
       b= tx.replace(a,x)
       data = b
#var int
    for m in re.finditer(t_var_int, data):
       tx=data
       a = '%s' % (m.group(0))
       x = a.replace(r'int ', 'var ')
      # print x
       b= tx.replace(a,x)
       data = b
#cin
    for m in re.finditer(t_c_in, data):
       tx=data
       ausiliar =""
       a = '%s' % (m.group(0))
       comillas = "'"
       for n in re.finditer(id, a):
          e = '%s' % (n.group(0))
          if e == 'cin':
            pass
          else:
              ausiliar = e
       x = a.replace(ausiliar,'')
       x = x.replace('>>','')
       x = x.replace('cin','$("#consola").append("<input name='+comillas+ausiliar+comillas+' class='+comillas+'Ejem_'+ausiliar+comillas+'><br>")')
       b= tx.replace(a,x)
       data = b
    data = data.replace(r'<<endl', '<br>')
    for n in re.finditer(coutp, data):
        tx=data
        auxiliar= " "
        a = '%s' % (n.group(0))
        comillas = '"'
        x = a.replace(r'cout' , '$("#consola").append(')
        x= x.replace (r'<<', ' ')
        x= x.replace (r'"', '')
        for m in re.finditer(id, a):
            e = '%s' % (m.group(0))
            if e == 'cout':
              pass
            else:
                auxiliar = e
        x= x.replace(auxiliar,comillas+auxiliar+comillas+')')
        b= tx.replace(a,x)
        data = b
        pass
    

    respuesta = {}
    respuesta['estado'] = 'correcto'
    respuesta['codigo'] = data
    respuesta['error']="aqui hay un error"
    return respuesta

'''if __name__ == '__main__':

    if (len(sys.argv) > 1):
        fin = sys.argv[1]
    else:
        fin = 'fuente/c++.cpp'
        f = open(fin,'r')
        data = f.read()
        Traductor(data)'''


