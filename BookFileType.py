import abc
from Parsers.OPF_Parser import OPF_Parser

#====================================================#
# Purpose: Represent the actual type of different    #
#          types of books that may need to be        #
#          processed (ex. EPUB, MP3, DAISY, etc...)  #
# Properties: name - The name of the type            #
#             property_list - The list of POTENTIAL  #
#                             metadata avaiable for  #
#                             that type              #
#====================================================#
class BookFileType(object):
        __metaclass__ = abc.ABCMeta
	name = ''
	
	@abc.abstractmethod
	def check_extension():
		return
	
class EPUB_Type(BookFileType):
	def __init__(self):
		self.name = 'EPUB'
	
	@staticmethod
	def check_extension(extension):
		isEPUB = False
		
		if extension == 'epub':
			isEPUB = True
		
		return isEPUB
	
	def get_metadata(self, filepath):
		return_result = None
		
		opf_parser = OPF_Parser(filepath)
		return_result = opf_parser.get_metadata()
		
		return return_result

class MP3_Type(BookFileType):
	def __init__(self):
		self.name = 'MP3'
	
	@staticmethod
	def check_extension(extension):
		isMP3 = False
		
		if extension == 'mp3':
			isMP3 = True
		
		return isMP3

class DAISY_Type(BookFileType):
	def __init__(self):
		self.name = 'DAISY'
	
	@staticmethod
	def check_extension(extension):
		isDAISY = False
		
		# Because this type isn't determined by extension skip this
		
		return isDAISY
	
	def check_string(self, token):
		isDAISY = False
		
		if token.startswith('DAISY'):
			isDAISY = True
		
		return isDAISY

class DAISY202_Type(DAISY_Type):
        def __init__(self):
                self.name = 'DAISY 2.02'
	
        def check_string(self, token):
                isDAISY = False

                if super(DAISY202_Type, self).check_string(token):
                        if token.endswith('202'):
				isDAISY = True

                return isDAISY

class DAISY3_Type(DAISY_Type):
        def __init__(self):
                self.name = 'DAISY 3'

        def check_string(self, token):
                isDAISY = False

                if super(DAISY3_Type, self).check_string(token):
			if token.endswith('3'):
                        	isDAISY = True

                return isDAISY

class BookFileTypeFactory(object):
	@staticmethod
	def getExtensionType(extension):
		returnType = None
		
		for type in [EPUB_Type, MP3_Type, DAISY_Type]:
			if type.check_extension(extension):
				returnType = type()
		
		return returnType
	
	def getStringType(self, token):
		returnType = None
		
		for type in [DAISY202_Type,DAISY3_Type]:
			caller = type()
			if caller.check_string(token):
				returnType = type()
		
		return returnType
