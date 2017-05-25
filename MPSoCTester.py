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

import os, re, argparse, yaml, signal, sys
from configparser     import ConfigParser

sys.path.append(os.path.dirname(__file__))

from modules.controller import Controller


#from modules.benchmarks import *

def command_line_handler():
	parser = argparse.ArgumentParser()
	parser.add_argument('configfile', metavar='config.yaml', \
						help='configuration file')
	parser.add_argument('simulfile', metavar='simul.txt', \
						help='simulation file')
	parser.add_argument('-li', '--lastinstall', dest='li', action='store_true', \
						help="Simulate with the last installation")
	parser.add_argument('-csi', '--clearsimulinstall', dest='csi', action='store_true', \
						help="Erase old installations and simulations")
	return parser.parse_args()





def config_parser_yaml(args):
	MPSoCBench = None
	controller = Controller()


	with open(args.configfile, 'r') as config:
				
		
		if args.li == False:
			yamls = yaml.load(config)

			comment = yamls['MPSoCTester']['comment'] + '&& SystemC : ' + yamls['systemc']['link/path'] + '&& ArchC : ' + yamls['archc']['link/path'] + '&& MPSoCBench : ' + yamls['mpsocbench']['link/path'] 

			controller.set_workspace(yamls['MPSoCTester']['workspace'])

			

			controller.set_htmloutput(yamls['MPSoCTester']['html output'], comment)

			controller.printenv()

			controller.start_systemc(yamls['systemc']['link/path'], yamls['systemc']['branch'])
			ret = controller.start_archc(yamls['archc']['link/path'], yamls['archc']['branch'])

			modellist = yamls['models']
			for _model in modellist:
				controller.models(_model, yamls['models'][_model]['link/path'])
				
			controller.export_models()
			controller.start_mpsocbench(yamls['mpsocbench']['link/path'], yamls['archc']['branch'])
			
		else:
			controller.getlastinstall()

		controller.tests(args.simulfile)

		if args.csi == True:			
			controller.clear_old_install_simul()

		#print(args.simulfile)



def main():
	args    = command_line_handler()    
	nightly = config_parser_yaml(args)
	
	 
if __name__ == '__main__':
	main()  