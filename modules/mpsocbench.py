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
 
from .utils import Utils
import os


class MPSoCBench:
	mpsocbench         = {}
	external_libs = []

	def __init__(self, workspace, logfolder):
		self.mpsocbench = {}
		self.mpsocbench['src']       = "/mpsocbench/src"
		self.mpsocbench['prefix']    = "/mpsocbench/install"
		self.workspace = workspace
		self.logfolder = logfolder

		self.utils = Utils(self.workspace, self.logfolder)

	def get_mpsocbench_src(self):
		return self.workspace + self.mpsocbench['src']

	def download_mpsocbench_to_folder(self, linkpath, branch):

		

		if linkpath.startswith('git') or linkpath.startswith('http') and linkpath.endswith('.git'): 
			cmd = 'git clone -b ' + branch + ' ' + linkpath + ' ' + self.workspace + '/mpsocbench/'
		elif linkpath.startswith('http'):
			cmd = 'wget ' + linkpath + ' --directory-prefix=' + self.workspace + self.mpsocbench['src']

		
		return self.utils.exec_to_log(cmd)
		
	def install_mpsocbench(self):
		cmd = 'cd ' + self.workspace + self.mpsocbench['src'] + ' && ./autogen.sh && ./configure --prefix='+ self.workspace  + self.mpsocbench['prefix']  + ' && make && make install'
		
		return self.utils.exec_to_log(cmd)
		

