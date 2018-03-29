from Metadata_Parser import Metadata_Parser

import dynamic_loader as loader
loader.load_abc()
abc = loader.abc
loader.load_XML_parser()
etree = loader.etree

import os.path

DEBUG_MODE = True
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
		if DEBUG_MODE:
			print '===================================================='
                        print 'Call Summary for __init__ (Metadata_XML_Parser) '
                        print '----------------------------------------------------'
                        print 'Self: ' + str(self)
                        print 'XML File List: ' + str(XML_files)
                        print '===================================================='
		
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
		if DEBUG_MODE:
			print '===================================================='
                        print 'Call Summary for file_to_tree (Metadata_XML_Parser) '
                        print '----------------------------------------------------'
                        print 'Self: ' + str(self)
                        print 'XML File: ' + str(XML_file)
                        print '===================================================='
		
		tree = etree.parse(XML_file)
		self.trees[XML_file] = tree.getroot()
		
		# Create a version where all namespaces are removed
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
		if DEBUG_MODE:
			print '===================================================='
                        print 'Call Summary for files_to_trees (Metadata_XML_Parser) '
                        print '----------------------------------------------------'
                        print 'Self: ' + str(self)
                        print 'File List: ' + str(file_list)
                        print '===================================================='
		
		# Loop over the files in the list
		for XML_file in file_list:
			if os.path.isfile(XML_file):
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
		check_attr_args = {
			'attrs':desired_attr_dict,
			'callback':callback,
			'callback_args':callback_args
		}
		
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
	
	def _remove_empty_from_result(self, input):
		if DEBUG_MODE:
			print '===================================================='
                        print 'Call Summary for _remove_empty_from_result (Metadata_XML_Parser) '
                        print '----------------------------------------------------'
                        print 'Self: ' + str(self)
                        print 'Input: ' + str(input)
                        print '===================================================='
		return_result = input
		
		# Check that the returned rsults are not empty and are of the 
		# expected type
		if return_result and isinstance(return_result, list):
			return_result = filter(None, return_result)
		
		return return_result
	
	def _remove_duplicates_or_encapsulated(self, input):
		if DEBUG_MODE:
			print '===================================================='
                        print 'Call Summary for _remove_duplicates_or_encapsulatted (Metadata_XML_Parser) '
                        print '----------------------------------------------------'
                        print 'Self: ' + str(self)
                        print 'Input: ' + str(input)
                        print '===================================================='
		
		#return_result = set(val for dic in input for val in dic.values())
		
		#
		
		return input	
		#return return_result
	
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
		
		return_result = self._remove_empty_from_result(return_result)
		return_result = self._remove_duplicates_or_encapsulated(return_result)
		#
		# If there is only a single entry then assign the variable to
		# that (rather than having a needless list with one element)
		if return_result:
			if len(return_result) == 1:
				return_result = return_result[0]
		
		# Return the result
		return return_result
