import dynamic_loader as loader
loader.load_XML_parser()
etree = loader.etree
def parse(file):
	fd = open(file)
	d = fd.read()
	xmp_start = d.find('<x:xmpmeta')
	xmp_end = d.find('</x:xmpmeta')
	xmp_str = d[xmp_start:xmp_end+12]
	root = etree.fromstring(xmp_str)
	for child in root:
		print child.tag[child.tag.find('}') + 1:] + ':' 
		for k,v in child.attrib.iteritems():
			print '\t' + k[k.find('}') + 1:] + ': ' + v
		print '\tParnet: ' + root.tag[root.tag.find('}') + 1:]
		for grandchild in child:
			print grandchild.tag[grandchild.tag.find('}') + 1:]
			for k,v in grandchild.attrib.iteritems():
				print '\t' + k[k.find('}') + 1:] + ': ' + v
			print '\tParent: ' + child.tag[child.tag.find('}') + 1:]
			for great_grandchild in grandchild:
				print great_grandchild.tag[great_grandchild.tag.find('}') + 1:] 
				for k,v in great_grandchild.attrib.iteritems():
					print '\t' + k[k.find('}') + 1:] + ': ' + v
				print '\tParent: ' + grandchild.tag[grandchild.tag.find('}') + 1:]
				for great_great_grandchild in great_grandchild:
					print great_great_grandchild.tag[great_great_grandchild.tag.find('}') + 1:] 
					for k,v in great_great_grandchild.attrib.iteritems():
						print '\t' + k[k.find('}') + 1:] + ': ' + v
					print'\tParent: ' + great_grandchild.tag[great_grandchild.tag.find('}') + 1:]
					for great_great_great_grandchild in great_great_grandchild:
						print great_great_great_grandchild.tag[great_great_great_grandchild.tag.find('}') + 1:]
						for k,v in great_great_great_grandchild.attrib.iteritems():
							print '\t' + k[k.find('}') + 1:] + ': ' + v
						print '\tParent: ' + great_great_grandchild.tag[great_great_grandchild.tag.find('}') + 1:]


if __name__ == '__main__':
	parse('Back_9781459802896/01 Back - Introduction.mp3')
