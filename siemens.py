#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os, errno
import sys
import re
import shutil
import time
import subprocess

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

directory = sys.argv[1]
pattern = '.*rda$'
format = 'rda'
config = '' #add more options for analysis

# find all files in the dir  
fileList = []
for root, subFolders, files in os.walk(directory):  
	for file in files:
		if re.search(pattern,file):
			fileList.append(os.path.join(root,file))  
			#print(file)

w = {}
s = []
s_num = []
s_keys = []
s_basis = []
for file in fileList:
	d = {}
	Lines = []
	f = open(file,"r")
	for line in f:	
		Lines.append(line)
		if 'End of header' in line:
			break
	f.close()
	for line in Lines[1:-1]:
		line=line.translate(None,' \r\n')
		line=line.replace('^','_')
		variable=line.split(':', 1);
		d[variable[0]]=variable[1]
	if (('water' in d['ProtocolName']) or ('water' in file)):
		w[d['PatientName']+'_'+d['StudyDate']+'^'+d['TE']+d['TR']+d['VOIPositionTra']+d['VOIPositionSag']+d['FoVHeight']]=file
	else:
		#print(d)
		s.append(file)
		s_keys.append(d['PatientName']+'_'+d['StudyDate']+'^'+d['TE']+d['TR']+d['VOIPositionTra']+d['VOIPositionSag']+d['FoVHeight'])
		s_num.append(d['SeriesNumber'])

#wybranie odpowiedniego basis-seta w zalenosci od czasu echa (TE) w metodzie
	if '30' in d['TE']:
		s_basis.append('/home/jovyan/.lcmodel/basis-sets/siemens-3t/gamma_press_te30_123mhz_104.basis')
	elif '135' in d['TE']:
		s_basis.append('/home/jovyan/.lcmodel/basis-sets/siemens-3t/gamma_press_te135_123mhz_084.basis')
	elif '144' in d['TE']:
		s_basis.append('/home/jovyan/.lcmodel/basis-sets/siemens-3t/gamma_press_te144_123mhz_104.basis')
	elif '270' in d['TE']:
		s_basis.append('/home/jovyan/.lcmodel/basis-sets/siemens-3t/gamma_press_te270_123mhz_091.basis')
	elif '68' in d['TE']:
		s_basis.append('/home/jovyan/.lcmodel/basis-sets/siemens-3t/3t_IU_MP_te68_748_ppm_inv.basis')
	else:
		print("HEJAAAAAAAAAAAAAAAA")

filenames=[]
i = 0
for file, key, num, basis_set_dir in zip(s,s_keys,s_num,s_basis):
	print('File: ' + file)
	print('Basis set: ' + basis_set_dir)
	filename=(key.split('^',1)[0]+'_'+num)
	patient_dir = os.path.join(os.path.dirname(file), filename)

	if not os.path.exists(patient_dir):	
		os.mkdir(patient_dir)
	if not os.path.exists(os.path.join(patient_dir,'h2o/')):	
		os.mkdir(os.path.join(patient_dir,'h2o/'))	
	if not os.path.exists(os.path.join(patient_dir, 'met/')):	
		os.mkdir(os.path.join(patient_dir,'met/'))

	if key in w:
		file_wat=w[key]
		convert_bin2raw = ('/home/jovyan/.lcmodel/siemens/bin2raw ' + file_wat + ' ' + patient_dir+'/ ' +'h2o')
		os.system(convert_bin2raw)
		print('Water file: ' + file_wat)
	else:
		print('-------------' + filename + ' Water scaling OFF' + '--------------------')

	convert_bin2raw = ('/home/jovyan/.lcmodel/siemens/bin2raw ' + file + ' ' +patient_dir+'/ ' +'met')
	os.system(convert_bin2raw)

	shutil.copy(os.path.join(patient_dir,'met/cpStart'), os.path.join(patient_dir,'met/myControl'))
	if os.path.exists(os.path.join(patient_dir,'h2o/RAW')):
		water_path = os.path.join(patient_dir,'h2o/RAW')
	csv_path = os.path.join(patient_dir,'spreadsheet.csv')
	table_path = os.path.join(patient_dir,'table')
	coord_path = os.path.join(patient_dir,'coord')


	file_content = list()
	source = open(os.path.join(patient_dir,'met/myControl'), 'r')
	for line in source.readlines():
		file_content.append(line)
	file_content.insert(0, "$LCMODL\n")
	file_content.insert(len(file_content), "\n$END")
	file_content.insert(len(file_content)-1, "key = 210387309\n")
	file_content.insert(len(file_content)-1, "filbas= '"+basis_set_dir+"'\n")
	file_content.insert(len(file_content)-1, "filcsv= '"+csv_path+"'\n")
	file_content.insert(len(file_content)-1, "filtab= '"+table_path+"'\n")
	file_content.insert(len(file_content)-1, "filcoo= '"+coord_path+"'\n")
	if os.path.exists(os.path.join(patient_dir,'h2o/RAW')):
		file_content.insert(len(file_content)-1, "filh2o= '" +water_path+"'\n")	
		file_content.insert(len(file_content)-1, "dows= T\n")	
		file_content.insert(len(file_content)-1, "doecc= T\n")	
	file_content.insert(len(file_content)-1, "lcsv= 11\n")	
	file_content.insert(len(file_content)-1, "ltable= 7\n")
	file_content.insert(len(file_content)-1, "lcoord= 9\n")

	for root, dirs, files in os.walk(os.path.dirname(file)):
    		for file in files:
        		if "wconc" in file:
             			f = open(os.path.join(root,file), 'r')
				wconc=f.read()
				f.close
				print("Volume corrected WCONC = " + wconc)
				file_content.insert(len(file_content)-1, "wconc= " + wconc + "\n")

	source.close()
	content = open(os.path.join(patient_dir,'met/myControl'), 'w')	
	for line in xrange(len(file_content)):
		content.write(file_content[line])
	content.close()
	

	command = ('/home/jovyan/.lcmodel/bin/lcmodel <' +os.path.join(patient_dir,'met/myControl'))
	os.system(command)
	output_pdf = ('ps2pdf ' +os.path.join(patient_dir, 'ps ') +os.path.join(patient_dir,filename+'.pdf'))
	os.system(output_pdf)
	delete_ps = ('rm '+os.path.join(patient_dir,'ps'))
	os.system(delete_ps)		
	

