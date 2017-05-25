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

import subprocess
import os, re, sys
from random import randint
from modules.archc import ArchC
from modules.systemc import SystemC
from modules.mpsocbench import MPSoCBench
from .html import *
from .utils import Utils
from datetime import datetime


class Controller:
	workspace 			= ''
	htmloutput 			= ''
	indexhtml       	= "index.html"
	testshtml			= "/tests.html"
	installationshtml	= "/installations.html"
	logfolder       	= '/log/'






	def __init__(self):
		self.random     = randint(0000,9999)
		self.scriptroot = os.getcwd() + '/'

		self.html = HTML() 

		

	def set_workspace(self, workspace):
		self.workspace = self.resolve_path(workspace) 

		for d in [ self.logfolder ]:
			if not os.path.exists(self.workspace + d + "/"):
				os.makedirs(self.workspace + d + "/")


	def resolve_path(self,cmd):
		cmd = re.sub(r"\$\{RANDOM\}", str(self.random), cmd)
		cmd = re.sub(r"\$\{SCRIPTROOT\}", str(self.scriptroot), cmd)
		return cmd

		return self.workspace

	def get_workspace(self):		
		return self.workspace

	def getNamePageHTMLIndex(self):
		return self.htmloutput + self.indexhtml

	def getNamePageHTMLTests(self):
		return self.htmloutput + self.testnumber + self.testshtml

	def getNamePageHTMLInstallations(self):
		return self.htmloutput + self.testnumber + self.installationshtml


	def set_htmloutput(self, htmloutput, comment):
		

		self.htmloutput = os.path.normpath(self.resolve_path(htmloutput)) + '/'
		self.testnumber = self.compute_testnumber() 
		if not os.path.exists(self.htmloutput + self.testnumber + "/"):
			os.makedirs(self.htmloutput + self.testnumber + "/")

		self.utils = Utils(self.workspace, self.logfolder)
		

		t = comment.split('&&')
		links = ''

		for link in t[1:]:
			b = link.split(' : ')
			links = links + self.html.to_link(b[1], 2, b[0])

		comment = t[0] + '<br>' + links

		

		item = self.html.new_item(self.getNamePageHTMLTests(), self.getNamePageHTMLInstallations(), self.testnumber, str(datetime.now()), socket.gethostname(), comment)
 
		
		# Verifica se existe a pagina index onde fica cada execucao do script, caso exista cria novas paginas HTML:
		# - installations.html onde fica as instalacoes com seus respectivos logs 
		# - tests.html onde fica todos os tests passado via arquivo de configuracao e seus respectivos logs

		if os.path.isfile(self.getNamePageHTMLIndex()):
			self.html.update_pageHTML(self.getNamePageHTMLIndex(), self.html.ret_body_file(self.htmloutput + self.indexhtml, 'no'), item)
			
			self.html.pageHTML('installations', self.testnumber, self.getNamePageHTMLInstallations(), '', str(datetime.now()))

			self.html.pageHTML('tests', self.testnumber, self.getNamePageHTMLTests(), '', str(datetime.now()))

		else:

			item = self.html.new_item(self.getNamePageHTMLTests(), self.getNamePageHTMLInstallations(), self.testnumber, str(datetime.now()), socket.gethostname(), comment)
 
			self.html.pageHTML('index', '', self.getNamePageHTMLIndex(), item, str(datetime.now()))

			self.html.pageHTML('installations', self.testnumber, self.getNamePageHTMLInstallations(), '', str(datetime.now()))

			self.html.pageHTML('tests', self.testnumber, self.getNamePageHTMLTests(), '', str(datetime.now()))


			

	def compute_testnumber(self):

		directories = os.listdir(self.htmloutput)
		if "index.html" in directories:
			directories.remove("index.html")

		if len(directories) == 0:			
			return str(1)
		else:			
			return str(int(max(directories)) + 1)


	def printenv(self):
		print("Environment: ")
		print("| workspace: "+self.workspace)
		print("| scriptroot: "+self.scriptroot)
		print("| htmloutput: "+self.htmloutput)


	def getNamePageHTMLInstallSystemC(self):
		return self.htmloutput + self.testnumber + '/install_systemc.html'

	def getNamePageHTMLDownloadSystemC(self):
		return self.htmloutput + self.testnumber + '/download_systemc.html'

	



	def start_systemc(self, linkpath, branch):
		#utils = Utils(self.workspace)

		systemc = SystemC(self.workspace, self.logfolder)
		print("-- SystemC --")

		print("- Download: ", end="")
			
		ret_download = systemc.download_systemc_to_folder(linkpath, branch)		
		log = os.path.normpath(ret_download[1])
		self.html.pageHTML('log', '', self.getNamePageHTMLDownloadSystemC() , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
				
		install = 'fail'
		if ret_download[0] :
			print("OK")
			log_download = self.html.to_link(self.getNamePageHTMLDownloadSystemC(), 1, 'Donwload')

			
			print("- Install: ", end="")	
			ret_install = systemc.install_systemc()
			log = os.path.normpath(ret_install[1])
			self.html.pageHTML('log', '', self.getNamePageHTMLInstallSystemC() , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
			
			
			if ret_install[0] and (os.path.exists(self.workspace + '/systemc/install/lib-linux64') or os.path.exists(self.workspace + '/systemc/install/lib-linux32')) :
				print("OK")

				install = 'ok'

				log_install = self.html.to_link(self.getNamePageHTMLInstallSystemC(), 1, 'Install')
			else:
				print("FALIED")
				install = 'fail'
				log_install = self.html.to_link(self.getNamePageHTMLInstallSystemC(), 0, 'Install')

			
		else:
			print("FALIED")
			log_download = self.html.to_link(self.getNamePageHTMLDownloadSystemC(), 0, 'Donwload')
			

			print("- Install: FALIED")
			ret_install = systemc.install_systemc()
			log = os.path.normpath(ret_install[1])
			self.html.pageHTML('log', '', self.getNamePageHTMLInstallSystemC(), self.html.ret_body_file(log, 'yes'), str(datetime.now()))
			
			install = 'fail'
			log_install = self.html.to_link(self.getNamePageHTMLInstallSystemC(), 0, 'Install')


		if os.path.isfile(self.getNamePageHTMLInstallations()):
			update = self.html.to_line(self.html.to_col('SystemC') + self.html.to_col(linkpath) + self.html.to_col(log_download + log_install))

			self.html.update_pageHTML(self.getNamePageHTMLInstallations(), self.html.ret_body_file(self.getNamePageHTMLInstallations(), 'no'), update)
		else:
			print('Not Exist HTML Page Installations')

	
	def getNamePageHTMLInstallArchC(self):
		return self.htmloutput + self.testnumber + '/install_archc.html'

	def getNamePageHTMLDownloadArchC(self):
		return self.htmloutput + self.testnumber + '/download_archc.html'


	def start_archc(self, linkpath, branch):
		
		archc = ArchC(self.workspace, self.logfolder)

		print("-- ArchC --")
		

		print("- Download: ", end="")
		ret_download = archc.download_archc_to_folder(linkpath, branch)
		log = os.path.normpath(ret_download[1])
		self.html.pageHTML('log', '', self.getNamePageHTMLDownloadArchC() , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
		
		
		if ret_download[0] :
			print("OK")
			log_download = self.html.to_link(self.getNamePageHTMLDownloadArchC(), 1, 'Donwload')

			print("- Install: ", end="")	
			ret_install = archc.install_archc()
			log = os.path.normpath(ret_install[1])			
			self.html.pageHTML('log', '', self.getNamePageHTMLInstallArchC() , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
			
			
			if ret_install[0]:
				print("OK")
				log_install = self.html.to_link(self.getNamePageHTMLInstallArchC(), 1, 'Install')
			else:
				print("FALIED")
				log_install = self.html.to_link(self.getNamePageHTMLInstallArchC(), 0, 'Install')

			
		else:
			print("FALIED")
			log_download = self.html.to_link(self.getNamePageHTMLDownloadArchC(), 0, 'Donwload')
			

			print("- Install: FALIED")
			ret_install = archc.install_archc()
			log = os.path.normpath(ret_install[1])			
			self.html.pageHTML('log', '', self.getNamePageHTMLInstallArchC() , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
				
			log_install = self.html.to_link(self.getNamePageHTMLInstallArchC(), 0, 'Install')


		if os.path.isfile(self.htmloutput + self.testnumber + self.testshtml):
			update = self.html.to_line(self.html.to_col('ArchC') + self.html.to_col(linkpath) + self.html.to_col(log_download + log_install))
			self.html.update_pageHTML(self.getNamePageHTMLInstallations(), self.html.ret_body_file(self.getNamePageHTMLInstallations(), 'no'), update)
		else:
			print('not exists tests')


		



		#archc.install_archc()

	def models(self, name, linkpath):
		self.utils = Utils(self.workspace, self.logfolder)

		name_model = linkpath.split('/')
		print(name_model[-1])

		print("- Download: ", end="")
		ret_download = self.download_models(linkpath)
		log = os.path.normpath(ret_download[1])
		self.html.pageHTML('log', '', self.htmloutput + self.testnumber + '/download_'+ name +'.html' , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
		

		if ret_download[0]:
			print("OK")
			log_download = self.html.to_link(self.htmloutput + self.testnumber + '/download_'+ name +'.html', 1, 'Donwload')
			
			#self.utils.untar(self.workspace + '/archc/install/compilers/' + name_model[-1], self.workspace + '/archc/install/compilers')

			
			parameter = self.ret_extension(name_model[-1])

			print("- Extraction File: ", end="")


			cmd = 'cd ' + self.workspace + '/archc/install/compilers/ && tar '+ parameter + name_model[-1]
			ret_extractionfile = self.utils.exec_to_log(cmd)

			self.html.pageHTML('log', '', self.htmloutput + self.testnumber + '/extraction_file_'+ name +'.html' , self.html.ret_body_file(os.path.normpath(ret_extractionfile[1]), 'yes'), str(datetime.now()))
			
			if ret_extractionfile[0]:
				print("OK")
				log_extractionfile = self.html.to_link(self.htmloutput + self.testnumber + '/extraction_file_'+ name +'.html', 1, 'Extraction')
			else:
				print("FALIED")
				log_extractionfile = self.html.to_link(self.htmloutput + self.testnumber + '/extraction_file_'+ name +'.html', 0, 'Extraction')


			cmd = 'rm ' + self.workspace + '/archc/install/compilers/' + name_model[-1]
			self.utils.exec_to_log(cmd)

		else:
			print("FALIED")
			log_download = self.html.to_link(self.htmloutput + self.testnumber + '/download_'+ name +'.html', 0, 'Donwload')
			log_extractionfile = self.html.to_link('#', 0, 'Extraction')


		if os.path.isfile(self.htmloutput + self.testnumber + self.testshtml):
			update = self.html.to_line(self.html.to_col(name + " Compiler") + self.html.to_col(linkpath) + self.html.to_col(log_download + log_extractionfile))
			self.html.update_pageHTML(self.getNamePageHTMLInstallations(), self.html.ret_body_file(self.getNamePageHTMLInstallations(), 'no'), update)
		else:
			print('not exists tests')



	def ret_extension(self, namefile):
		extension = namefile.split('.')

		if extension[-1] == 'tar':
			return '-xvf '

		elif extension[-2] == 'tar' and extension[-1] == 'bz2':
			return '-jxvf '

		elif extension[-2] == 'tar' and extension[-1] == 'gz':
			return '-vzxf '


	def download_models(self, linkpath):

		self.utils = Utils(self.workspace, self.logfolder)

		if linkpath.startswith('git') or linkpath.startswith('http') and linkpath.endswith('.git'): 
			cmd = 'git clone -b ' + branch + ' ' + linkpath + ' ' + self.workspace + '/mpsocbench/'
		elif linkpath.startswith('http'):
			cmd = 'wget' + ' --directory-prefix=' + self.workspace + '/archc/install/compilers ' + linkpath 
		
		return self.utils.exec_to_log(cmd)

	def export_models(self):
		models = os.listdir(self.workspace + '/archc/install/compilers/')

		

		arq = open(os.path.expanduser('~/.profile'), 'r')
		texto_anterior = arq.readlines()
		arq.close()

		arq = open(os.path.expanduser('~/.profile'), 'w')
		texto = []

		for _model in models:		 	
		 	texto.append('export PATH='+ self.workspace + '/archc/install/compilers/' + _model + '/bin:$PATH\n')
		 	cmd = 'export PATH='+ self.workspace + '/archc/install/compilers/' + _model + '/bin:$PATH'
		 	self.utils.exec_to_log(cmd)

		arq.writelines(texto_anterior)
		arq.writelines(texto)
		arq.close() 


	def getNamePageHTMLInstallMPSocBech(self):
		return self.htmloutput + self.testnumber + '/install_mpsocbench.html'

	def getNamePageHTMLDownloadMPSocBech(self):
		return self.htmloutput + self.testnumber + '/download_mpsocbench.html'



	def start_mpsocbench(self, linkpath, branch):
		
		mpsocbench = MPSoCBench(self.workspace, self.logfolder)
		self.utils = Utils(self.workspace, self.logfolder)


		print("-- MPSoCBench --")
		

		print("- Download: ", end="")
		ret_download = mpsocbench.download_mpsocbench_to_folder(linkpath, branch)
		log = os.path.normpath(ret_download[1])
		self.html.pageHTML('log', '', self.getNamePageHTMLDownloadMPSocBech() , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
		
		if ret_download[0] :
			print("OK")
			log_download = self.html.to_link(self.getNamePageHTMLDownloadMPSocBech(), 1, 'Donwload')

			print("- Install: ", end="")				
			cmd = 'cd ' + self.workspace + '/mpsocbench/ && sh setup.sh ' + self.workspace + '/archc/install/ && source env.sh && bash -l'
			ret_install = self.utils.exec_to_log(cmd)
			log = os.path.normpath(ret_install[1])
			self.html.pageHTML('log', '', self.getNamePageHTMLInstallMPSocBech() , self.html.ret_body_file(log, 'yes'), str(datetime.now()))
			

			if ret_install[0]:
				print("OK")
				log_install = self.html.to_link(self.getNamePageHTMLInstallMPSocBech(), 1, 'Install')

				arq = open('log/lastinstall.txt', 'w')
				arq.write(self.workspace ) 
				arq.write("\n") 
				arq.write(self.htmloutput + self.testnumber)
				arq.close()

			else:
				print("FALIED")
				log_install = self.html.to_link(self.getNamePageHTMLInstallMPSocBech(), 0, 'Install')			

		else:
			print("FALIED")
			log_download = self.html.to_link(self.getNamePageHTMLDownloadMPSocBech(), 0, 'Donwload')

			print("- Install: FALIED")
			log_install = self.html.to_link('#', 0, 'Install')	




		if os.path.isfile(self.getNamePageHTMLInstallations()):
			update = self.html.to_line(self.html.to_col('MPSoCBench') + self.html.to_col(linkpath) + self.html.to_col(log_download + log_install))
			self.html.update_pageHTML(self.getNamePageHTMLInstallations(), self.html.ret_body_file(self.getNamePageHTMLInstallations(), 'no'), update)
		else:
			print('not exists tests')
		




	def getlastinstall(self):

		#possivel erro ao usuario mudar o local do htmloutput
		arq = open('log/lastinstall.txt', 'r')
		dados = arq.read().splitlines() 
		arq.close()

		if not dados:
			print('***There is no last installation***')
			sys.exit()
		else:
			self.workspace = dados[0]
			self.htmloutput = dados[1]
			self.testnumber = ''

			print(self.workspace)
			print(self.htmloutput)


	def tests(self, simulfile):
		self.utils = Utils(self.workspace, self.logfolder)

		arq = open(simulfile, 'r')
		texto = arq.readlines()
		arq.close()

		# remove plataformas ja existentes
		self.utils.rm(self.workspace + '/mpsocbench/rundir')
		cmd = 'cd ' + self.workspace + '/mpsocbench/ && mkdir rundir'
		self.utils.exec_to_log(cmd)

		cont = 0

		for linha in texto:

			if linha[0] == '[':
				parametros = linha.strip('[').strip('\n').strip(' ').strip(']').split(',')

				if len(parametros) > 1:	
					comando = parametros[0]	
					string = ''
					
					for a in parametros[1:]:

						p = a.split('=')
						
						s = p[1].split(':')
						for t in s:
							v = p[0].strip(' ')
							string = comando.replace('%'+v+'%', t)
							cont = cont +1 
							
							namePagePlatformHTML = self.platformName(string)
							print(cont, namePagePlatformHTML)

							ret_test = self.utils.exec_to_log(self.getCommandSimul(string))

							log = os.path.normpath(ret_test[1])

							bodyFile = self.html.ret_body_file(log, 'yes')



							self.html.pageHTML('log', '', self.htmloutput + self.testnumber + '/'+ namePagePlatformHTML +'.html', bodyFile, str(datetime.now()))
							
							if self.verifyTestPassed(bodyFile):
								print("OK")
								log_test = self.html.to_link(self.htmloutput + self.testnumber + '/'+ namePagePlatformHTML +'.html', 1, 'See details')

							else:
								print("FALIED")
								log_test = self.html.to_link(self.htmloutput + self.testnumber + '/'+ namePagePlatformHTML +'.html', 0, 'See details')

							if os.path.isfile(self.getNamePageHTMLTests()):
								update = self.html.to_line(self.html.to_col(str(cont)) + self.html.to_col(namePagePlatformHTML) + self.html.to_col('./MPSoCBench ' + string) + self.html.to_col(log_test))
								self.html.update_pageHTML(self.getNamePageHTMLTests(), self.html.ret_body_file(self.getNamePageHTMLTests(), 'no'), update)
							else:
								print('not exists tests')


						
				else:
					cont = cont +1 

					namePagePlatformHTML = self.platformName(parametros[0])
					print(cont, namePagePlatformHTML)				

					
					ret_test = self.utils.exec_to_log(self.getCommandSimul(parametros[0]))

					log = os.path.normpath(ret_test[1])

					bodyFile = self.html.ret_body_file(log, 'yes')

					self.html.pageHTML('log', '', self.htmloutput + self.testnumber + '/'+ namePagePlatformHTML +'.html', bodyFile, str(datetime.now()))
							
					if self.verifyTestPassed(bodyFile):
						print("OK")
						log_test = self.html.to_link(self.htmloutput + self.testnumber + '/'+ namePagePlatformHTML +'.html', 1, 'See details')

					else:
						print("FALIED")
						log_test = self.html.to_link(self.htmloutput + self.testnumber + '/'+ namePagePlatformHTML +'.html', 0, 'See details')

					if os.path.isfile(self.getNamePageHTMLTests()):
						update = self.html.to_line(self.html.to_col(str(cont)) + self.html.to_col(namePagePlatformHTML) + self.html.to_col('./MPSoCBench ' + parametros[0]) + self.html.to_col(log_test))
						self.html.update_pageHTML(self.getNamePageHTMLTests(), self.html.ret_body_file(self.getNamePageHTMLTests(), 'no'), update)
					else:
						print('not exists tests')
				
		#print(cont)

	def verifyTestPassed(self, bodyFile):

		linesBodyFile = bodyFile.split('<br>')

		for line in linesBodyFile:			
			line = line.strip()
			if line == ' Test Passed.' or line == 'Test Passed.':
				print(line)
				return True

		return False


	def getCommandSimul(self, string):

		cmd = 'cd ' + self.workspace + '/mpsocbench/ ; ' 
		cmd += 'export PATH='+ self.workspace + '/archc/install/compilers/mips-newlib-elf/bin:$PATH ; '
		cmd += 'export PATH='+ self.workspace + '/archc/install/compilers/sparc-newlib-elf/bin:$PATH ; '
		cmd += 'export PATH='+ self.workspace + '/archc/install/compilers/powerpc-newlib-elf/bin:$PATH ; '
		cmd += 'export PATH='+ self.workspace + '/archc/install/compilers/arm-newlib-eabi/bin:$PATH ; '
		cmd += 'source env.sh ; '
		cmd += './MPSoCBench ' + string 

		return cmd
		


	def platformName(self, string):
		u = string.split(' ')

		p = ''
		i = ''
		pw = ''		
		n = ''		
		s = ''

		
		for t in u:
			y = t.split('=')
			c = y[0].strip('-')

			if c == 'p':
				p = y[-1]

			elif c == 'i':
				i = y[-1]

			elif c == 'pw':
				pw = 'pw'

			elif c == 'n':
				n = y[-1]

			elif c == 's':
				s = y[-1]

			

		if pw == '':
			namePlatform = p + '.' + i + '.' + n + '.' + s

		else:
			namePlatform = p + '.' + i + '.' + pw + '.' + n + '.' + s


		return namePlatform


	def clear_old_install_simul(self):	
		self.utils = Utils(self.workspace, self.logfolder)	

		absoluteDirectory = self.workspace.split('/')
		lastDirectory = absoluteDirectory.pop(-1)
		lastDirectory = lastDirectory

		absoluteDirectory = '/'.join(absoluteDirectory)
		absoluteDirectory = absoluteDirectory + '/'

		directories = os.listdir(absoluteDirectory)

		print(directories)

		for directory in directories:
			if directory != lastDirectory:
				cmd = 'cd ' + absoluteDirectory + ' && chmod -R 777 ' + directory  + ' && rm -rf ' + directory 
				self.utils.exec_to_log(cmd)

		
		


		


		


	



	