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
        name = ''
