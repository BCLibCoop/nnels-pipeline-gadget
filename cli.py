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

#====================================================#
# Purpose: To lazily loads the "plugins" from the    #
#          commands folder for Click use (ex.        #
#          rename, etc...)                           #
# Properties: None                                   #
# Methods: list_commands - List the available        #
#                          "plugins"                 #
#          get_command - Get the desired "plugin"    #
# Superclass: Click.MultiCommand                     #
#====================================================#
class MyCLI(click.MultiCommand):
  #----------------------------------------------------#
  # Purpose: To list the available "plugins"           #
  # Parameters: self (implicit) - The instance of the  #
  #                               object the function  #
  #                               is invoked on        #
  #             ctx - The Click context thats being    #
  #                   used                             #
  # Return: A (sorted) list of the available "plugins" #
  #----------------------------------------------------#
  def list_commands(self, ctx):
    # Initialize the return list
    rv = []

    # Loop over the files in the plugin directory
    for filename in os.listdir(plugin_folder):
      # Ensure the file is a Python file
      if filename.endswith('.py'):
        # Add the file to the list
        rv.append(filename[:-3])

    # Sort the list
    rv.sort()

    # Return the list
    return rv

  #----------------------------------------------------#
  # Purpose: Get the command for the given "plugin"    #
  # Parameters: self (implicit) - The instance of the  #
  #                               object the function  #
  #                               is invoked on        #
  #             ctx - The Click context thats being    #
  #                   used                             #
  #             name - The name of the "plugin" to get #
  #                    the command from                #
  # Return: function - The function to call to run the #
  #                    command                         #
  #----------------------------------------------------#
  def get_command(self, ctx, name):
    # Initialize the return dictionary
    ns = {}

    # Add the name of the command/"plugin" the user wants to use to
    # the end of the filepath for the "plugin"/commands folder
    fn = os.path.join(plugin_folder, name + '.py')

    # Open the file
    with open(fn) as f:
      # Compile and evaluate the file
      code = compile(f.read(), fn, 'exec')
      eval(code, ns, ns)

    # Return a pointer to the newly loaded function
    return ns['cli']

#----------------------------------------------------#
# Purpose: Provide the CLI for the generating of the #
#          dictiomary                                #
# Parameters: N/A                                    #
# Return: N/A                                        #
#----------------------------------------------------#
def generate_dictionary_cli(dict_extension, dict_source):
  # Setup the callback variables
  parser_type = {'MarcXML':Marc_XML_Parser}
  options = []
  callbacks = {}
  for k,v in parser_type.iteritems():
    options.append(k)
    callbacks[k] = v

  # # Prompt the use to see what kind of Metadata file
  # # they'd like to parse to generate the dictionary
  # # After some development this might include types like
  # # Marc, Marc XML, ONIX, etc...
  # type = click.prompt('What type of metadata to parse', type=click.Choice(options))

  # # Now prompt the user what they want the dictionary file
  # # to be called this is partly in case they ever want to
  #       # reuse that dictionary file
  # dictionary = click.prompt('Where (filename) should the file be stored?')

  dict_file = 'dict' + '.' + dict_extension
  # Initialize the proper parser and parse_to_file
  parser = callbacks[dict_source]()
  output = parser.parse_to_file(dict_file, format=dict_extension)

  # For the returned output lets parse it and display it
  # to the user so that they have som e idea of what is
  # happening
  #for parsed_file, parsed_values in output.iteritems():
  #  for record in parsed_values:
  #    if isinstance(record, dict):
  #      for k,v in record.iteritems():
  #        click.echo('Parsed the value ' + unicode(v) + ' for the records ' + k + ' from ' + parsed_file)
  #    else:
  #      print str(record) + ' isn\'t a dictionary'

  return dict_file

#----------------------------------------------------#
# Purpose:
# Parameters:
# Return:
#----------------------------------------------------#
def get_records_from_dictionary(dict_options):
  # # Ask if the user wants to generate a dictionary
  # generate_dictionary = click.confirm('Do you neeed to generate a dictionary?')

  # format_options = ['json', 'tabs', 'csv']
  # dict_format = click.prompt('What format to store the dictionary in?', type=click.Choice(format_options))

  dict_source = dict_options[0]
  dict_extension = dict_options[1]

  dict_file = generate_dictionary_cli(dict_extension, dict_source)
  click.echo('Using %s.%s as the dictionary' % (dict_file, dict_extension))
  print dict_file
  # else:
  #     # Because the user didn't specify a dictionary at
  #     # runtime and has said no to generating one we need to
  #     # ask what file they'd like to use given that we do
  #     # NEED one
  #     dictionary = click.prompt('Filename of the dictionary file to use?')
  #     Acknowledge the user input so that they know whats
  #     happening

  # else:
  #   if dict_options[0] == 'Marc_XML':
  #     parser = Marc_XML_Parser()
  #     output = parser.parse()
  #   dict_format = None

  # Load in the dictionary (wheither just generated or not)
  if not '.' in dict_file:
    if dict_extension == 'json':
      dict_file += '.json'
    elif dict_extension == 'tabs':
      dict_file += '.txt'
    elif dict_extension == 'csv':
      dict_file += '.csv'

  with open(dict_file) as f:
    if dict_extension is None:
      if dict_file.endswith('.json'):
        dict_extension = 'json'
      elif dict_file.endswith('.txt'):
        dict_extension = 'tabs'
      elif dict_file.endswith('.csv'):
        dict_extension = 'csv'

    print(dict_extension)

    #Different reading methods for dict_types
    if dict_extension == 'json':
      result = structs.json.load(f)
      records = structs.records_from_json(result)
    elif dict_extension == 'tabs':
      header_line = f.readline()
      lines = []
      curr_line = f.readline().decode('utf-8')
      while curr_line != '':
        lines.append(curr_line)
        curr_line = f.readline().decode('utf-8')
      records = structs.records_from_tab_seperated(header_line, lines)
    elif dict_extension == 'csv':
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
@click.option('--dictionary', '-d', default=('MarcXML', 'json'), type=(unicode, unicode), help='The filename that you want to use as the datastore dictionary/look up table')
@click.option('--action', '-a', default="rename", type=click.Choice(actions), help='The action you want the script to perform')
@click.option('--verbose', '-v', 'output_level', flag_value='verbose', default=True, help='Provide output to the user')
@click.option('--quiet', '-q', 'output_level', flag_value='quiet',  help='Provide minimal output to the user')
@click.pass_context
def main(ctx, dictionary, action, output_level):
  ctx.obj = {}
  ctx.obj['cfg'] = Config()

  records = get_records_from_dictionary(dictionary)

  #for record in records:
  #  print unicode(record)

  # Check if a (sub)command was specified
  if ctx.invoked_subcommand is None:
    actions = ctx.command.list_commands(ctx)

    # Defaults to rename for first release
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

        # #use_pattern = True
        # while use_pattern:
        #   # Ask if the user would like to use a pattern
        #   # for the rename function
        #   use_pattern = click.confirm('Would you like to specify a file pattern?')

        #   # If they do want to
        #   if use_pattern:
        #     patterns.append(click.prompt('What file pattern(s) would you like to use?'))

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
