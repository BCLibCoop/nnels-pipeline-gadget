######################################################
# Purpose: To load modules dynamically so that used  #
#          modules work properly and consistantly    #
#          across different Python installations     #
######################################################

#----------------------------------------------------#
# Purpose: To load the XML parser module dynamically #
# Parameters: N/A                                    #
# Return: Boolean - if it was successful             #
# Additional Notes: This allows classes to reference #
#                   the etree object for XML parsing #
#                   via a call to                    #
#                   <dynamic_loader>.etree           #
#----------------------------------------------------#
def load_XML_parser():
	# Boolean flag to represent if the import worked (default to False as 
	# want to assume NOT imported until know otherwise)
	success = False
	
	# Make the import global to the file and by extension accessible to 
	# other modules
	global etree
	
	try:
 		# Load the etree from/as the lxml package or module
		from lxml import etree
		
		# DEBUGGING: A print statement to allow the "user" to know 
		#            which version was imported
		#print("running with lxml.etree")
		
		# Since we've successfully imported the etree from/as the lxml 
		# package or module reset the Boolean flag to True
		success = True
	except ImportError:
		try:
    			# Load the etree from/as the xml.etree package or 
			# module (Python 2.5)
			import xml.etree.cElementTree as etree
			
			# DEBUGGING: A print statement to allow the "user" to 
			#            know which version was imported
			#print("running with cElementTree on Python 2.5+")
			
			# Since we've successfully imported the etree from/as 
			# the xml.etree package or module reset the Boolean flag
			# to True
			success = True
		except ImportError:
			try:
				# Load the etree from/as the xml.etree package 
				# or module (Python 2.5)
				import xml.etree.ElementTree as etree
				
				# DEBUGGING: A print statement to allow the 
				#            "user" to know which version was 
				#            imported
				#print("running with ElementTree on Python 2.5+")
				
				# Since we've successfully imported the etree 
				# from/as the xml.etree package or module reset 
				# the Boolean flag to True
				success = True
			except ImportError:
				try:
					# Load the etree from/as the 
					# cElementTree (normal cElementTree 
					# install)
					import cElementTree as etree
					
					# DEBUGGING: A print statement to allow 
					#            the "user" to know which 
					#            version was imported
					#print("running with cElementTree")
					
					# Since we've successfully imported the
					# etree from/as the cElementTree package
					# or module reset the Boolean flag to 
					# True
					success = True
				except ImportError:
					try:
						# Load the etree from/as the 
						# ElementTree (normal 
						# ElementTree install)
						import elementtree.ElementTree as etree
						
						# DEBUGGING: A print statement 
						#            to allw the "user" 
						#            to know which 
						#            version was 
						#            imported
					 	#print("running with ElementTree")
						# Since we've successfully 
						# imported the etree from the 
						# ElementTree package or module
						# reset the Boolean flag to True
						success = True
					except ImportError:
						
						# DEBUGGING: A print statement 
						#            to allow the "user"
						#            to know that we 
						#            couldn't seem to 
						#            import any version
						#            successfully
						print("Failed to import ElementTree from any known place")
	
	# Return the Boolean flag
	return success
