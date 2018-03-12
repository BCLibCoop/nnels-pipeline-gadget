import platform

#====================================================#
# Purpose; Provide an object that can be passed      #
#          around for the purposes of providing      #
#          program wide configurations               #
# Properties: HOST_OS - 
#             DEBUG_MODE - 
# Methods: 
# Superclass: object                                 #
#====================================================#
class Config(object):
	#----------------------------------------------------#
	# Purpose: Initialize the Config object with the     #
	#          default variables (constructor)           #
	# Parameters: self (implictt) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def __init__(self):
		self._config_setter_callbacks = {}
		self._config_getter_callbacks = {}
		self._DEBUG_MODES = ['none', 'status', 'stacktrace']
		self.DEBUG_MODE = 'none'
	
	#----------------------------------------------------#
	# Purpose: Return the DEBUG MODE configuration       #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	# Return: string - The DEBUG MODE the configuration  #
	#                  object is set to                  #
	#----------------------------------------------------#
	@property
	def DEBUG_MODE(self):
		return self._DEBUG_MODE
	
	#----------------------------------------------------#
	# Purpose: Setter for the DEBUG_MODE property        #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             mode - The mode to set the DEBUG_MODE  #
	#                    property to                     #
	# Return: N/A                                        #
	# Raises: TypeError - The mode provided isn't a      #
	#                     valid mode                     #
	#----------------------------------------------------#
	@DEBUG_MODE.setter
	def DEBUG_MODE(self, mode):
		# Make sure that the mode provided is a valid mode
		if mode in self._DEBUG_MODES:
			self._DEBUG_MODE = mode
		else:
			raise TypeError
		
	#----------------------------------------------------#
	# Purpose: Getter for the HOST_OS property           #
	# Parameter: self (implicit) - The instance of the   #
	#                              object the fuction    #
	#                              is invoked on         #
	# Return: string - The HOST OS of the current        #
	#                  configuration object              #
	#----------------------------------------------------#
	@property
	def HOST_OS(self):
		return platform.system()
	
	#----------------------------------------------------#
	# Purpose:
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             name - The name of the property to map #
	#                    to the setter                   #
	#             callback - The callback for setting    #
	#                        the nameed property of the  #
	#                        configuration object        #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def register_config_setter(self, name, callback):
		self._config_setter_callbacks[name] = callback
	
	#----------------------------------------------------#
	# Purpose: 
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             name - The name of the property to map #
	#                    to the getter                   #
	#             callback - The callback for getting    #
	#                        the named property of the   #
	#                        configuration object        #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def register_config_getter(self, name, callback):
		self._config_getter_callbacks[name] = callback
	
	#----------------------------------------------------#
	# Purpose: To prcess incoming property assignments   #
	#          (ex. configs.my_property = ... WITHOUT    #
	#          brackets) before their passed along to    #
	#          the default functionality so that if a    #
	#          custom setter was registered for the      #
	#          property we can redirect to the           #
	#          appropriate rather than applying the      #
	#          default behavour                          #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             name - The name of the property the    #
	#                    "user" is attempting to set     #
	#             value - The value the "user" is        #
	#                     attempt to assign to the       #
	#                     property                       #
	# Return: N/A                                        #
	#----------------------------------------------------#
	def __setattr__(self, name, value):
		# Flag for when the value is set (so that checks are 
		# independent)
		was_set = False
		
		# Ignore all "private" variables (starts with a underscore)
		if not name.startswith('_'):
			# Check if there is a custom setter for the given 
			# property
			if name in self._config_setter_callbacks:
				# Call the appropriate callback
				self._config_setter_callbacks[name](self, value)
				
				# Set the flag
				was_set = True
		
		# Check the flag
		if not was_set:
			# Perform the default behavour (call superclass version)
			super(Config, self).__setattr__(name, value)
	
	#----------------------------------------------------#
	# Purpose: To process incoming property references   #
	#          (ex. configs.my_property WITHOUT brackets #
	#          ) before their passed along to the        #
	#          default functionality so that if a custom #
	#          getter was registered for the property we #
	#          can redirect to the approprate function   #
	#          rather than getting an error              #
	# Parameters: self (implicit) - The instance of the  #
	#                               object the function  #
	#                               is invoked on        #
	#             name - The name of the property to be  #
	#                    retrieved                       #
	# Return: The value for the property including the   #
	#         return of the registered callback if       #
	#         applicable otherwise the value of the      #
	#         property                                   #
	#----------------------------------------------------#
	def __getattribute__(self, name):
		# Set the return variable initially to None/Null
		return_result = None
		
		# Ignore all "private" variables (starts with a undrscore)
		if not name.startswith('_'):
			# Check if there is a custom getter for the given 
			# property
			if name in self._config_getter_callbacks:
				return_result = self._config_getter_callbacks[name](self)
		# Check if the return variable 
		if return_result is None:
			# Perform the default behavour of the superclass
			return_result = super(Config, self).__getattribute__(name)
		# Return the result
		return return_result	
