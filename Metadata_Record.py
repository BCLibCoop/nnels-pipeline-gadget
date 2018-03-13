DEBUG_MODE = False

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
# Superclass: object                                 #
# NOTE: Can be used as a concrete class but the      #
#       recommendation is to subclass and treat it   #
#       as an abstract class so that more specific   #
#       types of metadata might be contained (ex.    #
#       Marc_XML, etc...)                            #
#====================================================#
class Metadata_Record(object):
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
		if DEBUG_MODE:
			print '===================================================='
			print 'Call Summary for __init__ (Metadata_Record)'
			print '----------------------------------------------------'
			print 'Self: ' + str(self)
			print '===================================================='
		
		self.title = None
		self.SCN = None
	
	def _generate_new_SCN(self):
		# Create and parse a timestamp as part of new
		# SCN generation
		now = datetime.now()
		
		year = str(now.year)
		
		month = str(now.month)
		month = month.zfill(2)
		
		day = str(now.day)
		day = day.zfill(2)
		
		hour = str(now.hour)
		hour = hour.zfill(2)
		
		minute = str(now.minute)
		minute = minute.zfill(2)
		
		second = str(now.second)
		second = second.zfill(2)
		
		microsecond = str(now.microsecond)
		microsecond = microsecond.zfill(7)
		
		# Generate the entire new SCN
		newSCN = "(AutoGenerated)" + year + month + day + hour + minute + second + microsecond
		
		return newSCN
	
	#----------------------------------------------------#
	# Purpose: To validate the object (check that it     #
	#          contains both an SCN and title at minimum #
	#          and any other checks that need to occur   #
	#          to make sure its valid)                   #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked ont       #
	# Return: boolean - If this instance of              #
	#                   Metadata_Record is valid         #
	#----------------------------------------------------#
	def validate(self):
                is_valid = True

                if self.SCN is None:
                        if self.title is None:
                                is_valid = False
                        else:
                                # Generate the entire new SCN
                                newSCN = self._generate_new_SCN()

                # Return the result
                return is_valid
	
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
