 # @file      MPSoCTester.py
 # @author    Thiago Rodrigues de Oliveira
 #            troliveiraa@gmail.com

 #            Faculdade de Computação 
 #            FACOM-UFMS
 #            http://www.facom.ufms.br/

 # @version   1.0
 # @date      Thu, 4 May 2017 
 
 
 # This program is free software; you can redistribute it and/or modify 
 # it under the terms of the GNU General Public License as published by 
 # the Free Software Foundation; either version 2 of the License, or 
 # (at your option) any later version. 
 
 # This program is distributed in the hope that it will be useful, 
 # but WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 # GNU General Public License for more details. 
 
 # You should have received a copy of the GNU General Public License 
 # along with this program; if not, write to the Free Software 
 # Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

#!/usr/bin/env python3
import os, re, shutil
import sys, re, os, string
import socket
from datetime import datetime

class HTML:

	arquivo = ''
	caminho = ''

	def __init__(self):

		self.arquivo = ''

		
	def pageHTML(self, type_page, titulo, caminho, corpo, date):

		if type_page == "index":

			page = '<!DOCTYPE html><html lang="pt-BR"><head> \
						<meta charset="utf-8"> \
						<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> \
						<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous"> \
						<title>MPSoC Tester</title> \
					</head> \
					<body> \
						<nav class="navbar navbar-inverse bg-inverse text-center"> \
							<a class="navbar-brand" href="#"> \
								MPSoC tester <span class="badge badge-info">v1.0</span> \
							</a> \
						</nav> \
						<div style="margin-top: 20px;"></div> \
						<div class="container"> \
							<div class="list-group"> \
								<div class="ini"></div> \
								'+ corpo +' \
							</div> \
							<footer style="margin-top:20px;"> \
								<p>&copy; 2017 MPSoCBench. &middot; \
									<a href="http://www.archc.org/benchs/mpsocbench/" class="btn-link text-gray-dark">Site</a> &middot; \
									<a  href="http://www.archc.org/" class="btn-link text-gray-dark" href="#">ArchC</a> \
								</p> \
							</footer> \
						</div> \
					</body> \
				</html>'

		elif type_page == "tests":

			page = '<!DOCTYPE html> \
					<html lang="pt-BR"> \
						<head> \
							<meta charset="utf-8">\
							<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> \
							<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous"> \
							<title>MPSoC Tester</title> \
						</head> \
						<body> \
							<nav class="navbar navbar-inverse bg-inverse text-center">\
								<a class="navbar-brand" href="#">\
									MPSoC tester <span class="badge badge-info">v1.0</span>  #'+ titulo +'	\
								</a>\
							</nav>\
							<div style="margin-top: 20px;"></div> \
							<div class="container"> \
								<a class="btn btn-outline-info btn-sm" href="../index.html">Página Inicial</a> \
								<a class="btn btn-outline-secondary btn-sm" href="tests.html">Tests</a> \
								<div style="margin-top: 20px;"></div> \
								<table class="table"> \
									<thead> \
										<tr> \
											<th>N°</th> \
											<th>Platform name</th> \
											<th>Command</th> \
											<th>Log</th> \
										</tr> \
									</thead> \
									<tbody> \
										<div class="ini"></div> \
										'+ corpo +'</tbody> \
								</table> \
								<footer style="margin-top:20px;">\
									<p>&copy; 2017 MPSoCBench. &middot; \
										<a href="http://www.archc.org/benchs/mpsocbench/" class="btn-link text-gray-dark">Site</a> &middot; \
										<a  href="http://www.archc.org/" class="btn-link text-gray-dark" href="#">ArchC</a> \
									</p>\
								</footer> \
							</div> \
						</body> \
					</html>'

		elif type_page == "installations":

			page = '<!DOCTYPE html> \
					<html lang="pt-BR"> \
						<head> \
							<meta charset="utf-8">\
							<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> \
							<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous"> \
							<title>MPSoC Tester</title> \
						</head> \
						<body> \
							<nav class="navbar navbar-inverse bg-inverse text-center">\
								<a class="navbar-brand" href="#">\
									MPSoC tester <span class="badge badge-info">v1.0</span>  #'+ titulo +'	\
								</a>\
							</nav>\
							<div style="margin-top: 20px;"></div> \
							<div class="container"> \
								<a class="btn btn-outline-info btn-sm" href="../index.html">Página Inicial</a> \
								<a class="btn btn-outline-secondary btn-sm" href="#">Installations</a> \
								<div style="margin-top: 20px;"></div> \
								<table class="table"> \
									<thead> \
										<tr> \
											<th>Component</th> \
											<th>Link/Path</th> \
											<th>Status</th> \
										</tr> \
									</thead> \
									<tbody> \
										<div class="ini"></div> \
										'+ corpo +'</tbody> \
								</table> \
								<footer style="margin-top:20px;">\
									<p>&copy; 2017 MPSoCBench. &middot; \
										<a href="http://www.archc.org/benchs/mpsocbench/" class="btn-link text-gray-dark">Site</a> &middot; \
										<a  href="http://www.archc.org/" class="btn-link text-gray-dark" href="#">ArchC</a> \
									</p>\
								</footer> \
							</div> \
						</body> \
					</html>'


		elif type_page == "log":

			page = '<!DOCTYPE html> \
					<html lang="pt-BR"> \
						<head> \
							<meta charset="utf-8">\
							<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> \
							<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous"> \
							<title>MPSoC Tester</title> \
						</head> \
						<body> \
							<nav class="navbar navbar-inverse bg-inverse text-center">\
								<a class="navbar-brand" href="#">\
									MPSoC tester <span class="badge badge-info">v1.0</span>	\
								</a>\
							</nav>\
							<div style="margin-top: 20px;"></div> \
							<div class="container"> \
								<a class="btn btn-outline-info btn-sm" href="../index.html">Página Inicial</a> \
								<a class="btn btn-outline-info btn-sm" href="tests.html">Tests</a> \
								<a class="btn btn-outline-secondary btn-sm" href="#" disabled>Log</a> \
								<div style="margin-top: 20px;"></div> \
								<p>Produced by MPSoCBench tester @ '+ date +'</p> \
								<div style="margin-top: 20px;"></div> \
								<code> \
									'+ corpo +' \
								</code> \
								<footer style="margin-top:20px;">\
									<p>&copy; 2017 MPSoCBench. &middot; \
										<a href="http://www.archc.org/benchs/mpsocbench/" class="btn-link text-gray-dark">Site</a> &middot; \
										<a  href="http://www.archc.org/" class="btn-link text-gray-dark" href="#">ArchC</a> \
									</p>\
								</footer> \
							</div> \
						</body> \
					</html> '

		#''.join(page.split(' \ '))	

		self.create_pageHTML(caminho, page)


	def create_pageHTML(self, caminho, page):
		arq = open(caminho, 'w')
		arq.writelines(page)
		arq.close()

	def to_link(self, href, success, corpo):
		if success == 1:

			link = '<a class="badge badge-success" href="'+ href +'" style="margin: 2px"> '+corpo+' </a>'
			return link

		elif success == 2:

			link = '<a class="badge badge-success" href="'+ href +'" target="_blank" style="margin: 2px"> '+corpo+' </a>'
			return link

		else:

			link = '<a class="badge badge-danger" href="'+ href +'" style="margin: 2px"}> '+corpo+' </a>'
			return link

	def to_col(self, corpo):
		col = '<td> ' + corpo + '</td>'
		return col

	def to_line(self, corpo):
		line = '<tr scope="row"> ' + corpo + '</tr>'

		return line

	def new_item(self, link_page_log, link_page_install, n, now, by, comment):


		item = '<div class="row">\
          			<div class="list-group-item list-group-item-action list-group-item  align-items-start">\
          				<div class="col-8">\
		              		<div class="d-flex w-100">\
		                		<h5 class="mb-1" style="margin-right: 20px;">#'+ n +'</h5>\
		                		<small>'+ now +'</small>\
		              		</div>\
		              		<p class="mb-1">by: '+ by +'</p>\
		              		<small>Comment: '+comment +'</small>\
		            	</div>\
		            	<div class="col-4 text-right">\
		              		<div style="margin-top: 5%;">\
		                		<a class="btn btn-outline-primary" href="'+ link_page_log +'">Tests</a>\
		                		<a class="btn btn-outline-primary" href="'+ link_page_install +'">Installations</a>\
		              		</div>\
		            	</div>\
		          	</div>\
		      	</div>'

		return item

	def update_pageHTML(self, link_arq, corpo, update):
		update = '<div class="ini"></div>' + update

		page = update.join(corpo.split('<div class="ini"></div>'))
		#print(page)
		self.create_pageHTML(link_arq, page)

	def ret_body_file(self, link_arq, log):

		if log == 'yes':

			conteudo = ''
			ref_arquivo = open(link_arq, "r")
			for linha in ref_arquivo:
				conteudo = conteudo + linha + ' <br> '
			ref_arquivo.close()
			#conteudo = ref_arquivo.read()
			return conteudo
		else:
			ref_arquivo = open(link_arq, "r")
			conteudo = ref_arquivo.read()
			ref_arquivo.close()
			return conteudo