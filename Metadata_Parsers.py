#====================================================#
# Purpose: A generic data structure to hold          #
#          information found in each metadata record #
# Properties: title - The title of the book the      #
#                     metadata record describes (    #
#                     Required field of all metadata #
#                     types)                         #
#             SCN - The XCN of the book the metadata #
#                   record describes (Required field #
#                   of all metadata types)           #
# NOTE: Can be used as a concrete class but the      #
#       recommendation is to subclass and treat it   #
#       as an abstract class so that more specific   #
#       types of metadata might be contained (ex.    #
#       Marc_XML, etc...)                            #
#====================================================#
class Metadata_Record(objec):
        def __init__(self):
                self.title = None
                self.SCN = None

#====================================================#
# Purpose: Provide an abstract base class for        #
#          metadata parsers for the purposes of      #
#          subtype polymorphism                      #
# Properties: recordset (abstract) - All subclasses  #
#                                    should have     #
#                                    some form of    #
#                                    recordset data  #
#                                    structure to    #
#                                    hold the        #
#                                    records         #
#====================================================#
class Metadata_Parser(object):
        @property
        def recordset(self):
                raise NotImplementedError

#====================================================#
# Purpose: A more specific concrete class for Marc   #
#          XML records                               #
# Properties: title (Metadata_Record) - See Docs     #
#             SCN (Metadata_Record) - See Docs       #
#====================================================#
class Marc_XML_Record(Metadata_Record):
        def __init__(self):
                super(Metadata_Record, self).__init__())

class Marc_XML_RecordSet(object):
        def __init__(self):
                self._records = []
	
	@property
	def records(self):
		return self._records
	
	@records.setter
	def records(self):
		# TO BE IMPLEMENTED
		# Check if all entries are of Marc_XML_Record type
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
                if isinstance(record, Marc_XML_Record):
                        self._records.append(reord)
                else:
                        raise TypeError

#====================================================#
# Purpose: Provide a concreate implementation of the $
#          metadata parser abstract class for the    #
#          specific purpose of parsing Marc XML      #
#          files                                     #
# Properties: recordset (Metadata_Parser - See Docs  #
#====================================================#
class Marc_XML_Parser(Metadata_Parser):
        def __init__(self):
                self.recordset = Marc_XML_RecordSet()
