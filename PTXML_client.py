#! /usr/bin/python

# ****************************************************************************** 
#  @file PTXML_client.py
#  @brief Example using PTXMLClient
#
#  Copyright (C) 2014
#
#  @author Miguel Jimenez Lopez <klyone@ugr.es>
#
# ******************************************************************************
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#  
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library. If not, see <http//www.gnu.org/licenses/>.
# ******************************************************************************

import sys
import PacketTesterXML

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: PTXML_client.py <XML test file> ... <XML test file>"
		sys.exit(-1)

	nfiles = len(sys.argv)-1

	for ifile in range(nfiles):

		file_xml = sys.argv[ifile+1]

		client = PacketTesterXML.PTXMLClient(file_xml)

		print "\n"
		print "Test",ifile+1,"of",nfiles,"->",file_xml
	
		print "==============================================="
	
		client.run(1)

