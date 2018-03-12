from Marc_XML_Record import Marc_XML_Record

#====================================================#
# Purpose: A collection data structure to ensure     #
#          proper typing of entries within the       #
#          sturcture as well as provide any          #
#          additional processing or functionality as #
#          requried                                  #
# Propterties: records - The records held within the #
#                        data structure              #
# Methods: __init__ - The constructor for the        #
#                     object. Does some simple       #
#                     initalizations to avoid        #
#                     unknown variable errors        #
#          __getitem__ - A overriden method so that  #
#                        if "duck typing" occurs     #
#                        during a for loop the       #
#                        object provides the proper  #
#                        response                    #
#          records (getter) - A simple getter method #
#                             for the records        #
#                             property               #
#          records (setter) - A simple setter method #
#                             for the records        #
#                             property               #
#          add_record - To add a record to the data  #
#                       structure                    #
#          __str__ - Provides a string               #
#                    representation of the object    #
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
		# Initialize an empty list variable
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
	#          contained within the object               #
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
	
	#----------------------------------------------------#'
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
