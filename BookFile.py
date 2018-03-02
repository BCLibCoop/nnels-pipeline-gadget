from BookFileType import BookFileType
import data_structs as structs

#====================================================#
# Purpose: Represent a BookFile object within the    #
#          Python scripts                            #
# Properties: fullpath - The full file path to the   #
#                        file                        #
#             filename - The filename of the book    #
#                        file (No directory          #
#                        information)                #
#             SCN - The SCN of the book the file     #
#                   represents                       #
#             title - The title of the book the file #
#                     represents                     #
#             type = The type of book it is (ex.     #
#                    EPUB, MP3, DAISY, etc...)       #
#====================================================#
class BookFile(object):
	fullpath = ''   # The full filepath to the book file
	filename = ''	# The filename (No directory information)
	
	#----------------------------------------------------#
	# Purpose: Constructor for the BookFile object       #
	# Parameters: type - The "type" of BookFile object   #
	#                    to create (ex. EPUB vs MP3 vs   #
	#                    DAISY vs ...)                   #
	# Return: N/A (Constructor)                          #
	#----------------------------------------------------#
	def __init__(self):
		self.SCN = None
		self.title = None
		self._type = None
	
	#----------------------------------------------------#
	# Purpose: Getter for the object's type property (   #
	#          Needed as a result of having a custom     #
	#          setter for validation)                    #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being called on   #
	# Return: The type property of the object            #
	#----------------------------------------------------#
	@property
	def type(self):
		return self._type
	
	#----------------------------------------------------#
	# Purpose: Custom setter for the object's type       #
	#          property because needs to validate that   #
	#          it is a valid type                        #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being called on   #
	#             newType - The value proposed to be the #
	#                      type                          #
	# Return: N/A (Setter)                               #
	#----------------------------------------------------#
	@type.setter
	def type(self, newType):
		if isinstance(newType, BookFileType):
			self._type = newType
		else:
			raise TypeError('BookFileType required')
	
	def __str__(self):
		result_str = '{'
		
		attrs = vars(self)
		for k,v in attrs.iteritems():
			if k.startswith('_'):
				result_str += k[1:] + ':' + str(v) + ', '
			else:
				result_str += k + ':' + str(v) + ', '
		
		result_str = result_str[:-2] + '}'
		result_str = unicode(result_str)
		
		return result_str
