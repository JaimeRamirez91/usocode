#!/usr/bin/python
# -*- encondig: utf-8 -*-
import ply.lex as lex
import os
import sys
from sys import exit
error=[ ]
# lista de tokens
class Lexer(object):
     tokens = (
        'INCLUDE',
        'NAMESPACE_MOD',
        'COUT',
        'CIN',
        'GET',
        'ENDL',
        'ELSE',
        'IF',
        'INT',
        'STRING',
        'STRINGJC',
        'CHAR',
        'VOID',
        'WHILE',
        'FOR',
        'RETURN',
        'POW',
        'SIN',
        'COS',
        'TAN',
        'SQRT',

        'NUMERAL',
        'PUNTO',
        'MAS',
        'PLUS',
        'MENOS',
        'MENOSMENOS',
        'ASTERISCO',
        'DIVISION',
        'MATH',
        'MENORQUE',
        'MAYORQUE',
        'MAYOROIGUAL',
        'MENOROIGUAL',
        'IGUAL',
        'DOBLEIGUAL',
        'DISTINTODE',
        'PUNTOYCOMA',
        'COMA',
        'DOBLEMENORQUE',
        'DOBLEMAYORQUE',
        'PARENTESISIZQUIERDO',
        'PARENTESISDERECHO',
        'CORCHETEIZQUIERDO',
        'CORCHETEDERECHO',
        'LLAVEIZQUIERDA',
        'LLAVEDERECHA',
        'COMILLASDOBLES',
        'ID',
        'NUMBER',
        'PORCENTAJE',
     )
     t_ignore = ' \t'
#     t_ignore_COMMENT = r'[//]+[^\n]*'
     t_MAS = r'\+'
     t_MENOS = r'-'
     t_MENOSMENOS = r'\-\-'
     t_PUNTO = r'\.'
     t_ASTERISCO = r'\*'
     t_IGUAL = r'='
     t_MENORQUE = r'<'
     t_MAYORQUE = r'>'
     t_PUNTOYCOMA = ';'
     t_COMA = r','
     t_PARENTESISIZQUIERDO = r'\('
     t_PARENTESISDERECHO = r'\)'
     t_CORCHETEIZQUIERDO = r'\['
     t_CORCHETEDERECHO = r'\]'
     t_COMILLASDOBLES = r'\"'

     def t_comments(self,t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

     def t_comments_C99(self,t):
          r'//(.)*?\n'
          t.lexer.lineno += 1

     def t_NAMESPACE_MOD(self,t):
         r'using+[ *]+namespace+[ *]+std'
         return t

     def t_INCLUDE(self,t):
         r'include'
         return t

     def t_COUT(self,t):
          r'cout'
          return t

     def t_CIN(self,t):
         r'cin'
         return t

     def t_GET(self,t):
         r'get'
         return t

     def t_ENDL(self,t):
         r'endl'
         return t

     def t_ELSE(self,t):
         r'else'
         return t

     def t_IF(self,t):
         r'if'
         return t

     def t_INT(self,t):
         r'int'
         return t

     def t_STRINGJC(self,t):
         r'string'
         return t

     def t_CHAR(self,t):
         r'char'
         return t

     def t_RETURN(self,t):
         r'return'
         return t

     def t_VOID(self,t):
         r'void'
         return t

     def t_WHILE(self,t):
         r'while'
         return t

     def t_FOR(self,t):
         r'for'
         return t

     def t_POW(self,t):
         r'pow'
         return t

     def t_SIN(self,t):
         r'sin'
         return t

     def t_COS(self,t):
         r'cos'
         return t

     def t_TAN(self,t):
         r'tan'
         return t

     def t_SQRT(self,t):
         r'sqrt'
         return t

     def t_NUMBER(self,t):
          r'\d+'
          t.value = int(t.value)
          return t

     def t_ID(self,t):
          r'\w+(_\d\w)*?'
          return t
#cambios realizados el 27-11-2015 por jarv----------------------
     def t_STRING(self, t):
        r'"[( *?)]+[w+_\d\ \w\:\.\,\;]*"|"[w+_\d\ \w\:\.\,\;]*"'
        return t

     def t_MATH(self,t):
        r'\.\h'
        return t

     def t_NUMERAL(self,t):
          r'\#'
          return t


     def t_PLUS(self,t):
          r'\+\+'
          return t


     def t_MENOROIGUAL(self,t):
            r'<='
            return t


     def t_MAYOROIGUAL(self,t):
            r'>='
            return t

     def t_DIVISION(self,t):
            r'/'
            return t


     def t_DOBLEIGUAL(self,t):
            r'=='
            return t


     def t_LLAVEIZQUIERDA(self,t):
            r'{'
            return t


     def t_LLAVEDERECHA(self,t):
          r'}'
          return t

     def t_DOBLEMENORQUE(self,t):
            r'\<\<'
            return t

     def t_DOBLEMAYORQUE(self,t):
            r'\>\>'
            return t

     def t_DISTINTODE(self,t):
          r'\!\='
          return t

     def t_PORCENTAJE(self,t):
          r'\%'
          return t

     def t_newline(self,t):
          r'\n+'
          t.lexer.lineno = t.lexer.lineno + len(t.value)


     def t_error(self,t):
          try:
              str(t.value).decode('utf-8')
              a =  ( u"Linea %d: caracter >> %s << ilegal !!NO SOPORTADO EN LA IMPLEMANTACION DE USOCODE!!!! revise el fragmento de codigo." %(t.lexer.lineno, t.value[0]))
          except UnicodeError:
                a =  ( u"Linea %d: caracter ilegal  detectado !!NO SOPORTADO EN LA IMPLEMANTACION DE USOCODE!!!! revise el fragmento de codigo." %(t.lexer.lineno))
          error.append(a)
          t.lexer.skip(1)
     def build(self, **kwargs):
#-------------------------original-------------------------------
#        self.lexer = lex.lex(module=self, **kwargs)
#------------------modo optimizado----------------------
          self.lexer = lex.lex(module=self,optimize = 1)

     def test(self, data):
         self.lexer.input(data)
         while True:
               token = self.lexer.token()
               if not token:
                  break
def lexer(data):
    respuesta = { }
    l = Lexer()
    l.build()
    #limpiamos la lista
    while len(error) > 0 : error.pop()
    l.test(data)
    if error == [ ]:
        respuesta['estado'] = 'error'
        respuesta['codigo'] = 'Analisis 1, Lexer OK.'
    else:
        respuesta['estado'] = 'error'
        try:
            respuesta['codigo']= error[0]
        except:
            respuesta['codigo']= error
    return respuesta
