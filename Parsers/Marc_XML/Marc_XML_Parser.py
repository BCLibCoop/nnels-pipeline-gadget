from Parsers.Metadata_XML_Parser import Metadata_XML_Parser
from File_Writers.Metadata_File_Writer import Metadata_File_Writer
from File_Writers.Metadata_JSON_Writer import Metadata_JSON_Writer
from File_Writers.Metadata_Tab_Seperated_Writer import Metadata_Tab_Seperated_Writer
from File_Writers.Metadata_CSV_Writer import Metadata_CSV_Writer
from Marc_XML_RecordSet import Marc_XML_RecordSet
from Marc_XML_Record import Marc_XML_Record
import funcs

import dynamic_loader as loader
loader.load_subprocess()
subprocess = loader.subprocess

DEBUG_MODE = False
#====================================================#
# Purpose: Provide a concreate implementation of the $
#          metadata parser abstract class for the    #
#          specific purpose of parsing Marc XML      #
#          files                                     #
# Properties: parsable_files (Metadata_Parser) - See #
#                                                Doc #
#             recordset (Metadata_Parser) - See Docs #
#             trees (Metadata_XML_Parser) - See Docs #
#             record_tag (Metadata_XML_Parser) - See #
#                                                Doc #
# Methods: files_to_trees (Metadata_XML_Parser)-See  #
#                                               Docs #
#          file_to_tree (Metadata_XML_Parser) - See  #
#                                               Docs #
#          find_records (Metadata_XML_Parser) - See  #
#                                               Docs #
#          _recordset_set (Overriden) - Sets the     #
#                                       recoredset   #
#                                       property     #
#          find_parsable_files (Overriden) - finds   #
#                                            proper  #
#                                            files   #
#          parse_record (Overriden) - Provides       #
#                                     implementation #
#                                     of the parsing #
#                                     of records     #
# Superclass: Metadata_XML_Parser                    #
#====================================================#
class Marc_XML_Parser(Metadata_XML_Parser):
	# A dictionary of corresponding Marc to labeled values
	Marc_index = {
		'SCN':{'tag':'035', 'code':'a'},
		'title':{'tag':'245', 'code':'a'}
	}
	
	#----------------------------------------------------#
	# Purpose: Initialize a Marc_XML_Parser with         #
	#          default variables (constructor)           #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             patterns (optional) - 
	# Return: N/A                                        #
	# See Also: __init__ documentation in Python         #
	#           documentaion                             #
	#----------------------------------------------------#
	def __init__(self, patterns=None):
		# Check if the pattern parameter was set
		if patterns is not None:
			self.find_parsable_files(custom_patterns=patterns)
			
			super(Marc_XML_Parser, self).__init__(self.parsable_files)
		else:
			super(Marc_XML_Parser, self).__init__()
		
		# Set the recordset property to a new Marc_XML_Recordset object
		self.recordset = Marc_XML_RecordSet()
	
	#----------------------------------------------------#
	# Purpose: To set the recordset property (indirectly #
	#          ). Perform validation in checking that    #
	#          the supplied records argument is a        #
	#          instance of the Marc_XML_RecordSet class  #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: N/A                                        #
	# Overrides: _recordset_set (Metadata_Parser)        #
	#----------------------------------------------------#
	def _recordset_set(self, records):
		if isinstance(records, Marc_XML_RecordSet):
			self._recordset = records
		else:
			raise TypeError
	
	#----------------------------------------------------#
	# Purpose: Getter for the record_tag property (tells #
	#          what tag indicates a record)              #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: string - The name of the tag that          #
	#                  represents the record ('record'   #
	#                  in the case of Marc XML)          #
	# Overrides: record_tag (Metadata_XML_Parser)        #
	# See Also: @property in the Python documentation    #
	#----------------------------------------------------#
	@property
	def record_tag(self):
		return 'record'
	
	#----------------------------------------------------#
	# Purpose:
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             look_dir (optional) -
	#             custom_patterns (optional) -
	# Return: List - A list of files for parsing         #
	# Overrides: find_parsable_files (Metadata_Parser)   #
	#----------------------------------------------------#
	def find_parsable_files(self, look_dir='.', custom_patterns=['*.xml']):
		# Check if the parent_dir is that special . character
		if look_dir == '.':
			# Because there is prefix all entries with .*/
			full_pattern = funcs.combine_regex(custom_patterns, prefix_each='.*/')
		else:
			# Because we're not looking in the current directory no
			# special processing has to occur
			full_pattern = funcs.combine_regex(custom_patterns)
		
		# Setup arguments for the use of the find utility
		args = ['find', '-E', look_dir, '-regex', full_pattern]
		
		# DEBUGGING: Print statement showing whats being run
		print 'Running ' + args[0] + ' with arguments ' + str(args[-1:])
		
		# Actually running the command
		proc = subprocess.Popen(args, stdout=subprocess.PIPE)
		stdout, stderr = proc.communicate()
		
		# Break the output up into lines
		Marc_XML_files = stdout.decode('ascii').splitlines()
		
		# Return the results
		return Marc_XML_files
	
	#----------------------------------------------------#
	# Purpose: To parse an individual subfield element   #
	#          in the Marc XML file (callback for        #
	#          find_tag_with_attr call)                  #
	# Parameters: self (implicit) -
	#             subfield -
	#             name -
	#             record -
	#----------------------------------------------------#
        def parse_subfield(self, subfield, name, record):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for parse_subfield (Marc_XML_Parser)'
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print 'Subfield: ' + str(subfield)
			print 'Subfield - Text: ' + subfield.text.encode('utf-8')
			print 'Name: ' + str(name)
			print 'Record: ' + str(record)
			print '===================================================='
		if hasattr(record, name) and getattr(record, name) is not None:
			setattr(record, name, [getattr(record, name), subfield.text])
		else:
			# Set a attribute/property of the Marc_XML_Record to be
			# of the name name and value of subfield.text
			setattr(record, name, subfield.text)
		
		return_result = {name:  getattr(record, name)}
		
		return return_result
	
	#----------------------------------------------------#
	# Purpose: To parse an individual datafield element  #
	#          in the Marc XML file (callback function   #
	#          for find_tag_with_attr call)              #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             data_field - The XML Element that      #
	#                          represents the individual #
	#                          data field being          #
	#                          processed                 #
	#             name - The name of the value we're     #
	#                    trying to get (ex. SCN, title,  #
	#                    etc...)                         #
	#             subfield - The subfield code to look   #
	#                        for to get the desired      #
	#                        value                       #
	#             record - The Marc_XML_Record object    #
	#                      that all parsed values are    #
	#                      added to                      #
	# Return: N/A
	#----------------------------------------------------#
	def parse_data_field(self, data_field, name, subfield, record):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for parse_data_field (Marc_XML_Parser)'
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print 'Datafield: ' + str(data_field)
			print '===================================================='
		
		# What attributes (with associated values) to look for
		look_for_attrs = {'code':subfield}
		
		# What method to call when an appropriate element is found
		callback = self.parse_subfield
		
		# ADDITIONAL (excluding self AND the element) arguments to the
		# callback method
		callback_args = {
			'record':record,
			'name':name
		}
		
		# Call the methoD
		return_result = self.find_tag_with_attr('subfield', look_for_attrs, callback, callback_args, data_field)
		
		return return_result
	
	#----------------------------------------------------#
	# Purpose: To parse an individual record (callback   #
	#          function for find_record)                 #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             record - The XML Element that          #
	#                      represents an individual      #
	#                      record                        #
	# Return: N/A                                        #
	# Overrides: parse_record (Metadata_XML_Parser)      #
	#----------------------------------------------------#
	def parse_record(self, record):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for parse_record (Marc_XML_Parser)'
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print 'Record; ' + str(record)
			print '===================================================='
		
		return_result = []
		
		# Create a new Marc_XML_Record object for the purposes of
		# holding all the information contained within the record in a
		# clear dedicated data structure
		record_obj = Marc_XML_Record()
		
		# Loop over the Marc_index to extract as much meaningful info as
		# we can
		for k,v in self.Marc_index.iteritems():
			# What attributes (with associated values) to look for
			look_for_attrs = {'tag':v['tag']}
			
			# What method to call when an appropriate element is
			# found
			callback = self.parse_data_field
			
			# ADDITIONAL (excluding self AND the element) arguments
			# to the callback method
			callback_args = {
				'name':k,
				'subfield':v['code'],
				'record':record_obj
			}
			
			# Call the method
			return_result.append(self.find_tag_with_attr('datafield', look_for_attrs, callback, callback_args, record))
		
		# Add the record to the recordset
		self.recordset.add_record(record_obj)
		
		curr_index = 0
		while curr_index < len(return_result):
			if return_result[curr_index] is None:
				del return_result[curr_index]
			else:
				curr_index += 1
		
		new_return_result = {}
		for return_val in return_result:
			if isinstance(return_val, dict):
				for k,v in return_val.iteritems():
					new_return_result[k] = v
			elif isinstance(return_val, list):
				for item in return_val:
					for k,v in item.iteritems():
						new_return_result[k] = v

		
		if len(new_return_result) > 0:
			return_result = new_return_result
		
		#print '[parse_record]Preparing to Return: ' + str(return_result)
		
		return return_result
	
	#----------------------------------------------------#
	# Purpose: Generic trigger method similar to that    #
	#          of execute or run in similar models       
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def parse(self):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for parse (Marc_XML_Parser)'
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print '===================================================='
		
		return_result = {}
		
		# If the parsable files isn't set already set it up with
		# defaults
		if self.parsable_files is None or len(self.parsable_files) < 1:
			self.parsable_files = self.find_parsable_files()
		
		# Build the XML trees from the parsable_files property
		self.files_to_trees(self.parsable_files)
		
		# For each file/tree loop over and find the records in it
		for parsable_file in self.parsable_files:
			return_result[parsable_file] = self.find_records(parsable_file)
		
		return return_result
	
	#----------------------------------------------------#
	# Purpose: Similar to parse in that it is a trigger  #
	#          method to simply start the parsing of the #
	#          files. The difference being this outputs  #
	#          the results to a file with the designated #
	#          name and in the designated type           #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             output_file - The filename (including  #
	#                           path) of the file to     #
	#                           output to (preferablly   #
	#                           without a file           #
	#                           extensions but...)       #
	#             fromat (optional) - The format in      #
	#                                 which the output   #
	#                                 file should be in. #
	#                                 By default this is #
	#                                 JSON beause this   #
	#                                 is a schemaless    #
	#                                 database structure #
	#                                 and the data       #
	#                                 between reords     #
	#                                 doesn't            #
	#                                 NECCESSARLY follow #
	#                                 a consistant       #
	#                                 schema and JSON is #
	#                                 common place in    #
	#                                 other programs     #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def parse_to_file(self, output_file, format='json'):
		# Parse the files using the generic trigg3er method
		return_result = self.parse()
		
		print 'Format to use: ' + format
		
		# Give the filename the appropriate extension
		if format == 'json' and not output_file.endswith('.json'):
			# TO BE IMPLEMENTED: Strip extension if it exists
			output_file = output_file + '.json'
		elif format == 'tabs' and not output_file.endswith('.txt'):
			# TO BE IMPLEMENTED: Strip extension if it exists
			output_file = output_file + '.txt'
		elif format == 'csv' and not output_file.endswith('.csv'):
			# TO BE IMPLEMENTED: Strip extension if it exists
			output_file = output_file + '.csv'
		
		writer = None
		if format == 'json':
			writer = Metadata_JSON_Writer()
		elif format == 'tabs':
			writer = Metadata_Tab_Seperated_Writer()
		elif format == 'csv':
			writer = Metadata_CSV_Writer()
		
		if isinstance(writer, Metadata_File_Writer):
			writer.write_to_file(output_file, self.recordset)
		
		return return_result
