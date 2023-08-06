#! /usr/bin/python3
'''
qucs-netlist.py License: GPL-3+ Chris Rogers 31st March 2020
Use .sch file for components as details are separate and .sim file 
for nets as only that file contains them.
Version 0.0.5
'''

#-------------------------------------------------------------------------------
def appendpin(net, pin):
	global netlist
	
	foundnet = False
	for sublist in netlist:
		if sublist[0] == net:
			foundnet = True
	if not foundnet: # net not found, so add a new row for it
		netlist.append ([net])
	
	# look for net, find it and add pin
	for sublist in netlist:
		if sublist[0] == net:
			sublist.append(pin)
			break

#-------------------------------------------------------------------------------
def parsesch():
	global validparts
	
	#fields count 0 onwards
	if line[2] == '1': #component is active
			
		pfield9 = '' ; pfield11 = '' ; pfield13 = ''
		if len(line) > 9:
			pfield9 = line[9]
	
			if len(line) > 11:
				pfield11 = line[11]

				if len(line) > 13:
					pfield13 = line[13]

		pqucs = line[0]; pname = line[1]; pactive = line[2]
		if pqucs == 'Lib':
				pqucs = pfield9; pdetailA = pfield11 ; pdetailB = ''
		else:
				pqucs = line[0]; pdetailA = pfield9 ; pdetailB = pfield13 
	
		pdetail = '' ; foundpart = False

		for sublist in partlist:		
			if sublist[0] == pqucs:
				if sublist[1] == ''	or (sublist[1] == '9' and sublist[2] == pdetailA):
					foundpart = True
					validparts.append(pname)
					return('[\n'+pname+'\n'+sublist[3]+'\n'+pdetailA+'\n\n\n]\n')

				elif (sublist[1] == '13' and sublist[2] == pdetailB):
					foundpart = True
					validparts.append(pname)
					return('[\n'+pname+'\n'+sublist[3]+'\n'+pdetailB+'\n\n\n]\n')

		if not foundpart:
			print('Warning: Unknown component type not converted: '+pname + ' ' + pqucs)	 
			return(None)

#-------------------------------------------------------------------------------
def parsesim():
	# inactive components don't get into sim file
	pname = line[1]; pqucs = line[0]
	fieldtotal = len(line)
	
	if pname in validparts:
		validnet = []
		for fno in range (2,fieldtotal): # skip the first 2 irrelevant fields
			# find all the pins in the line
			if '=' not in line[fno]:
				if line[fno] not in validnet: # to avoid transistors with 4 pins
					validnet.append(line[fno])
					pin = line[1]+'-'+str(fno-1) #take 1 from fno because 0 and 1 have other data
					appendpin(line[fno], pin)	# add pin connection to net

#=start=========================================================================
import os, sys, shlex, webbrowser 
from importlib import resources # for filepaths

netlist = []
namebrowser = 'qucs-netlist.html'
namehelp = 'qucs-netlist.hlp'
nameparts = 'qucs-netlist.dat'

print(); print('For more details, a list of parts or example files, see https://github.com/PopoutApps/qucs-netlist'); print()

# link to package filenames. No checks on these files as should have been installed.
namehelp_traversable = resources.files(__package__) / namehelp
nameparts_traversable = resources.files(__package__) / nameparts

if len(sys.argv) < 2:
	print()
	with resources.as_file(namehelp_traversable) as filehelp:
		with open(filehelp) as f:
	 		print(f.read())
	print()
	sys.exit(0)
else:
	filesch	= sys.argv[1];	filename = filesch.split('.'); filename = filename[0]
	filesim = filename + '.sim'
	filenet = filename + '.net'

#-------------------------------------------------------------------------------
# load partlist-----------------------------------------------------------------
partlist = []

with resources.as_file(nameparts_traversable) as fileparts:
	with open(fileparts, 'r') as fpl:
		try: 
			line = fpl.readline()
			if line[:14] == '<Qucs Partlist':
				line = ''; lineno = 0
				while line != [] and lineno < 100: 
					lineno += 1
					line = fpl.readline() 
					line = shlex.split(line)
					if line != []:
						partlist.append(line)
			else:
				sys.exit('Error: Not a valid parts list file.')
		except:
			sys.exit('Error: Parts list file is empty.')

# check that input file exists--------------------------------------------------
if os.path.isfile(filesch):
	with open(filesch, 'r') as fin:
		try:
			line = fin.readline()
			if line[:15] != '<Qucs Schematic':
				sys.exit('Error: Input file is not a Qucs file.')
		except:
			sys.exit('Error: Qucs input file is invalid.')
else:
	sys.exit('Error: Qucs input file does not exist.')

# check overwriting of output file----------------------------------------------
'''
overwrite = 'N'
if len(sys.argv) == 3:
	overwrite = sys.argv[2]
	if overwrite in ('y','Y'):
			overwrite = 'Y'
	#if (os.path.isfile(filesch) or os.path.isfile(filesim)) and not overwrite == 'Y': #~~~ Why check the sch and sim?
	if os.path.isfile(filenet) and not overwrite == 'Y': 
		sys.exit('Error: Output file already exists.')
'''

if len(sys.argv) == 3:
	if sys.argv[2] not in ('y','Y'):
		sys.exit('Error: Output .net file already exists.')
else:
		sys.exit('Error: Output .net file already exists.')

# check whether a valid sim file exists and if not, create one if qus available-
oksim = True
if os.path.isfile(filesim):
	with open(filesim, 'r') as fin:
		try:
			line = fin.readline()
			if line[:6] != '# Qucs':				
				oksim = False
		except:
			oksim = False
else:
	oksim = False

if not oksim: # no valid sim file exists so try to create one
	command = 'type qucs'
	result = os.system(command)
	if result == 0:
		command = 'qucs -i ' + filesch + ' -o ' + filesim + ' -n'
		result = os.system(command)
	else:
		command = 'type qucs-spice.qucs'
		result = os.system(command)
		if result == 0:
			command = 'qucs-spice.qucs -i ' + filesch + ' -o ' + filesim + ' -n'
		else:
			oksim = False	

# check whether a valid sim file exists now
if os.path.isfile(filesim):
	with open(filesim, 'r') as fin:
		try:
			line = fin.readline()
			if line[:6] != '# Qucs':
				print('Error: Qucs simulation file is invalid.')
		except:
			oksim = False
			print('Qucs sim file is empty.')
else:
		oksim = False

#-------------------------------------------------------------------------------
# read and process sch file for components--------------------------------------
with open(filesch, 'r') as fin:
	with open(filenet, 'w') as fout:

		# skip lines before components start
		line = '~'; lineno = 0
		while line[:12] != '<Components>' and line != '' and lineno < 100:
			line = fin.readline();	lineno += 1
		
		# read line until components end or > 100 lines
		validparts = []
		while line != '' and lineno < 100:
			line = fin.readline(); lineno += 1
			if line[:13] == '</Components>':
				break
			line = line[3:-2] #remove '	<' and '>\n'
			line = shlex.split(line)	#put into fields on ' ' and stripping double-quotes
			lineout = parsesch()
			if lineout != None:
				fout.write(lineout)

if oksim: # there is a valid simfile, process it to create nets-----------------
	# find last .Def:End to give number of lines to skip 
	with open(filesim, 'r') as fin:
		line='~'; lineno = 0; skip = 0
		while line != '' and lineno < 100:
			line = fin.readline();	lineno += 1
			if '.Def:End' in line:
				skip = lineno

	#read sim file and compile list of nets
	with open(filesim, 'r') as fin:
		# skip the .def lines
		line = '~'; lineno = 0
		while line != '' and lineno < skip:
			line = fin.readline();	lineno += 1

		# read line until components end or > 100 lines
		while line != '' and lineno < 100:
			line = fin.readline(); lineno += 1
			if line[0:1] != '.' and line[0:1] != ' ' and line.find(':') > -1 and line.find(' ') > line.find(':'): 										# its a component line
				line = line[:-1]								 # remove \n			
				line = line.replace(':', ' ', 1) # remove colon marker in components
				line = shlex.split(line)			 	 # put into fields on ' ' and strip "
				parsesim()

	# append net lines to net file
	with open(filenet, 'a') as fout:
		for netno in range (0, len(netlist)):
			line = netlist[netno]
			fout.write('(\n')
			for pinno in range (0, len(line)):
				fout.write(line[pinno]+'\n')
			fout.write(')\n')	

else:
	print ('There was no valid sim file, so the netlist file will contain components but not nets.')

sys.exit(0)

'''
filehelp_contents = resources.read_text(__package__, namehelp)
with resources.path(__package__, namehelp) as filehelp:
	print(filehelp)

fileparts_contents = resources.read_text(__package__, nameparts)
with resources.path(__package__, nameparts) as fileparts:
	print(fileparts)

	webbrowser.open_new(filebrowser)


'''
