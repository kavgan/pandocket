#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pandoc-webpage.py
# TODO: Preserve span formatting from original webpage
# TODO: Remove img tags with BeautifulSoup
# TODO: Make error handling easier to understand

import urllib2
import pandoc
from bs4 import BeautifulSoup

# Open the input file and empty the output file
input = open("sources.txt", "r").read().splitlines()
open("pandocket-output.md","w").close()

for line in input:
 
 	if line.startswith("http"):

		# Get information from line about website to be parsed
		# Help provided by http://stackoverflow.com/questions/13537829/
		vars = line.split(' | ')
		url, args = line.split (' | ', 1)
		args = args.split(' >')
		name = args[0]
		params = dict([param.strip().split('=') for param in args[1:]])

		# Open specified URL and use BeautifulSoup to get specified section
		html = urllib2.urlopen(url).read()
	 	soup = BeautifulSoup(html)
 		html_section = str(soup.find(name, **params))
		doc = pandoc.Document()
		doc.html = html_section
		html_md = doc.markdown

 		# Write to output file, getting rid of any literal linebreaks
 		f = open('pandocket-output.md','a').write(html_md.replace("\\\n","\n"))

	elif len(line) == 0:

		# Convert blank lines in input file to newlines in output file
		f = open('pandocket-output.md','a').write("\n")

	else:

		# Pass regular lines from input file to output file
		f = open('pandocket-output.md','a').write(line + "\n")	

# Call on pandoc to convert fulltext to markdown and write to file
# Using yoavram fork of pyandoc

fulldoc = pandoc.Document()
fulldoc.add_argument("standalone")
fulldoc.add_argument("toc")
fulldoc.markdown = open('pandocket-output.md','r').read()
fulldoc.to_file('pandocket-output.pdf')
fulldoc.to_file('pandocket-output.epub')
