#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Description: Lister tous les articles wikipedia  de CIV qui manquent de sources secondaires
# Auteurs: Samuel Guebo & Paul Bouaffou
# Licence:

         

import json
import requests

def logText(filename, text):
	""" Utility for writing in a text file """
	with open(filename, "a") as f:
		f.write(text + "\n")

def printNotice(notice):
    ''' Print notice message in yellow '''

    print('\033[93m' + notice + '\033[0m')

def runMediaWikiRequest(url):
	""" function to give resultat of url request """
	resultatJson = requests.get(url).content
	# return the json text
	return resultatJson
	

def app():
	""" Main entry point for the tool. It gets all articles from CIV archives """
	civ_archives_url = "https://fr.wikipedia.org/w/api.php?action=parse&format=json&page=Projet:C%C3%B4te_d%27Ivoire/Articles_r%C3%A9cents/Archive&prop=links" 
	archives_json = runMediaWikiRequest(civ_archives_url)

	# convert from plain text to python array, and browse to get items 'parse' and its child 'links'
	archives_links = json.loads(archives_json)['parse']['links']  

	# just the two first items of the array
	links_test = archives_links[0:500]

	# initiate counter
	articles_count = 0
	# loop through the small set
	for link in links_test:
		page_title = link['*']
		# build the url 
		page_templates_url = "https://fr.wikipedia.org/w/api.php?action=parse&format=json&page="
		page_templates_url += page_title + "&prop=templates"
		
		# run an Http request and get the template of each page
		page_templates_json = runMediaWikiRequest(page_templates_url)
		page_templates = json.loads(page_templates_json)['parse']['templates']

		
		# Make sure the list is not empty
		if(len(page_templates) > 0):
			# Define which templates are considered problematic
			modele_bandeau = [
				"Modèle:Sources secondaires",
				"Modèle:Ébauche",
				"Modèle:Sources",
				"Modèle:Méta bandeau d'avertissement",
			]
			
			for template in page_templates:
				if template["*"] in modele_bandeau:
					logText("articles_civ.txt", page_title)
					articles_count += 1
					print(page_title + " has some issues.")
	# Print total
	printNotice("In total, " + str(articles_count) + " articles have issues.")
	if (articles_count > 0):
		printNotice("Checkout the logs for more details.")
# Triggering the application
app()