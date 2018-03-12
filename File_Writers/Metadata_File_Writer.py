import dynamic_loader as loader
loader.load_abc()
abc = loader.abc

class Metadata_File_Writer(object):
        __metaclass__ = abc.ABCMeta

        #----------------------------------------------------#
        # Purpose: The entry/top level function that         #
        #          triggers or performs the writes of the    #
        #          provided records to the file itself       #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
        #             output_file - The file to put the      #
        #                           output in                #
        #             recordset - The set of records to be   #
        #                         written to the file        #
        # Return: N/A                                        #
        #----------------------------------------------------#
        @abc.abstractmethod
        def write_to_file(self, output_file, recordset):
                raise NotImplementedError
