import requests
import time
import json
import datetime

#import subprocess


def merge_datasource(vacdata,disdata):
	mapping_key = {
	'DE-BW':{'name':'Baden-Württemberg'     , 'guid':'80394ddf-c6a4-4a6e-be8e-0259a81b22a9'},
	'DE-BY':{'name':'Bayern'                , 'guid':'1ff920f4-62cd-4a4f-b8c9-f042f2a3e00a'},
	'DE-BE':{'name':'Berlin'                , 'guid':'c7033073-2bb0-486b-97af-5b3c639e7219'},
	'DE-BB':{'name':'Brandenburg'           , 'guid':'b560af89-5895-4be4-96f8-0f581cd8a858'},
	'DE-HB':{'name':'Bremen'                , 'guid':'4132268b-54de-4327-ac1e-760e915112f1'},
	'DE-HH':{'name':'Hamburg'               , 'guid':'0f3e860c-5181-4d3f-a421-1d51f50315ea'},
	'DE-HE':{'name':'Hessen'                , 'guid':'93277ac4-e8fc-48c7-8940-028dc2ed66af'},
	'DE-MV':{'name':'Mecklenburg-Vorpommern', 'guid':'a27f5628-e790-45be-898d-f0a6841c0f7e'},
	'DE-NI':{'name':'Niedersachsen'         , 'guid':'3fd77024-c29b-4843-9be8-682ad48e60c9'},
	'DE-NW':{'name':'Nordrhein-Westfalen'   , 'guid':'561d658f-3ee5-46e3-bc95-3528c6558ab9'},
	'DE-RP':{'name':'Rheinland-Pfalz'       , 'guid':'e9b4296f-9be2-4e53-9a58-ccf1396cb03d'},
	'DE-SL':{'name':'Saarland'              , 'guid':'e3396a6f-8a30-4fdf-8df7-def77dd38bea'},
	'DE-SN':{'name':'Sachsen'               , 'guid':'256d2405-a7c8-4fec-93df-29f3c808cd25'},
	'DE-ST':{'name':'Sachsen-Anhalt'        , 'guid':'66106bbe-f04b-4f92-80e1-5b5b30da25b5'},
	'DE-SH':{'name':'Schleswig-Holstein'    , 'guid':'fc5ba936-c95c-432c-8a33-9eb2f30b660f'},
	'DE-TH':{'name':'Thüringen'             , 'guid':'3a3e2817-bb19-4f8c-8bca-d8ff591140d4'}
	}
	return_list = []
	for this_vac in vacdata:
		return_object = {}
		for this_dis in disdata:
			if (mapping_key[this_vac['code']]['guid'] == this_dis['GlobalID']):
				return_object['name'] = this_dis['LAN_ew_GEN']
				return_object['shortname'] = this_vac['code']
				return_object['vacchalf'] = int(this_vac['peopleFirstTotal'])
				return_object['vaccfull'] = int(this_vac['peopleFullTotal'])
				return_object['guid'] = this_dis['GlobalID']
				return_object['cases7'] = int(this_dis['cases7_bl'])
				return_object['cases'] = int(this_dis['Fallzahl'])
				return_object['died'] = int(this_dis['Death'])
				return_object['population'] = int(this_dis['LAN_ew_EWZ'])
				return_list.append(return_object)
	return(return_list)

def csv_parse(data,seperator):
	return_list = []
	list_of_rows = data.split("\n")	
	fieldnames = list_of_rows[0].split(seperator)
	for row_number in range(1,len(list_of_rows)):
		row_values = list_of_rows[row_number].split(seperator)
		if (len(row_values) == len(fieldnames)):
			row_dict = {}
			for col_number in range(0,len(fieldnames)):
				row_dict[fieldnames[col_number]] = row_values[col_number]
			return_list.append(row_dict)
		else:
			print('+++'+str(row_values))
	return(return_list)


def get_vac_data():
	#downloads current data about vaccination
	r = requests.get('https://impfdashboard.de/static/data/germany_vaccinations_by_state.tsv')
	vac_data = r.text
	# parsing
	vac_data3 = csv_parse(vac_data,'\t')
	return(vac_data3)


def get_dis_data():
	#downloads current data about diseese
	r = requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?where=1%3D1&outFields=LAN_ew_GEN,OBJECTID,GlobalID,cases7_bl_per_100k,cases7_bl,LAN_ew_EWZ,Fallzahl,Death&outSR=4326&f=json')
	dis_data = r.json()
	return_list = []
	for this_featureset in dis_data['features']:
		return_list.append(this_featureset['attributes'])
	return(return_list)


def get_rounded(f):
	foo = f*10
	foo = int(foo)
	foo = str(foo * 0.1)
	return(foo)

vaccinedata = get_vac_data()
incidencedata = get_dis_data()
print(vaccinedata)
print(incidencedata)
mergeddata = merge_datasource(vaccinedata,incidencedata)


markdown_output = '# Covid19 Impung und Inzidenz\n'
markdown_output += '\n'
markdown_output += 'In diesem Dokument soll die Inzidenz der Bundesländer in Relation zu ihrer Impfrate dargestellt werden.\n'
markdown_output += 'Genauer gesagt, zur Nicht-Geimpft-Rate.\n'
markdown_output += '\n'
markdown_output += '\n'

for this_bundesland in mergeddata:
	markdown_output += '### '+this_bundesland['name']+'\n'
	markdown_output += '\n'
	novac = this_bundesland['population'] - this_bundesland['vacchalf'] - this_bundesland['vaccfull']
	nofullvac = this_bundesland['population'] - this_bundesland['vaccfull']
	cases7_100k = 100000 * this_bundesland['cases7'] / this_bundesland['population']
	cases7_100k_novac = 100000 * this_bundesland['cases7'] / novac
	cases7_100k_nofullvac = 100000 * this_bundesland['cases7'] / nofullvac
	markdown_output += '| Inzidenz der letzten sieben Tage pro 100.000 Einwohner | '+get_rounded(cases7_100k)+' |\n'
	markdown_output += '| Inzidenz der letzten sieben Tage pro 100.000 ungeimpfte Einwohner | '+get_rounded(cases7_100k_novac)+' |\n'
	markdown_output += '| Inzidenz der letzten sieben Tage pro 100.000 teilweise oder gar nicht geimpfter Einwohner | '+get_rounded(cases7_100k_nofullvac)+' |\n'
	markdown_output += '\n'
	markdown_output += '\n'
	markdown_output += '\n'
markdown_output += '\n'
markdown_output += '\n'
markdown_output += 'In diesen Daten wurde nicht berücksichtigt, ob die jeweilige Impfung schon wirksam ist (nach ca. 14 Tagen), sondern lediglich ob geimpft wurde.\n'
markdown_output += '\n'
markdown_output += '----\n'
markdown_output += '\n'
markdown_output += '#### Datenquellen und Lizenz\n'
markdown_output += '\n'
markdown_output += 'Die erhobenen Daten stammen vom Robert Koch Institut und stehen unter [Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0)\n'
markdown_output += '\n'
markdown_output += '#### Benutzung\n'
markdown_output += '\n'
markdown_output += 'Die Datei collect_data.py läd die aktuellen Daten zur Inzidenz und zur Impfung von impfdashboard.de und vom COVID-19 Datenhub herunter und verbindet sie.\n'
markdown_output += 'Anschließend wird **diese Readme** hier erzeugt und die ermittelten Daten in einer Datei (nach Datum benannt) weggespeichert. Damit könnte man später Verlaufsgraphen generieren.\n'
markdown_output += 'Abschließend wird automatisch `git push` durchgeführt, damit die Daten aktualisiert werden.\n'

readmefilehandler = open("README.md", "w")
readmefilehandler.write(markdown_output)
readmefilehandler.close()
	
jsonfilehandler = open('collected_data/'+datetime.date.today().isoformat()+'.json', 'w')
json.dump(mergeddata, jsonfilehandler)
jsonfilehandler.close()
