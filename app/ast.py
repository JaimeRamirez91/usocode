from collections import defaultdict
lista = []
class Node(object):

    source = "prog"
    funcs = []

    unique = defaultdict(int)

    def __init__(self, type, sub=None, value=None):
        self.type = type
        self.sub = sub or []
        self.value = value
#       self.lineno = lineno
        self.uvalue = None

        if self.type == "programa":
            Node.funcs.append(self)
            Node.unique[self.value] += 1
            self.uvalue = "%s_%d" % (self.value, Node.unique[self.value])

    def __repr__(self):
        if  self.type == "Funcion":
            return " %s  %s " % (self.value,self.sub,)
        elif  self.type == "todo":
            return "%s" % (self.sub)
        elif  self.type == "cout":
            return "%s" % (self.sub)
        elif  self.type == "for":
            a = "%s" % (self.sub)
            return "%s" % (self.sub)
        elif  self.type == "if":
            a = "%s" % (self.sub)
            return "%s" % (self.sub)
        elif  self.type == "ciclos":
            return "%s" % (self.sub,)
        elif self.type == "parametrosfun":
            return "%s" % (self.sub,)
        elif self.type == "ID":
            return "%s" % (self.sub,)
        elif self.type == "cin":
            return "%s" % (self.sub,)
        elif self.type == "dec_lst":
            return "%s" % (self.sub,)
        elif self.type == "encabezado":
            return "%s" % (self.sub,)
        else:
            return " %s %s " % (self.value , self.sub,)