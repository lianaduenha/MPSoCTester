MPSoCTester
============

MPSoCTester is a script for automated tests of the MPSoCBench tools and platforms, which involves the download of the tools of their official repositories, configuring, installing and simulating a significant set of MPSoCS. 

License
-------
 - ArchC tools are provided under the GNU GPL license.
   See [License](LICENSE) file for details on this license.

Required
--------
 - Linux Ubuntu 14.04 or 16.04
 - Python 3.5 (or higher)  
 - Library PyYAML 3.12 
 - Git 2.7 (or higher) 
 - GCC 


Initial Setup
-------------

To download and install all tools and to perform the pre-determined set of simulations:

python3 MPSoCTester.py conf/site.yaml conf/simul.txt


To perform the predetermined set of simulations using the software infrastructure installed previously.

python3 MPSoCTester.py conf/site.yaml conf/simul.txt -li




More
----

Remember that ArchC models, SystemC library and MPSoCBench components must be compiled with
the same GCC version, otherwise you will get compilation problems.

You can find language overview, models, and documentation at
http://www.archc.org


The ArchC Team
Computer Systems Laboratory (LSC)
IC-UNICAMP
http://www.lsc.ic.unicamp.br


# MPSoCTester
