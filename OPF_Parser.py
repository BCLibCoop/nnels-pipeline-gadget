from Metadata_Parsers import Metadata_XML_Parser

import dynamic_loader as loader

loader.load_subprocess()
subprocess = loader.subprocess

loader.load_XML_parser()
etree = loader.etree

class OPF_Parser(Metadata_XML_Parser):
	def __init__(self, epub_file):
		opf_file = self.get_opf_name(epub_file)
		self.ingest_opf(epub_file, opf_file)
	
	def get_opf_name(self, epub_file):
		# List the files in the EPUB archieve using the unzip utility
		unzip_args = ['unzip', '-l', epub_file]
		unzip_proc = subprocess.Popen(unzip_args, stdout=subprocess.PIPE)
		
		# Extract the .opf file from the list provided by the prevous 
		# command
		grep_args = ['grep', '-o', "\\b[^\\s-]*\\.opf\\b"]
		grep_proc = subprocess.Popen(grep_args, stdin=unzip_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		# Allow unzip_proc to receive a SIGPIPE if grep_proc exits
		unzip_proc.stdout.close()
		
		# Actually perform the commands
		out, err = grep_proc.communicate()
		
		# Extract the .opf name from the result
		output_parts = out.split(' ')
                filepath_opf = output_parts[len(output_parts) - 1][:-1]
                
		# Return the filepath
		return filepath_opf
		
	def ingest_opf(self, epub_file, opf_file):
		unzip_args = ['unzip', '-p', epub_file, opf_file]
		unzip_proc = subprocess.Popen(unzip_args, stdout=subprocess.PIPE)
		
		out, err = unzip_proc.communicate()
		
		self.root = etree.fromstring(out)
	
	def _recordset_set(self, value):
		self._recordset = value
	def find_parsable_files(self):
		pass
	@property
	def record_tag(self):
		return 'metadata'
	def parse_meta_tag(self, tag_elem):
		print etree.tostring(tag_elem)
	def parse_title_tag(self, title_elem):
		print 'The title is: ' + title_elem.text
	def parse_record(self, record):
		self.find_tag('meta', self.parse_meta_tag, curr_elem=record)
		self.find_tag('title', self.parse_title_tag, curr_elem=record)
	
	def get_metadata(self):
		return_value = {}
		self.find_records(None, curr_elem=self.root)
		#for child in self.root:
		#	curr_tag = child.tag[child.tag.find('}') + 1:]
		#	if curr_tag == 'metadata':
		#		for grandchild in child:
		#			curr_tag = grandchild.tag[grandchild.tag.find('}') + 1:]
		#			if curr_tag == 'meta':
		#				value = grandchild.get('content')
		#				if grandchild.get('content').startswith('id'):
		#					value = self.get_manifest_entry(grandchild.get('content'))
		#				return_value[grandchild.get('name')] = value
		#			else:
		#				return_value[curr_tag] = grandchild.text
		#
		# Return the result
		#return return_value
	
	def get_manifest_entry(self, id):
		return_value = None
		
		for child in self.root:
			curr_tag = child.tag[child.tag.find('}') + 1:]
			if curr_tag == 'manifest':
				for grandchild in child:
					curr_tag = grandchild.tag[grandchild.tag.find('}') + 1:]
					if curr_tag == 'item':
						if grandchild.get('id') == id:
							return_value = grandchild.get('href')
		
		#
		return return_value
