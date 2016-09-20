def compila(codigo):
	# respuesta = '{"estado":"correcto","codigo":"David"}'
	codigo1 = codigo.split('\n')
	codigo_dev =''
	for i in codigo1:
		if codigo_dev=='':
			codigo_dev += '"' + i + '"'
		else:
			 codigo_dev += ',"' + i + '"'
	#borrar si se desea separar las lineas
	codigo_dev = codigo.replace('\n',' ')
	respuesta = {}
	respuesta['estado'] = 'correcto'
	respuesta['codigo'] = codigo_dev
	# respuesta = '{"estado":"correcto","codigo":"'+codigo_dev+'"}'
	return respuesta
