import requests, itertools as it
import urllib.request
import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
from csv import DictWriter

url = 'https://www.eleicoes.mai.gov.pt/legislativas2005/be_ftp.html#'

uClient = urlopen(url)

soup = BeautifulSoup(uClient.read(), "html.parser")

filename = "2002.csv"
f = open(filename, "w")

headers = "cargos\n"
f.write(headers)

list1 = ['', 'aveiro', 'beja', 'braga', 'braganca', 'castelo', 'coimbra', 'evora', 'faro', 'guarda', 'leiria', 'lisboa', 'madeira', 'portalegre', 'porto', 'santarem', 'setubal', 'viana', 'vila', 'viseu']
list2 = ['be', 'cdu', 'cds', 'ph', 'pnd', 'pnr', 'pctp', 'pous', 'pda', 'psd', 'ps']

c = soup.findAll("td", {"class": "bckgrd"}) #candidate and position tags
d1 = soup.findAll("td", {"class": "ligacoes"}) #districts 1
d2 = soup.findAll("span", {"class": "ligacoes"}) #districts 2

# sobreposição de Beja, Braga, Bragança e Coimbra

#for i in list2:
	#url = 'https://www.eleicoes.mai.gov.pt/legislativas2005/{}_ftp.html#'.format(i)
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")
	#print(soup.span)


def get_page(district):
	d = list(filter(lambda x:x != '\n', BeautifulSoup(requests.get(f'https://www.eleicoes.mai.gov.pt/legislativas2005/{district}_ftp.html#viana').text, 'html.parser').table.contents))[7:-2]
	new_d, last, c = [[i.find('td', {'class':'ligacoes'}), [[k.text for k in b.find_all('td')] for b in i.find_all('tr', {'valign':'bottom'})]] for i in d], None, []
	for a, b in new_d:
		if a is None:
			c.extend([j for _, j in b])
		elif last is None:
			last = a.text        
			c.extend([j for _, j in b])
		else:
			yield {'name':last, 'vals':c}
			last, c = a.text, [j for _, j in b]
	yield {'name':last, 'vals':c}

result = [{'name':i, 'party':'be', 'district':k['name']} for k in get_page('be') for i in k['vals']] #por página do partido;
																									 #necessário fazer alterações

#result = [[{'name':i, 'party':'be', 'district':k['name']} for k in get_page(party) for i in k['vals']] for party in list2] #ERRO: be fixo

with open('be_2005.csv', 'w') as outfile:
	writer = DictWriter(outfile, ('name', 'party', 'district'))
	writer.writerows(result)

