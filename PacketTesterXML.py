#! /usr/bin/python

# ****************************************************************************** 
#  @file PacketTesterXML.py
#  @brief PacketTesterXML Classes
#
#  Copyright (C) 2014
#
#  PTXMLClient: Packet Tester Client with Python
#  PTXMLServer: Packet Tester Server with Python
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

import socket 
import sys
import time
import random
import xml.etree.ElementTree as ET

class PTXMLClient:
	
	def __init__(self,file_xml="test.xml"):
		self.file_xml = file_xml

	def run(self,verbose=0):
		tree = ET.parse(self.file_xml)
		root = tree.getroot()

		test_attr = root.get("iters")

		if test_attr != None:
			test_iter = int(test_attr)
		else:
			test_iter = 1

		for itest in range(test_iter):

			if verbose == 1:
				print "\n"
				print "Iter",itest+1,"of",test_iter
				print "----------------------------------------"
				print "\n"

			msgs = root.findall("message")

			for msg in msgs:	
				msg_header = msg.find("header")
				msg_content = msg.find("content")
				msg_text = msg_content.text
				msg_proto = msg_header.find("proto").text
				msg_times = msg_header.find("times")
				msg_sleep = msg_header.find("sleep")
				msg_ip = msg_header.find("ip").text
				msg_port = msg_header.find("port").text
	
				if(msg_times == None):
					times = 1
				else:
					times = int(msg_times.text)

				if(msg_sleep == None):
					sleep_enable = False
				else:
					sleep_enable = True
					sleep_attr = msg_sleep.get("random")

					if(sleep_attr != None):
						is_random_sleep = (sleep_attr == "yes")
						if is_random_sleep:
							sleep_range = (msg_sleep.text).split(',')
							sleep_range_min = float(sleep_range[0])
							sleep_range_max = float(sleep_range[1])
						else:
							sleep_gap = float(msg_sleep.text)
					else:
						is_random_sleep = False
						sleep_gap = float(msg_sleep.text)

				npackets = 0

				if (msg_proto.upper() == "TCP"):			

					for i in range(times):	
						sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 		
						sock.connect((msg_ip,int(msg_port)))
						sock.send(msg_text)
						npackets = npackets+1

						if verbose == 1:
							print "(",npackets,"/",times,")","To",msg_ip,":",msg_port,"-",msg_proto,"->",msg_text
						
						sock.close()

						if sleep_enable:
							if is_random_sleep:
								sleep_gap = random.uniform(sleep_range_min,sleep_range_max)

							if verbose == 1:
								print "( Waiting for",sleep_gap,"seconds )"
	
							if sleep_gap != 0:
								time.sleep(sleep_gap)

				else:				
					sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
	
					for i in range(times):
						sock.sendto(msg_text, (msg_ip, int(msg_port)))
						npackets = npackets+1
						
						if verbose == 1:
							print "(",npackets,"/",times,")","To",msg_ip,":",msg_port,"-",msg_proto,"->",msg_text

						if sleep_enable:
							if is_random_sleep:
								sleep_gap = random.uniform(sleep_range_min,sleep_range_max)

							if verbose == 1:
								print "( Waiting for",sleep_gap,"seconds )"

							if sleep_gap != 0:
								time.sleep(sleep_gap)

					sock.close()

class PTXMLServer:
	
	def __init__(self,file_xml="server.xml"):
		self.file_xml = file_xml

	def run(self,verbose=0,maxbuf=1024,maxcon=100):
		tree = ET.parse(self.file_xml)
		root = tree.getroot()

		server_port = int(root.find("port").text)
		server_proto = root.find("proto").text

		bufsize = maxbuf
		max_connections = maxcon
		npackets = 0

		if(server_proto.upper() == "TCP"):
			server_protocol = socket.SOCK_STREAM
		else:
			server_protocol = socket.SOCK_DGRAM
 
		sock = socket.socket(socket.AF_INET,
                      server_protocol)

		sock.bind(('', server_port))

		if(server_proto.upper() == "TCP"):
			sock.listen(max_connections)

		if verbose == 1:
			print "............. Server ............."
			print "Port:", server_port
			print "Protocol:",server_proto
			print ".......... Listening ............."

		listening = True

		if server_proto.upper() == "TCP":
			while listening:
				conn, addr = sock.accept()
				data = conn.recv(bufsize)
				npackets=npackets+1
				
				if verbose == 1:
					print npackets,"-> received message:", data

				conn.close()
		else:
			while listening:
				data, addr = sock.recvfrom(bufsize)
				npackets=npackets+1
				
				if verbose == 1:
					print npackets,"-> received message:", data

		sock.close()

