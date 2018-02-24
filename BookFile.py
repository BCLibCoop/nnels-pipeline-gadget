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
		self._SCN = None
		self._title = None
		self._type = None
	
	#----------------------------------------------------#
	# Purpose: Getter for the object's SCN property (    #
	#          Needed as a result of having a custom     #
	#          setter for validation)                    #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being called on   #
	# Return: The SCN property of the object             #
	#----------------------------------------------------#
	@property
	def SCN(self):
		return self._SCN
	
	#----------------------------------------------------#
	# Purpose: Custom setter for the object's SCN        #
	#          property because need to validate it      #
	#          against the "database"                    #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being called on   #
	#             newSCN - The value proposed to be the  #
	#                      SCN                           #
	# Return: N/A (Setter)                               #
	#----------------------------------------------------#
	@SCN.setter
	def SCN(self, newSCN):
		if structs.hasSCN(newSCN):
			self._SCN = newSCN
	
	#----------------------------------------------------#
	# Purpose: Getter for the object's title property (  #
	#          Needed as a result of having a custom     #
	#          setter for validation)                    #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being called on   #
	# Return: The title property of the object           #
	#----------------------------------------------------#
	@property
	def title(self):
		return self._title 
	
	#----------------------------------------------------#
	# Purpose: Custom setter for the object's title      #
	#          property because need to validate it      #
	#          against the "database"                    #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is being called on   #
	#             newTitle - The value proposed to be    #
	#                        the title                   #
	# Return: N/A (Setter)                               #
	#----------------------------------------------------#
	@title.setter
	def title(self, newTitle):
		if structs.hasTitle(newTitle):
			if self.SCN is None or self.SCN == structs.getSCN_fromTitle(newTitle):
				self._title = newTitle
	
	#----------------------------------------------------#
	# Purpose: Getter for the object's type property (  #
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
