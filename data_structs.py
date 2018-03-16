import dynamic_loader as loader

# Load json (JSON) module
loader.load_json()
json = loader.json

# Load theMetadata_Record classt
loader.load_Metadata_Record()
Metadata_Record = loader.Metadata_Record

bySCN = {}
byTitle = {}

def hasSCN(scn):
	return scn in bySCN
def hasTitle(title):
	return title in byTitle
def getSCN_fromTitle(title):
	return byTitle[title]
def getTitle_fromSCN(scn):
	return bySCN[scn]
def setTitle_fromSCN(scn, title):
	bySCN[scn] = title
def setSCN_fromTitle(title, scn):
	byTitle[title] = scn

#----------------------------------------------------#
# Purpose: Check if the provided attribute with the  #
#          provided value is in the record set       #
#          provided                                  #
# Parameters: records - The set of Metadata_Record ( #
#                       or subclass) to look through #
#                       for the title                #
#             attr_name - The name of the property   #
#                         to check                   #
#             attr_value - The value to check the    #
#                          given property for        #
# Return: Metadat_Record (or subclass) - The record  #
#                                        found       #
#                                        meeting the #
#                                        specified   # 
#                                        criteriad   #
#----------------------------------------------------#
def get_item_with_attr(records, attr_name, attr_value):
	return_value = None
	
	# Loop over the record set to check each one
	for record in records:
		try:
			if isinstance(getattr(record, attr_name), list):
				for gotten_attr in getattr(record, attr_name):
					if attr_value == gotten_attr:
						return_value = record
			else:
				if attr_value == getattr(record, attr_name):
					return_value = record
		except AttributeError:
			pass
	
	return return_value

#----------------------------------------------------#
# Purpose: Check if the provided attribute with the  #
#          provided value is in the record set       #
#          provided                                  #
# Parameters: records - The set of Metadata_Record ( #
#                       or subclass) to look through #
#                       for the title                #
#             attr_name - The name of the property   #
#                         to check                   #
#             attr_value - The value to check the    #
#                          given property for        #
# Return: boolean - If it was found                  #
#----------------------------------------------------#
def has_item_with_attr(records, attr_name, attr_value):
        return get_item_with_attr(records, attr_name, attr_value) != None

#----------------------------------------------------#
# Purpose: To check if a record with the given SCN   #
#          exists in the set specified               #
# Parameters: records - The set of Metadata_Record ( #
#                       or subclass) to look through #
#                       for the SCN                  #
#             SCN - The SCN to check the records for #
# Return: boolean - If there was a matching record   #
#                   found                            #
#----------------------------------------------------#
def has_SCN(records, SCN):
	return has_item_with_attr(records, 'SCN', SCN)

#----------------------------------------------------#
# Purpose: To check if a record with the given title #
#          exists in the set specified               #
# Parameters: records - The set of Metadata_Record ( #
#                       or subclass) to look through #
#                       for the title                #
#             title - The title to check the records #
#                     for                            #
# Return: boolean - If there was a matching record   #
#                   found                            #
#----------------------------------------------------#
def has_title(records, title):
	return has_item_with_attr(records, 'title', title)

#----------------------------------------------------#
# Purpose: To construct a set of Metadata_Record     #
#          objects from the result of a json.load    #
#          call                                      #
# Parameters: json_dict - The dictionaary object     #
#                         provided by the json.load  #
#                         call                       #
# Return: list - A set of Metadata_Record objects    #
#                constructed from the input          #
#----------------------------------------------------#
def records_from_json(json_dict):
	# Make sure this file s in a recognized form (more a sanity check at 
	# this point but might become more later)
	if 'collection' in json_dict:
		records = []
		
		# For each "object" within the collection array create a new 
		# Metadata_Record object and assign the appropriate values
		for record in json_dict['collection']:
			new_record = Metadata_Record()
			for k,v in record.iteritems():
				setattr(new_record, k, v)
			records.append(new_record)
		
		# For each Metadata_Record object that we've now created 
		# validate to mitigate mistakes (human or computer)
		for record in records:
			if not record.validate():
				print 'Removing ' + str(record) + ' because it is an invalid record'
				records.remove(record)
	
	# Return the results
	return records

#----------------------------------------------------#
# Purpose: To construct a set of Metadata_Record     #
#          objects from the input of a tab seperated #
#          file                                      #
# Parameters: head_line - The line that has the      #
#                         columns names (denotes the #
#                         schema of the file)        #
#            lines - The array of lines to parse     #
#                    into individual records         #
# Return: list - A set of Metadata_Record objects    #
#               constructed from the input           #
#----------------------------------------------------#
def records_from_tab_seperated(head_line, lines):
	records = []
	
	# Parse the schema (what each column means)
	props = head_line.split('\t')
	for index in range(0, len(props)):
		props[index] = props[index].strip()
	
	# If the first line of the array and the schema line are the same remove
	# it (so that we don't try to parse it as a line
	if lines[0] == head_line:
		lines.remove(lines[0])
	
	# Loop over each line an create a new Metadata_Reord object assign its
	# values to is appropriate property (as determined by the schema)
	for line in lines:
		new_record = Metadata_Record()
		tokens = line.split('\t')
		for index in range(0, len(tokens)):
			setattr(new_record, props[index], tokens[index].decode('utf-8').strip())
		records.append(new_record)
	
	# For each of the records we now have lets validate them so that we know
	# there wasn't hany mistakes made (human or program)
	for record in records:
		if not record.validate():
			print 'Removing ' + str(record) + ' because it is an invalid record'
			recoreds.remove(record)
	
	# Return result
	return records
