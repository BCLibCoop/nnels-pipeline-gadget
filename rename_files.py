######################################################
# Purpose: The purpose of this script is to process  #
#          the MarcXML ingesteed into the system and #
#          assist in the naming of files             #
# Author: Alan Bridgeman                             #
# Date: 2018-02-12                                   #
######################################################

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

from ConfigParser import SafeConfigParser
import subprocess

#----------------------------------------------------#
# Purpose: Get a list of the MarcXML files in the    #
#          current directory or any subdirectory     #
# Parameters: N/A                                    #
# Return: A list of file paths for the MarcXML files #
#----------------------------------------------------#
def getMarcXMLFiles():
	args = ['find', '.', '-name', '*.xml']
	proc = subprocess.Popen(args, stdout=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	lines = stdout.decode('ascii').splitlines()
	return lines

#----------------------------------------------------#
# Purpose: Extract the SCN from the MarcXML record   #
#          if it exits return blank dictionary       #
#          otherwise                                 #
# Parameters: record (Element) - The record we are   #
#                                extracting the SCN  #
#                                for                 #
# Return: A dicitionary with the SCN as the key and  #
#         the record as the value otherwise a blank  #
#         dictionary                                 #
#----------------------------------------------------#
def getSCNFromRecord(record):
	returnVal = {}
	
	for field in record:
		if field.get('tag') == '035':
			for subfield in field:
				if subfield.get('code') == 'a':
					returnVal[subfield.text] = record 
	
	return returnVal

#----------------------------------------------------#
# Purpose: Extract the title information from the    #
#          current MarcXML record                    #
# Parameters; record - The record being processed    #
# Return: The ttile information of the provided      #
#         record otherwise a blank string            #
#----------------------------------------------------#
def getTitleFromRecord(record):
	returnVal = ""
	
	for field in record:
		if field.get('tag') == '245':
			for subfield in field:
				if subfield.get('code') == 'a':
					title = subfield.text
					title = title.replace(",","")
					title = title.replace(":","")
					title = title.replace(".","")
					title = title.replace("'","")
					title = title.replace("?","")
					title = title.replace("&","")
					title = title.replace(" ", "_")
					returnVal = title
	
	return returnVal

#----------------------------------------------------#
# Purpose: To process an individual MarcXML file     #
# Parameters: filename - The filename of the MarcXML #
#             to perform the processsing on          #
# Return: A dictionary matching titles with their    #
#         SCNs for as many titles within the MarcXML #
#         as possible                                #
#----------------------------------------------------#
def processMarcXMLFile(filename):
	# Setup the variables
	returnVal = {}
	with035 = {}
	
	print "parsing " + filename
	
	# Setup the XML parsing of the file
	tree = etree.parse(filename)
	root = tree.getroot()
	
	# Get the SCN
	for record in root:
		with035.update(getSCNFromRecord(record))
	
	# Get the title
	for key,value in with035.iteritems():
		returnVal[getTitleFromRecord(value)] = key
	
	return returnVal


#----------------------------------------------------#
# Purpose: Program entry point                       #
# Parameters: Command line parameters                #
# Return: N/A                                        #
#----------------------------------------------------#
if __name__ == '__main__':
	# Setup the propery variables
	renames = {}
	
	# Get the list of MarcXML files
	lines = getMarcXMLFiles()
	
	# Loop over the MarcXML files to create a lits of filenames we think there should be
	for line in lines:
		renames.update(processMarcXMLFile(line))
	
	# Loop over the filenames we think there should be
	for key,value in renames.iteritems():
		print "File should be named " + value + "_" +  key + ".format"

	#parser = SafeConfigParser()
	#parser.read('The Legacy-metadata.ini')
	#print parser.get('The Legacy', 'title')
