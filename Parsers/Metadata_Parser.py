# My Modules;
import dynamic_loader as loader
import funcs				# Requried to use some generic functions

# Load abc (Abstract Class) module
loader.load_abc()
abc = loader.abc

# Load the Metadata_Record class
loader.load_Metadata_Record()
Metadata_Record = loader.Metadata_Record

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
