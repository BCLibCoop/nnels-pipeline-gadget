#!/usr/bin/env python

import click
import os
import data_structs as structs
from Parsers.Marc_XML.Marc_XML_Parser import Marc_XML_Parser
from funcs import func_get, func_set
from rename_files import rename_files
from config import Config

actions = ['get', 'rename']

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

class MyCLI(click.MultiCommand):
	def list_commands(self, ctx):
		rv = []
		for filename in os.listdir(plugin_folder):
			if filename.endswith('.py'):
				rv.append(filename[:-3])
		rv.sort()
		return rv
	
	def get_command(self, ctx, name):
		ns = {}
		fn = os.path.join(plugin_folder, name + '.py')
		with open(fn) as f:
			code = compile(f.read(), fn, 'exec')
			eval(code, ns, ns)
		return ns['cli']

#----------------------------------------------------#
# Purpose: Provide the CLI for the generating of the #
#          dictiomary                                #
# Parameters: N/A                                    #
# Return: N/A                                        #
#----------------------------------------------------#
def generate_dictionary_cli(dictionary_format):
	# Setup the callback variables
	parser_type = {'Marc XML':Marc_XML_Parser}
	options = []
	callbacks = {}
	for k,v in parser_type.iteritems():
		options.append(k)
		callbacks[k] = v
	
	# Prompt the use to see what kind of Metadata file
	# they'd like to parse to generate the dictionary
	# After some development this might include types like
	# Marc, Marc XML, ONIX, etc...
	type = click.prompt('What type of metadata to parse', type=click.Choice(options))
	
	# Now prompt the user what they want the dictionary file
	# to be called this is partly in case they ever want to
        # reuse that dictionary file
	dictionary = click.prompt('Where (filename) should the file be stored?')
	
	# Initialize the proper parser and parse_to_file
	parser = callbacks[type]()
	output = parser.parse_to_file(dictionary, format=dictionary_format)
	
	# For the returned output lets parse it and display it
	# to the user so that they have som e idea of what is
	# happening
	#for parsed_file, parsed_values in output.iteritems():
	#	for record in parsed_values:
	#		if isinstance(record, dict):
	#			for k,v in record.iteritems():
	#				click.echo('Parsed the value ' + unicode(v) + ' for the records ' + k + ' from ' + parsed_file)
	#		else:
	#			print str(record) + ' isn\'t a dictionary'
	
	return dictionary

#----------------------------------------------------#
# Purpose: 
# Parameters: 
# Return: 
#----------------------------------------------------#
def get_records_from_dictionary(dictionary):
	# Check if the dictionary was defined
	if dictionary is None:
		# Ask if the user wants to generate a dictionary
		generate_dictionary = click.confirm('Do you neeed to generate a dictionary?')
		
		format_options = ['json', 'tabs', 'csv']
		dictionary_format = click.prompt('What format to store the dictionary in?', type=click.Choice(format_options))
		
		# Check what response was given
		if generate_dictionary:
			dictionary = generate_dictionary_cli(dictionary_format)
                else:
			# Because the user didn't specify a dictionary at
			# runtime and has said no to generating one we need to
			# ask what file they'd like to use given that we do
			# NEED one
			dictionary = click.prompt('Filename of the dictionary file to use?')
			# Acknowledge the user input so that they know whats
			# happening
			click.echo('Alright. Using %s as the dictionary' % dictionary)
	else:
		if dictionary == 'Marc_XML':
			parser = Marc_XML_Parser()
			output = parser.parse()
			
	# Load in the dictionary (wheither just generated or not)
	if not '.' in dictionary:
		if dictionary_format == 'json':
			dictionary += '.json'
		elif dictionary_format == 'tabs':
			dictionary += '.txt'
		elif dictionary_format == 'csv':
			dictionary += '.csv'
	
	with open(dictionary) as f:
		if dictionary_format == 'json':
			result = structs.json.load(f)
			records = structs.records_from_json(result)
		elif dictionary_format == 'tabs':
			header_line = f.readline()
			lines = []
			curr_line = f.readline().decode('utf-8')
			while curr_line != '':
				lines.append(curr_line)
				curr_line = f.readline().decode('utf-8')
			records = structs.records_from_tab_seperated(header_line, lines)
		elif dictionary_format == 'csv':
			header_line = f.readline()
			lines = []
			curr_line = f.readline().decode('utf-8')
			while curr_line != '':
				lines.append(curr_line)
				curr_line = f.readline().decode('utf-8')
			records = structs.records_from_csv(header_line, lines)
	return records

#----------------------------------------------------#
# Purpose: Provide the CLI for the program including #
#          triggers for applicable inputs            #
# Parameters: dictionary - The filename of the       #
#                          datastore/look up table   #
#                          dictionary to use         #
#             action - The action to be taken        #
#                      (automatically) by the script #
#             output_level - The level of output to  #
#                            provide to the user     #
# Return: N/A                                        #
#----------------------------------------------------#
@click.command(cls=MyCLI, invoke_without_command=True)
@click.option('--dictionary', '-d', default=None, help='The filename that you want to use as the datastore dictionary/look up table')
@click.option('--action', '-a', default=None, type=click.Choice(actions), help='The action you want the script to perform')
@click.option('--verbose', '-v', 'output_level', flag_value='verbose', default=True, help='Provide output to the user')
@click.option('--quiet', '-q', 'output_level', flag_value='quiet',  help='Provide minimal output to the user')
@click.pass_context
def main(ctx, dictionary, action, output_level):
	ctx.obj = {}
	ctx.obj['configs'] = Config()
	
	records = get_records_from_dictionary(dictionary)
	
	#for record in records:
	#	print unicode(record)
	
	# Check if a (sub)command was specified
	if ctx.invoked_subcommand is None:
		actions = ctx.command.list_commands(ctx)
		
		if action is None:
			# Prompt the user to see what they want to do
        		action = click.prompt('What would you like to do?', type=click.Choice(actions))
		
		# Check if the action choosen needs to be acompanied by some 
		# other arguments
		if action in actions:
			# Check if the function being called is spcifically 
			# rename
			if action == 'rename':
				# Set the records extra parameter to supply for
				# rename callback
				ctx.obj['records'] = records
				
				patterns = []
				
				use_pattern = True
				while use_pattern:
					# Ask if the user would like to use a pattern 
					# for the rename function
					use_pattern = click.confirm('Would you like to specify a file pattern?')
				
					# If they do want to 
					if use_pattern:
						patterns.append(click.prompt('What file pattern(s) would you like to use?'))
				
				# Check if the list is empty
				if patterns:
					# If the list isn't empty then we need
					# to assign it to the context objec 
					# don't bother otherwise
					ctx.obj['patterns'] = patterns
			
			# Invoke the desired callback with the additional 
			# arguments
			ctx.invoke(ctx.command.get_command(ctx, action))
		else:
			# Invoke the desired callback
			ctx.invoke(ctx.command.get_command(ctx, action))
	else:
		if ctx.invoked_subcommand == 'rename':
			ctx.obj['records'] = records

#----------------------------------------------------#
# Purpose: To provide the entry point for the CLI    #
# Parameters (Command Line) - See main (Click)       #
#                             function for details   #
# Return: N/A                                        #
#----------------------------------------------------#
if __name__ == '__main__':
        main()
