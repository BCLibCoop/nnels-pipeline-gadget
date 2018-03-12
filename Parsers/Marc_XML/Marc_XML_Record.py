from Metadata_Record import Metadata_Record

#====================================================#
# Purpose: A more specific concrete class for Marc   #
#          XML records                               #
# Properties: title (Metadata_Record) - See Docs     #
#             SCN (Metadata_Record) - See Docs       #
# Superclass: Metadata_Record                        #
#====================================================#
class Marc_XML_Record(Metadata_Record):
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
                super(Marc_XML_Record, self).__init__()

        @property
        def SCN(self):
                return self._SCN

        @SCN.setter
        def SCN(self, value):
                if value is not None:
                        if '(' in value:
                                value = value[value.find(')') + 1:]
                                value = value.strip()

                self._SCN = value

        @property
        def title(self):
                return self._title

        @title.setter
        def title(self, value):
                if value is not None:
                        # Remove special characters
                        specialchars = [",", ":", ".", "'", "?", "&", "/"]

                        for char in specialchars:
                                value = value.replace(char, "")

                        # Strip any extranous whitespace
                        value = value.strip()

                        # Underscore remaining whitespace
                        value = value.replace(" ", "_")

                self._title = value

        #def __str__(self):
        #       return super(Marc_XML_Record, self).__str__()
