from Metadata_File_Writer import Metadata_File_Writer

class Metadata_JSON_Writer(Metadata_File_Writer):
	#----------------------------------------------------#
        # Purpose: Add the quotes needed for the JSON        #
        #          formating of the output                   #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked  on       #
        #             input - The input the process and      #
        #                     produce the desired output     #
        # Return: String - A string representing the input   #
        #                  properly quoted for JSON          #
        # NOTE: This method starts with a underscore (_)     #
        #       which means its intended to be a private     #
        #       method for use by the class only             #
        #----------------------------------------------------#
        def _add_json_quotes(self, input):
                # Split the input into tokens by colon(s)
                sub_tokens = input.split(':')

                # Make sure there is an appropriate amount of tokens
                if len(sub_tokens) != 2:
                        raise TypeError

                # Add the quotes and reconstruct the string
                returnValue = ''
                returnValue += '"' + sub_tokens[0].strip() + '"'
                returnValue += ':'
                returnValue += '"' + sub_tokens[1].strip() + '"'

                # Return the result
                return returnValue

        #----------------------------------------------------#
        # Purpose: Process each entry string for the JSON    #
        #          this includes making sure correct quoting #
        #          and adding commas as appropriate          #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
        #             tokens - The array of json tokens      #
        #             index - The index within the tokens    #
        #                     array to process               #
        # Return: string - The processed token               #
        # NOTE: This method starts with a underscore (_)     #
        #       which means its intended to be a private     #
        #       method for use by the class only             #
        #----------------------------------------------------#
        def _process_json_entry(self, token, is_first=False, is_last=False):
                returnValue = token

                if is_first:
                        returnValue = returnValue[1:]
                if is_last:
                        returnValue = returnValue[:-1]

                returnValue = self._add_json_quotes(returnValue)

                return returnValue
	
	#----------------------------------------------------#
        # Purpose: Builds the proper string for an entry in  #
        #          a record (ex. title in a record)          #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
        #             tokens - The array of JSON tokens      #
        #             index - The index of the element in    #
        #                     the tokens array being         #
        #                     "reconstructed"                #
        # Return: string - The processed line                #
        # NOTE: This method starts with a underscore (_)     #
        #       which means its intended to be a private     #
        #       method for use by the class only             #
        #----------------------------------------------------#
        def _build_json_entry(self, token, is_first=False, is_last=False):
                processed_record = self._process_json_entry(token, is_first, is_last)

                if not is_last:
                        processed_record += ', '

                return processed_record

        #----------------------------------------------------#
        # Purpose: Build a JSON record within the entire     #
        #          JSON file                                 #
        # Parameters: self (implicit) - The instance of the  #
        #                               object the function  #
        #                               is invoked on        #
        #             record - The record we're creating a   #
        #                      JSON representation of        #
        # Return: string - The valid JSON string             #
        #                  representation of the record      #
        # NOTE: This method starts with a underscore (_)     #
        #       which means its intended to be a private     #
        #       method for use by the class only             #
        #----------------------------------------------------#
        def _build_json_record(self, record):
                # Tokenize the record by comma (,)
                tokens = record.split(',')

                # Do the converstion/processing and reconstruct by returning
                # results
                returnValue = '{'
                for index in range(0, len(tokens)):
                        curr_token = tokens[index]
                        is_first = index == 0
                        is_last = index == len(tokens) - 1
                        returnValue += self._build_json_entry(curr_token, is_first, is_last)
                returnValue += '}'

                return returnValue
	
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
        def _write_record_to_file(self, fp, record, is_last=False):
                record_str = unicode(record)

                record_str = self._build_json_record(record_str)

                fp.write(record_str.encode('utf-8'))

                if not is_last:
                        fp.write(',\n')

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
                        is_last = record_index == len(recordset) - 1
                        self._write_record_to_file(fp, record, is_last)
	
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
                # Write to the file
                with open(output_file, 'w+') as f:
                        f.write('{\n"collection":[\n')
                        self._write_records_to_file(f, recordset)
                        f.write(']\n}')
