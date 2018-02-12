from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('The Legacy-metadata.ini')
print parser.get('The Legacy', 'title')
