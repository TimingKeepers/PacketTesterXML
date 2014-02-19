#! /usr/bin/python

# ****************************************************************************** 
#  @file PTXML_client.py
#  @brief Example using PTXMLServer
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
	if len(sys.argv) != 2:
		print "Usage: PTXML_server.py <XML server configuration file>"
		sys.exit(-1)

	file_xml = sys.argv[1]

	server = PacketTesterXML.PTXMLServer(file_xml)
	server.run(1)


