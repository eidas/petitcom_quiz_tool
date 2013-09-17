#!/usr/bin/env python
#### -*- coding: utf-8 -*-
# encoding=shift_jis

#this script is for python 2.x

import sys
import codecs
import struct

class pqError(Exception):
	""" Base class for exception in this module """
	pass

class GenreNameTooLongError(pqError):
	"""Raised when the genre name is longer than 10 bytes. 

	Attribute:
		expression -- input expression in which the error occurred
	"""
	def __init__(self, expression):
		self.expression = expression
		self.message = "genre name '" + str(expression) + "' is longer than 10 bytes."
	def __str__(self):
		return repr(self.message)

class GenresTooManyError(pqError):
	"""Raised when the genres are more than 19. 

	Attribute:
		expression -- then number of genres in which the error occurred
	"""
	def __init__(self, expression):
		self.expression = expression
		self.message = str(expression) + " genres are too many. (Maximum 19 genres)"
	def __str__(self):
		return repr(self.message)

def get_genre_index(genre_list, genre):
	if genre in genre_list :
		return genre_list.index(genre)
	else:
		genre_list.append(genre)
		return len(genre_list)-1

def make_quesion_data(fin, fout, syserr, enc):
	hdata = ""  #the body of header data
	idata = ""  #the body of index data
	qdata = ""  #the body of question data
	gdata = ""  #the body of genre index data
	b = 256*5   #the haed of the question data
	genre_list = list() #the list of genre

	#make data from fin
	cnt = 0
	for line in fin:
		sl=line.split(",")
		idata += struct.pack('>H',b)  #append index address to index data

		#make question data and answer data
		for i in [1,3,5,7,9,11,13]:
			s=sl[i].encode(enc)
			qdata += struct.pack('B',len(s))
			qdata += struct.pack('<'+str(len(s))+'s',s)
			b += len(s)+1

		#make extend data (genre and the others)
		genre_index = get_genre_index(genre_list, sl[0])
		qdata += struct.pack("B",1)
		qdata += struct.pack('B',genre_index)
		cnt += 1

	#make genre data
	if len(genre_list)>=19 :
		raise GenresTooManyError, len(genre_list)
	for e in genre_list:
		ec = e.encode(enc)
		if len(ec)>10 :
			raise GenreNameTooLongError, e
		gdata += struct.pack('>10s',struct.pack('<'+str(len(ec))+'s',ec))

	#write data to file
	hdata = struct.pack('>64s',struct.pack('>H',cnt)) + struct.pack('>192s', gdata)
	fout.write(hdata)
	idata = struct.pack('>1024s',idata)
	fout.write(idata)
	fout.write(qdata)

def main():
	sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)
	enc = "shift_jis"
	fin  = codecs.open(sys.argv[1], 'r', enc)
	fout = open(sys.argv[2], 'wb')
	syserr = sys.stderr
	make_quesion_data(fin, fout, syserr, enc)

if __name__ == '__main__' :
	main()
exit()
