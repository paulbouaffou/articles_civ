#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Description: Lister tous les articles wikipedia  de CIV qui manquent de sources secondaires
# Auteurs: Samuel Guebo & Paul Bouaffou
# Licence:

         

import json
import requests

# function to give resultat of url request
def runMediaWikiRequest(url):
	resultatJson = requests.get(url).content
	# return the json text
	return resultatJson
	

# get all articles from CIV archives
civ_archives_url = "https://fr.wikipedia.org/w/api.php?action=parse&format=json&page=Projet:C%C3%B4te_d%27Ivoire/Articles_r%C3%A9cents/Archive&prop=links" 
archives_json = runMediaWikiRequest(civ_archives_url)

# convert from plain text to python array, and browse to get items 'parse' and its child 'links'
archives_links = json.loads(archives_json)['parse']['links']  

# just the two first items of the array
links_test = archives_links[0:]

# loop through the small set
for link in links_test:
	page_title = link['*']
	# build the url 
	page_templates_url = "https://fr.wikipedia.org/w/api.php?action=parse&format=json&page="
	page_templates_url += page_title + "&prop=templates"
	
	# run an Http request and get the template of each page
	page_templates_json = runMediaWikiRequest(page_templates_url)
	page_templates = json.loads(page_templates_json)['parse']['templates']


    # this loop permit to selection only article   
	for template in page_templates:
		template_type = template['*']
		template_liste = list()				
		template_liste.append(template_type)

		modele_bandeau = "Modèle:Sources secondaires"
		
		if modele_bandeau in template_liste:
			fichier = open("Articles_CIV.txt", "w")
			fichier.write(page_title)
			fichier.close()
			
		elif modele_bandeau not in template_liste:
			fichier = open("Articles_CIV.txt", "w")
			fichier.write("\n Aucun articles !!!")
			fichier.close()
			
		else:
			fichier = open("Articles_CIV.txt", "w")
			fichier.write("\n Encore Aucun articles !!!")
			fichier.close()
	
# end script