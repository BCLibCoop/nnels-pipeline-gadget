from Metadata_File_Writer import Metadata_File_Writer

class Metadata_CSV_Writer(Metadata_File_Writer):
	#----------------------------------------------------#
        # Purpose: Write a individual record to the output   #
        #          file                                      #
        # Parameters: self (implicit) - The insanfce of the  #
        #                               object the function  #
        #                               is invoked on        #
        #             fp - The file pointer/object that can  #
        #                  be wrote to                       #
        #             record - The record (object) being     #
        #                      written out                   #
        #             is_last - Boolean if it is the last    #
        #                       entry (for comma suffix)     #
        #----------------------------------------------------#
        def _write_record_line_to_file(self, fp, record):
		record_str = ''
		
		keep_writing = True
                # Loop over properties of the record profided
                for k in vars(record):
                        if isinstance(vars(record)[k], list):
				keep_writing = False
				for entry in vars(record)[k]:
					record_copy = record
					setattr(record_copy, k, entry)
					self._write_record_line_to_file(fp, record_copy)
			else:
				if keep_writing:
					record_str += unicode(vars(record)[k]) + ','
		
		if record_str != '':
                	fp.write(record_str.encode('utf-8'))
			fp.write('\n')
	
	def _write_header_line_to_file(self, fp, header_names):
		header_line = ''
		
		for header_name in header_names:
			header_line += header_name + ','
		
		fp.write(header_line.encode('utf-8'))
		fp.write('\n')
		
		
        #----------------------------------------------------#
        # Purpose: To write the records contained in the     #
        #          recordset property of this instance into  #
        #          a file                                    #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the funtion   #
        #                               is invoked on        #
        #             fp - The file pointer/object that can  #
        #                  be wrote to                       #
        #             format - The format being writen       #
        # Return: N/A                                        #
        # NOTE: This method starts with a underscore (_)     #
        #       which means its intended to be a private     #
        #       method for use by the class only             #
        #----------------------------------------------------#
        def _write_records_to_file(self, fp, recordset):
                for record_index in range(0, len(recordset)):
                        record = recordset[record_index]
                        self._write_record_line_to_file(fp, record)
	
	#----------------------------------------------------#
        # Purpose: Write the provided recordset out to a     #
	#          JSON file                                 #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
        #             output_file - The filename (including  #
        #                           path) of the file to     #
        #                           output to (preferablly   #
        #                           without a file           #
        #                           extensions but...)       #
        #             recordset - The records to be written  #
	#                         to the file                #
        # Return: N/A                                        #
        #----------------------------------------------------#
        def write_to_file(self, output_file, recordset):
                print 'Staring to write to ' + output_file
		# Write to the file
                with open(output_file, 'w+') as f:
			headers = vars(recordset[0]).keys()
			for index in range(0, len(headers)):
				headers[index] = headers[index].replace('_', '')
			print 'Writing headers ' + str(headers)
			self._write_header_line_to_file(f, headers)
			print 'Writing records'
			self._write_records_to_file(f, recordset)
