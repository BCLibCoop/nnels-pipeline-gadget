try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

from ConfigParser import SafeConfigParser
import subprocess

args = ['find', '.', '-name', '*.xml'] #, '-print0']
proc = subprocess.Popen(args, stdout=subprocess.PIPE)
stdout, stderr = proc.communicate()
lines = stdout.decode('ascii').splitlines()
for line in lines:
	with035 = {}
	
	print "Parsing " + line
	tree = etree.parse(line)
	root = tree.getroot()
	for record in root:
		for field in record:
			if field.get("tag") == '035':
				for code in field:
					with035[code.text] = record
	print with035
#parser = SafeConfigParser()
#parser.read('The Legacy-metadata.ini')
#print parser.get('The Legacy', 'title')
