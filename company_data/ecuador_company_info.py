import time
#import scrapy
import selenium
#from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
from collections import namedtuple

# https://sqa.stackexchange.com/questions/1941/how-do-i-close-the-browser-window-at-the-end-of-a-selenium-test
# https://intellipaat.com/community/27189/selenium-close-browser-how-to-close-the-whole-browser-window-by-keeping-the-webdriver-active
# http://allselenium.info/how-to-handle-exceptions-in-selenium-python-webdriver/

# https://stackoverflow.com/questions/16201094/how-to-reference-an-exception-class-in-python
# https://stackoverflow.com/questions/40198924/handling-imported-module-exceptions
# https://www.pingshiuanchua.com/blog/post/error-handling-in-selenium-on-python

def parse_info_general(soup, outfile="testout.json"):

	# the page is annoying - the field name is randomly generated each time the data is loaded, even for the same company
	# however, it seems that the SUFFIX (last 2 chars) of the field remain constant
	# so basically we will find randomly-generated PREFIX each time we load the page
	# after that we can use the 'matches' table and pull out the data values for each field
	# but we'll include a sanity check that the correspondence doesn't change

	fields = soup.find_all('span', class_="z-label")
	Datafield = namedtuple('Datafield', 'suffix fieldname')

	# hand-assembled correspondence between the suffix of the field NAME, and the suffix containing the field VALUE
	# the field ending in "02" is the spot displaying "expediente", the field ending in "12" has the value thereof
	matches = {
			"02" : Datafield("12", "Expediente"),
			"22" : Datafield("32", "Nombre Comercial"),
			"42" : Datafield("52", "Ruc"),
			"72" : Datafield("82", "Fecha de Constitución"),
			get_comp"92" : Datafield("a2", "Nacionalidad"),
			"b2" : Datafield("c2", "Plazo Social"),
			"e2" : Datafield("f2", "Tipo Compañía"),
			"g2" : Datafield("h2", "Oficina de Control"),
			"i2" : Datafield("j2", "Situación Legal"),
			"p2" : Datafield("q2", "Provincia"),
			"r2" : Datafield("s2", "Cantón"),
			"t2" : Datafield("u2", "Ciudad"),
			"w2" : Datafield("x2", "Parroquia"),
			"y2" : Datafield("z2", "Calle"),
			"_3" : Datafield("03", "Numero"),
			"23" : Datafield("33", "Intersección"),
			"43" : Datafield("53", "Ciudadela"),
			"63" : Datafield("73", "Conjunto"),
			"93" : Datafield("a3", "Edificio/Centro Comercial"),
			"b3" : Datafield("c3", "Barrio"),
			"d3" : Datafield("e3", "Km"),
			"g3" : Datafield("h3", "Camino"),
			"i3" : Datafield("j3", "Piso"),
			"k3" : Datafield("l3", "Bloque"),
			"n3" : Datafield("o3", "Referencía Ubicación"),
			"u3" : Datafield("v3", "Casillero Postal"),
			"w3" : Datafield("x3", "Celular"),
			"y3" : Datafield("z3", "Fax"),
			"04" : Datafield("14", "Teléfono 1"),
			"24" : Datafield("34", "Teléfono 2"),
			"44" : Datafield("54", "Sitio Web"),
			"74" : Datafield("84", "Correo 1"),
			"94" : Datafield("a4", "Correo 2"),
			"g4" : Datafield("h4", "¿Es proveedora de bienes o servicios del estado?"),
			"i4" : Datafield("j4", "¿Ofrece servicios de pago a remesas?"),
			"k4" : Datafield("l4", "¿Compañía vende a crédito?"),
			"n4" : Datafield("o4", "¿Pertenece a MV?"),
			"p4" : Datafield("q4", "Fecha de última actualización - Seguros"),
			"r4" : Datafield("s4", "Fecha de última actualización - Societario"),
			"w4" : Datafield("x4", "¿Es sociedad de interés público?"),
			"y4" : Datafield("z4", "Disposición judicial que afecta la compañía"),
			"45" : Datafield("55", "Objeto Social"),
			"75" : Datafield("85", "Ciiu Actividad Nivel 2"),
			"95" : Datafield("c5", "Descripción"),
			"g5" : Datafield("h5", "Ciiu Operación Principal"),
			"i5" : Datafield("l5", "Descripción"),
			"r5" : Datafield("s5", "Capital suscrito"),
			"t5" : Datafield("u5", "Capital Autorizado"),
			"v5" : Datafield("w5", "Valor Nominal"),
	}

	dataout = dict()

	data_flag = False
	for field in fields:
		# first find the field which has company name
		# only after finding the name (and hence prefix) do we start searching for field/value pairs
		if field['id'].endswith('u1'):
			dataout['company_name'] = field.text
			data_flag = True			# toggle flag to begin field/value searching
			prefix = field['id'][:-2]

		if data_flag:
			suffix = field['id'][-2:]
			if suffix in matches:
				datafield = matches[suffix]
				data_obj = soup.find(id = prefix + datafield.suffix)
				
				try:
					# for most of the fields, the payload is stored as the "value" attribute
					payload = data_obj.attrs['value']
				except KeyError:
					# for a couple of the fields, the payload is stored as the text
					payload = data_obj.text
				dataout[field.text] = payload.strip()

				# sanity-check
				assert datafield.fieldname == field.text

	with open(outfile, 'a', encoding='utf8') as f:
		f.write(json.dumps(dataout, ensure_ascii=False) + '\n')  # don't use ASCII, since we have so many latin characters
	return dataout



#############################################

driver = webdriver.Chrome('./chromedriver/chromedriver')
target_base = "https://appscvsmovil.supercias.gob.ec/portaldeinformacion/consulta_cia_menu.zul?expediente="
# https://appscvsmovil.supercias.gob.ec/portaldeinformacion/consulta_cia_menu.zul?expediente=131


results_file = "resultados.json"

# reset file
with open(results_file, 'w') as f:
	f.write('')

time.sleep(1)


#skipped = [20855, 22514, 88376] 
#skipped = [8373]        # "No se encontraron registros para el expediente ingresado."

for num in range(1,185000):
	target = target_base + str(num)
	print('\n\n\t' + target)

	try:
		driver.get(target)
	except TimeoutException:
		print("Timeout; restarting the driver.")
		driver.quit()
		time.sleep(5)
		driver = webdriver.Chrome('./chromedriver/chromedriver')
		driver.get(target)
		

	"""
	The iconos end up being:
	0	:	Información General
	1	:	Administradores
	2	:	Actos Jurídicos
	3	:	Información Anual
	4	:	Consulta de Cumplimiento
	5	:	
	6	:	Socio o Accionistas
	7	:	Documentos Online
	8	:	Información Estados Financieros
	9	:	Kardex
	10	:	Valores Adeudados
	11	:	Notificaciones Generales
	12	:	Valores Pagados
	"""
	iconos = driver.find_elements_by_class_name("m_iconos")
	iconos[0].click()	# brings up new HTML code, rendered via javascript

	time.sleep(0.5)

	# metadata about how well each company worked; if we can't get the payload, save it instead (just for the record)
	meta = {'num' : num, 'n_try':0, 'server_errs':0} 

	# parse the new page using BeautifulSoup
	i = 0
	while True:
#		fname = "./pages/company_{0:06d}".format(num) + ".html"
		i += 1
		meta['n_try'] = i
		if i >= 10 :
			# give up if we haven't gotten it after a few tries
			with open(results_file, 'a') as f:
				f.write(json.dumps(meta) + '\n')
			break

		# parse the page, but sometimes the server randomly isn't available, so just wait and retry
		try:
			soup = BeautifulSoup(driver.page_source, 'html')
		except Exception:
			print("...WTF MATE??")
			meta['server_errs'] = meta['server_errs'] + 1
			time.sleep(2)
			continue

		fields = soup.find_all('span', class_="z-label")

		match = "INFORMACIÓN GENERAL DE LA COMPAÑÍA"
		if len(fields) > 1 and (fields[1].text == match):
			# if we've matched the field that shows the new data has come up, save the page
			print('\t\tSaving data...')
#			with open(fname, 'w') as f:
#				f.write(driver.page_source)
			dataout = parse_info_general(soup, results_file)
			break

		else:
			# wait and try again
			print('\t\t...waiting...(' + str(i) + ')')
			time.sleep(0.5)


	
