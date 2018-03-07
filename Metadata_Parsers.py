# My Modules;
import dynamic_loader as loader
import funcs				# Requried to use some generic functions

# Load abc (Abstract Class) module
loader.load_abc()
abc = loader.abc

# Load subprocess (Command Line) module
loader.load_subprocess()
subprocess = loader.subprocess

# Load etree (XML)  module
loader.load_XML_parser()		# Reqried to use XML parser module
etree = loader.etree

# Load the Metadata_Record class
loader.load_Metadata_Record()
Metadata_Record = loader.Metadata_Record

from Metadata_File_Writers import Metadata_File_Writer, Metadata_JSON_Writer

DEBUG_MODE = False

#====================================================#
# Purpose: Provide an abstract base class for        #
#          metadata parsers for the purposes of      #
#          subtype polymorphism                      #
# Properties: parsable_files - The files to parse    #
#             recordset - A collection of records    #
#                         parsed from the dired data #
#                         NOTE: This property is     #
#                               special in that I    #
#                               force all subclasses #
#                               to implemented a     #
#                               setter for it. I     #
#                               employ a indirection #
#                               technique that has   #
#                               me call a secondary  #
#                               abstract method      #
# Methods: _recordset_set (abstract) - Indirection   #
#                                      merthod for   #
#                                      forcing       #
#                                      subclasses to #
#                                      implement     #
#                                      recordset     #
#                                      setter        #
#          find_parsable_files (abstract) - Find     #
#                                           files    #
#                                           that     #
#                                           could be #
#                                           parsed   #
# Superclass: object                                 #
#====================================================#
class Metadata_Parser(object):
	__metaclass__ = abc.ABCMeta
	parsable_files = []
	
	#----------------------------------------------------#
	# Purpose: Getter for the recordset property         #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: The value of the recordset property        #
	# See Also: @property in the Pythobn documentation   #
	#----------------------------------------------------#
	@property
	def recordset(self):
		return self._recordset
	
	#----------------------------------------------------#
	# Purpose: Actual setter of the recordset property   #
	#          but delegates back to the abstracct       #
	#          _recordset_set                            #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             records - The value desired for the    #
	#                       recordset property to become #
	# Return: N/A                                        #
	# See Also: @<var>.setter in Python documentation    #
	#----------------------------------------------------#
	@recordset.setter
	def recordset(self, records):
		self._recordset_set(records)
	
	#----------------------------------------------------#
	# Purpose: A sudo-setter (indirect setter) method    #
	#          for the recordset property mostly to make #
	#          the variable "abstract" so that all       #
	#          subclasses must implement their own way   #
	#          to set the variable as its a fundemental  #
	#          design choice for the parser              #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             records - The collection of records to #
	#                       set the recordset property   #
	#                       to                           #
	# Return: N/A                                        #
	# Raises: NotImplementedError - Can't call the       #
	#                               method for the base  #
	#                               class                #
	# See Also: @abstractmethod in the abc module        #
	#           documentation in the Python              #
	#           documentation                            #
	#----------------------------------------------------#
	@abc.abstractmethod
        def _recordset_set(self, records):
                raise NotImplementedError
	
	#----------------------------------------------------#
	# Purpose: To find all parsable files based on a     #
	#          directory or pattern                      #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             look_dir - Directory to invoke find on #
	#                        meaning that all files      #
	#                        matching at least one of    #
	#                        the patterns in the         #
	#                        patterns parameter within   #
	#                        the directory specified     #
	#                        are found                   #
	#                        NOTE: use . to represent    #
	#                              current directory     #
	#             patterns - A set of Regular            #
	#                        Expressions (reges) to use  #
	#                        in the find utility to find #
	#                        the desired files           #
	# Return: List - A list of filenames that match at   #
	#                least one of the patterns specified #
	#                in the parametersaned are beneath   #
	#                the direcotry specified             #
	# Raises: NotImplementedError - Can't call the       #
	#                               method of the base   #
	#                               class                #
	# See Also: @abstractmethod in abc module            #
	#           documentation in Python documentation    #
	#----------------------------------------------------#
	@abc.abstractmethod
	def find_parsable_files(self, look_dir, patterns):
		raise NotImplementedError
	

#====================================================#
# Purpose: A tier 2 abstract class in the            #
#          Metadata_Parser hiearchy meant to         #
#          simplify the processing of XML file based #
#          metadata parsing                          #
# Properties: parsable_files (Metadata_Parser) - See #
#                                                Doc #
#             recordset (Metadata_Parser) - See Docs #
#             trees - A dictionary of XML tree       #
#                     objects if applicable          #
#             record_tag (abstract) - The name of    #
#                                     the tag that   #
#                                     represents a   #
#                                     tag (ex.       #
#                                     'record')      #
# Methods: _recordset_set (Metadata_Parser) - See    # 
#                                             Docs   #
#          find_parsable_files (Metadata_Parser)-See #
#                                                Doc #
#          files_to_trees - Construct XML tree       #
#                           objects from a list of   #
#                           files                    #
#          file_to_tree - Construct XML tree from a  #
#                         file                       #
#          parse_record (abstract) - Do the actual   #
#                                    parsing of the  #
#                                    record element  #
#                                    as defined by   #
#                                    the record_tag  #
#                                    property        #
#          find_record - Find the record elements    #
#                        and call the parse_record   #
#                        method                      #
# Superclass: Metadata_Parser                        #
#====================================================#
class Metadata_XML_Parser(Metadata_Parser):
	#----------------------------------------------------#
        # Purpose: Initialize a Metadata_XML_Parser with     #
        #          default variables (constructor)           #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
	#             XML_files (optional) - If specified    #
	#                                    used as the     #
	#                                    source for the  #
	#                                    parsing by      #
	#                                    loading in the  #
	#                                    XML file into a #
	#                                    XML tree object #
        # Return: N/A                                        #
        # See Also: __init__ documentation in Python         #
        #           documentaion                             #
        #----------------------------------------------------#
	def __init__(self, XML_files=None):
		# Call the parents constructor
		super(Metadata_XML_Parser, self).__init__()
		
		self.trees = {}
		self.trees_without_ns = {}
		
		# Check if the file parameter was set
		if XML_files is not None:
			# TO BE IMPLEMENTED: Check if XML_files is an actual 
			#                    set of files or a set regexs/paths 
			#                    that would need to be expaneded 
			#                    into a set of files
			
			# Load the file in so that we can use it as an XML tree 
			# instead
			self.file_to_trees(XML_files)
	
	#----------------------------------------------------#
	# Purpose: To parse a file into a XML tree object    #
	#          for ease parsing using the built in       #
	#          etree.parse function                      #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  # 
	#                               is being invoked on  #
	#             XML_file - The file (path) to be       #
	#                        converted into the XML tree #
	#                        object                      #
	# Return: N/A                                        #
	# NOTE: Sets up a self.tree dictionary property that #
	#       uses the XML_file paramter as the keys       #
	#----------------------------------------------------#
	def file_to_tree(self, XML_file):
		tree = etree.parse(XML_file)
		self.trees[XML_file] = tree.getroot()
		
		it = etree.iterparse(XML_file)
		for _, el in it:
			el.tag = el.tag.split('}', 1)[1]  # strip all namespace
		self.trees_without_ns[XML_file] = it.root
	
	#----------------------------------------------------#
	# Purpose: To parse a set of files int a set of XML  #
	#          tree objects for ease of parsing          #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being invoked on  #
	#             file_list - The set of files (paths)   #
	#                         to be converted into a set #
	#                         of XML treee objects       #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def files_to_trees(self, file_list):
		# Loop over the files in the list
		for XML_file in file_list:
			self.file_to_tree(XML_file)
	
	def add_XML_tree(self, name, input):
		if type(input) is list:
			self.files_to_trees(input)
		else:
			if '<' not in input:
				self.file_to_tree(input)
			else:
				self.tress[name] = etree.fromstring(input)
	#----------------------------------------------------#
	# Purpose: Getter for an abstract property           #
	#          record_tag that each subclass needs to    #
	#          set individually                          #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being invoked on  #
	# Return: N/A                                        #
	# Raises: NotImplementedError - Can't access the     #
	#                               variable/property of #
	#                               the base class (     #
	#                               point is to force    #
	#                               subclasses to        #
	#                               implement what to    #
	#                               return)              #
	# See Also: @abstractproperty in the abc module      #
	#           documentation in the Python              #
	#           documentation                            #
	#----------------------------------------------------#
	@abc.abstractproperty
	def record_tag(self):
		raise NotImplementedError
	
	#----------------------------------------------------#
	# Purpose: Force all subclasses to have a method to  #
	#          perform the actual parsing of the         #
	#          applicable XML Element object             #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being invoked on  #
	#             record - The XML Element object to be  #
	#                      parsed                        #
	# Return: N/A                                        #
	# Raises: NotImplementedError - Can't call the base  #
	#                               class's abstract     #
	#                               method               #
	# See Also: @abstractmethod in the abc module        #
	#           documentation in the Python              #
	#           documentation                            #
	#----------------------------------------------------#
	@abc.abstractmethod
	def parse_record(self, record):
		raise NotImplementedError
	
	#----------------------------------------------------#
	# Purpose: Find the appropriate records and trigger  #
	#          the parsing of them                       #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being invoked on  #
	#             from_file - The file to look in for    #
	#                         records elements (however  #
	#                         the subclass defines       #
	#                         record elements            #
	#             curr_elem (optional) - The elemet      #
	#                                    we're currently #
	#                                    looking at (    #
	#                                    uses recurrsion #
	#                                    )               #
	# Return: N/A                                        #
	# NOTE: This method calls the parse_record method    #
	#       whenever it finds a new record               #
	#----------------------------------------------------#
	def find_records(self, from_file, curr_elem=None):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for find_records (Metadata_XML_Parser) '
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print 'From File: ' + str(from_file)
			print 'Current Element: ' + str(curr_elem)
			print '===================================================='
		# call the find_tag function with the appropraite arguments
		return_result = self.find_tag(self.record_tag, self.parse_record, root=curr_elem, from_file=from_file)
		
		# Return the results
		return return_result
	
	#----------------------------------------------------#
	# Purpose: Find the elements that have the given     #
	#          attributes                                #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being invoked on  #
	#             desired_tag - The tag to find          #
	#             desired_attr_dict - A dictionary where #
	#                                 the keys are the   #
	#                                 attribute names    #
	#                                 and the values are #
	#                                 the values to look #
	#                                 for                #
	#             callback - The callback for when       #
	#                        elements are found          #
	#             callback_args - Arguments to the       #
	#                             callback function      #
	#             root_elem - The root Element object to #
	#                         look within for the tags   #
	#                         with the given attributes  #
	#----------------------------------------------------#
	def find_tag_with_attr(self, desired_tag, desired_attr_dict, callback, callback_args, root_elem):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for find_tag_with_attr (Metadata_XML_Parser)'
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print 'Desired Tag: ' + str(desired_tag)
			print 'Desired Attributes: ' + str(desired_attr_dict)
			print 'Callback: ' + str(callback)
			print 'Callback Arguments: ' + str(callback_args)
			print 'Root Element: ' + str(root_elem)
			print '===================================================='
		
		# Create the callback arguments for the check_attr function that
		# we'll need to specify for the find_tag call
		check_attr_args = {'attrs':desired_attr_dict,
		                   'callback':callback,
		                   'callback_args':callback_args}
		
		# Call the find_tag function with the appropriate parameters
		return_result = self.find_tag(desired_tag, self.check_attr, check_attr_args, root=root_elem)
		
		# Return the results
		return return_result
	
	#----------------------------------------------------#
	# Purpose: To check if the current element has the   #
	#          desired attributes. This is a seperate    #
	#          method because of code reuse in           #
	#          particular the find_tag method ONLY finds #
	#          the desired tag elements and doesn't do   #
	#          any additional checking. It would make    #
	#          the method overly complex to add this     #
	#          functionality directly to that method so, #
	#          instead replace the callback normally     #
	#          supplied to that method by the calling    #
	#          (concrete) class with this method and     #
	#          perform checks in this method and call    #
	#          the specificed callback with the element  #
	#          this method recieves if and only if the   #
	#          attributes match what was asked. In       #
	#          shorter but less explict terms it works   #
	#          as a transparent filter (to the calling   #
	#          class)                                    #
	# Parameters: self (implicit) - 
	#             elem - The element being inspected     #
	#             attrs - A dictionary containing the    #
	#                     desired key-value combinations #
	#             callback - A callback function to      #
	#                        invoke when an appropraite  #
	#                        element is found            #
	#             callback_args - A dictionary of        #
	#                             ADDITIONAL arguments   #
	#                             to supply to the       #
	#                             callback               #
	#----------------------------------------------------#
	def check_attr(self, elem, attrs, callback, callback_args):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for check_attr (Metadata_XML_Parser)   '
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print 'Element: ' + str(elem)
			print 'Attributes: ' + str(attrs)
			print 'Callback: ' + str(callback)
			print 'Callback Arguments: ' + str(callback_args)
			print '===================================================='
		# Set the return variable to initially be None
		return_result = None
		
		# Check that it has and is equal to the ones we want. If so, 
		# call the callback
		for k,v in attrs.iteritems():
			if elem.get(k) == v:
				return_result = self._use_callback(elem, callback, callback_args)
		
		# Return the result
		return return_result
	
	#----------------------------------------------------#
	# Purpose: To abstract some of the callback calling  #
	#          complexity out of other methods           #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             curr_elem - The current element being  #
	#                         processed                  #
	#             callback - The callback function/      #
	#                        method to use               #
	#             callback_args - The arguments to       #
	#                             supply to the callback #
	# Return: The return of callback                     #
	#----------------------------------------------------#
	def _use_callback(self, curr_elem, callback, callback_args):
		if DEBUG_MODE:
			print '===================================================='
                        print 'Call Summary for _use_callback (Metadata_XML_Parser)     '
                        print '----------------------------------------------------'
                        print 'Self: ' + str(self)
                        print 'Current Element: ' + str(curr_elem)
                        print 'Callback: ' + str(callback)
                        print 'Callback Arguments: ' + str(callback_args)
                        print '===================================================='
		
		# Set the return variable originally to None
		return_result = None
		
		# Check that people aren't trying to get away 
		# with not specifing the callback 
		if callback is not None:
			# Check if there was any callback arguments given or not
			if callback_args is None:
				return_result = callback(curr_elem)
			else:
				return_result = callback(curr_elem, **callback_args)
		else:
			return_result = curr_elem.tag #etree.tostring(curr_elem)
		
		# Return the result
		return return_result
	
	#----------------------------------------------------#
	# Purpose: The purpose of this method is to find the #
	#          desired tag and call the apporpriate      #
	#          callback with that element as a parameter #
	#          (in essencd it works as wrapper method    #
	#          around the ElementTree.iter command       #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             desired_tag - The tag to be lookin for #
	#             callback - The callback function to    #
	#                        invoke when the desired tag #
	#                        is found                    #
	#             callback_args (Optional) - Any         #
	#                                        additional  #
	#                                        arguments   #
	#                                        to be used  #
	#                                        when making #
	#                                        the         #
	#                                        callback    #
	#                                        call        #
	#             root (Optional) - The root element to  #
	#                               "look" under         #
	#             from_file (Optional) - The file to     #
	#                                    "look" in       #
	# Return: An array containing the non-None results   #
	#         that were provided by the callbacks        #
	#----------------------------------------------------#
	def find_tag(self, desired_tag, callback, callback_args=None, root=None, from_file=None):
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for find_tag (Metadata_XML_Parser)     '
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print 'Desired Tag: ' + str(desired_tag)
			print 'Callback: ' + str(callback)
			print 'Callback Arguments: ' + str(callback_args)
			print 'Root: ' + str(root)
			print 'From File: ' + str(from_file)
			print '===================================================='
		
		return_result = []
		
		# If we've specified a file do some simple checks
		if root is None:
			# Check that we don't have the erronous case of both 
			# not being specified
			if from_file is None:
				raise NotImplementedError
			else:
				# Check if the desired tag provided has a 
				# namespace attached to it or not (denoted by 
				# {namespace})
				if desired_tag.startswith('{'):
					new_root = self.trees[from_file].getroot()
				else:
					new_root = self.trees_without_ns[from_file]
				# Recall this method with the new parameter
				return_result = self.find_tag(desired_tag, callback, callback_args, root=new_root)
		else:
			# Find all elements of the given type within the subree
			elems = root.iter(desired_tag)
			
			# Loop over of the found elements and call the callback
			# with it
			for elem in elems:
				callback_return = self._use_callback(elem, callback, callback_args)
				return_result.append(callback_return)
		
		# Delete any extranous None values
		curr_index = 0
		while curr_index < len(return_result):
                        if return_result[curr_index] is None:
                               	del return_result[curr_index]
			else:
				curr_index += 1
		
		# If there is only a single entry then assign the variable to 
		# that (rather than having a needless list with one element)
                if len(return_result) == 1:
                        return_result = return_result[0]
		
		# Return the result
		return return_result

#====================================================#
# Purpose: A more specific concrete class for Marc   #
#          XML records                               #
# Properties: title (Metadata_Record) - See Docs     #
#             SCN (Metadata_Record) - See Docs       #
# Superclass: Metadata_Record                        #
#====================================================#
class Marc_XML_Record(Metadata_Record):
	#----------------------------------------------------#
        # Purpose: Initialize a Metadata_Recored with        #
        #          default variables (constructor)           #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
        # Return: N/A                                        #
        # See Also: __init__ documentation in Python         #
        #           documentaion                             #
        #----------------------------------------------------#
        def __init__(self):
                super(Marc_XML_Record, self).__init__()
	
	@property
	def SCN(self):
		return self._SCN
	
	@SCN.setter
	def SCN(self, value):
		if value is not None:
			if '(' in value:
				value = value[value.find(')') + 1:]
				value = value.strip()
		
		self._SCN = value
	
	@property
	def title(self):
		return self._title
	
	@title.setter
	def title(self, value):
		if value is not None:
			# Remove special characters
			specialchars = [",", ":", ".", "'", "?", "&", "/"]
			
			for char in specialchars:
				value = value.replace(char, "")
			
			# Strip any extranous whitespace
			value = value.strip()
			
			# Underscore remaining whitespace
			value = value.replace(" ", "_")
		
		self._title = value
	
	#def __str__(self):
	#	return super(Marc_XML_Record, self).__str__()

#====================================================#
# Purpose: A collection data structure to ensure     #
#          proper typing of entries within the       #
#          sturcture as well as provide any          #
#          additional processing or functionality as #
#          requried                                  #
# Propterties: records - The records held within the #
#                        data structure              #
# Methods: add_record - To add a record to the data  #
#                       structure                    #
# Superclass: object                                 #
#====================================================#
class Marc_XML_RecordSet(object):        
	#----------------------------------------------------#
        # Purpose: Initialize a Marc_XML_RecordSet with      #
        #          default variables (constructor)           #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
        # Return: N/A                                        #
        # See Also: __init__ documentation in the Python     #
        #           documentaion                             #
        #----------------------------------------------------#
	def __init__(self):
                self._records = []
	
	#----------------------------------------------------#
	# Purpose: Provide a method so that this object may  #
	#          be looped over and provides the           #
	#          appropriate value when reached as an      #
	#          index                                     #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             index - The index of the object being  #
	#                     referenced                     #
	# Return: Marc_XML_Record - The record object at the #
	#                           given position           #
	# See Also: __getitem__ documentation in the Python  # 
	#           documentation                            #
	#----------------------------------------------------#
	def __getitem__(self, index):
		return self._records[index]
	
	#----------------------------------------------------#
	# Purpose: Provide functionality (answer) for when   #
	#          len(Marc_XML_RecordSet)                   #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: int - The "length" of the object           #
	# See Also: __len__ documentation in the Python      #
	#           documentation                            #
	#----------------------------------------------------#
	def __len__(self):
		return len(self._records)
	
	#----------------------------------------------------#
	# Purpose: Getter for the recordset (property) of    #
	#          the object                                #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: list - A list of all the records contained #
	#                in the data structur                #
	#----------------------------------------------------#
	@property
	def records(self):
		return self._records
	
	#----------------------------------------------------#
	# Purpose: Setter for the records (property)         #
	#          contained within the object                 #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: N/A                                        #
	#----------------------------------------------------#
	@records.setter
	def records(self):
		# TO BE IMPLEMENTED: Check if all entries are of Marc_XML_Record
		#                    type
		pass
		
	
	#----------------------------------------------------#
	# Purpose: Add a record to the recordset             #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             record - The record to be added to the #
	#                      recordset                     #
	# Return: N/A                                        #
	# Throws: TypeError - IF record isn't a              #
	#         Marc_XML_Record object                     #
	#----------------------------------------------------#
        def add_record(self, record):
		# Check that the record argument provided is an instance of 
		# Marc_XML_Record
                if isinstance(record, Marc_XML_Record):
			# Make sure that its a "valid" instance
			if record.validate():
				# Add it to the set
                        	self._records.append(record)
                else:
			# Raise a type error as they provided an incorrect type
                        raise TypeError
	
	#----------------------------------------------------#
	# Purpose: Provide a string representation of the    #
	#          object                                    #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: string - A string representation of the    #
	#                  object                            #
	# See Also: __str__ documentation in the Python      #
	#           documentation                            #
	#----------------------------------------------------@
	def __str__(self):
		# Start with an open square brace
		result_str = '['
		
		# For each record suffix a comma and space
		for record in self.records:
			result_str += str(record) + ', '
		
		# Remove the last comma and space and replace with a close 
		# square bracket
		result_str = result_str[:-2] + ']'
		
		# Return the result
		return result_str

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
			print '===================================================='
		
		# Set a attribute/property of the Marc_XML_Record to be of the 
		# name name and value of subfield.text
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
		
		# Call the method
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
			if type(return_val) == dict:
				for k,v in return_val.iteritems():
					new_return_result[k] = v
		if len(new_return_result) > 0:
			return_result = new_return_result
		#if len(return_result) == 1:
		#	return_result = return_result[0]
		
		print '[parse_record]Preparing to Return: ' + str(return_result)
		return return_result
	
	#----------------------------------------------------#
	# Purpose: Generic trigger method similar to that    #
	#          of execute or run in similar models       #
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
		
		# Give the filename the appropriate extension
		if format == 'json' and not output_file.endswith('.json'):
			# TO BE IMPLEMENTED: Strip extension if it exists
			output_file = output_file + '.json'
		
		writer = None
		if format == 'json':
			writer = Metadata_JSON_Writer()
		
		if isinstance(writer, Metadata_File_Writer):
			writer.write_to_file(output_file, self.recordset)
		
		return return_result
