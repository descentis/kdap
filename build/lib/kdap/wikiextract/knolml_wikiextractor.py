import os


class QueryExecutor:
	def __init__(self, ):
		### Always Runs in Quiet Mode
		### For information about logs, specify
		##  in the log file.

		## query instruction build
		## stores last query executed, this is also used in runQuery and callQuery
		self.query = ''

		## show in json format
		self.json = False

		## show in html format we can use only one format at a time
		self.html = False

		## number of processes
		self.processes = 1

		## directory for extracted files
		## default value as text (no flags needed for this)
		self.output = 'text'

		## maximum bytes per output file
		self.bytes = 1000000

		## output file compression using bzip
		self.compress = False

		## preserve links or not
		self.links = False

		## preserve section or not
		self.sections = False

		## preserve list or not
		self.lists = False

		## accepted namespaces in links comma separated
		self.namespaces = ''

		## use or create file containing templates
		self.templates = ''

		## do not expand templates
		self.do_not_expand_templates = False

		## Minimum expanded text length required to write document
		self.min_text_length = 0

		## Include or exclude specific categories from the dataset.
		self.path_of_category_file = ''

		## Remove pages from output that contain disabmiguation markup
		self.filter_disambig_pages = False

		## comma separated list of tags that will be dropped, keeping their content
		self.ignored_tags = ''

		## comma separated list of elements that will be removed from the article text
		self.discard_elements = ''

		## Preserve tables in the output article text
		self.keep_tables = False

		## will save log information in this file
		self.log_file = ''

		## generate file from this plain text by appending dummy tags
		## Because the wikiExtractor works only with those tags
		self.text = ''


	## sets OutputFile Directory Name (used in query building stage)
	def setOutputFileDirectoryName(self, outputDirectory = 'text'):
		self.output = outputDirectory

	## getter function for output file directory
	def getOutputFileDirectoryName(self):
		return self.output

	#setter function
	## flips json and html
	def setJson(self):
		self.json = True
		self.html = False

	#setter function
	## flips json and html
	def sethtml(self):
		self.html = True
		self.json = False


	#setter function
	def setNumberOfProcesses(self, numOfProcesses):
		self.processes = numOfProcesses

	## getter function
	def getNumberOfProcesses(self, numOfProcesses):
		return self.numOfProcesses

	#setter function
	def setNumberOfBytes(self, numOfBytes):
		self.bytes = numOfBytes

	## getter function
	def getNumberOfBytes(self):
		return self.bytes

	#setter function
	def setCompress(self, compressValue):
		self.compress = compressValue

	## getter function
	def getCompressValue(self):
		return self.compress

	#setter function
	def setPreserveLinks(self, preserveValue):
		self.links = preserveValue

	## getter function
	def getPreserveValue(self):
		return self.links

	#setter function
	def setPreserveSections(self, preserveValue):
		self.sections = preserveValue

	## getter function
	def getPreserveSections(self):
		return self.sections

	#setter function
	def setPreserveLists(self, preserveValue):
		self.lists = preserveValue

	## getter function
	def getPreserveLists(self):
		return self.lists

	#setter function
	def setNamespaces(self, ns_list_comma_Separated):
		self.namespaces = ns_list_comma_Separated

	## getter function
	def getNamespaces(self):
		return self.namespaces

	#setter function
	def setTemplates(self, template):
		self.templates = template

	## getter function
	def getTemplates(self):
		return self.templates

	#setter function
	def setMinTextLength(self, min_length):
		self.min_text_length = min_length

	## getter function
	def getMinTextLength(self):
		return self.min_text_length

	#setter function
	def setPathOfCategoryFile(self, file_path):
		self.path_of_category_file = file_path

	## getter function
	def getPathOfCategoryFile(self):
		return self.path_of_category_file

	#setter function
	def setDisambiguationPages(self, setValue):
		self.filter_disambig_pages = setValue

	## getter function
	def getDisambiguationPages(self):
		return self.filter_disambig_pages

	#setter function
	def setIgnoredTagsCommaSeparated(self, comma_separated_tags):
		self.ignored_tags  = comma_separated_tags

	## getter function
	def getIgnoredTagsCommaSeparated(self):
		return self.ignored_tags

	#setter function
	def setDiscardElementsCommaSeparated(self, comma_separated_elements):
		self.discard_elements = comma_separated_elements

	## getter function
	def getDiscardElementsCommaSeparated(self):
		return self.discard_elements

	#setter function
	def setKeepTables(self, keepValue):
		self.keep_tables = keepValue

	## getter function
	def getKeepTables(self):
		return self.keep_tables

	#setter function
	def setLogFileName(self, log_file_name):
		self.log_file = log_file_name

	## getter function
	def getLogFileName(self):
		return self.log_file

	#setter function
	def setDoNotExpandTemplates(self, do_not_expand_templates_value):
		self.do_not_expand_templates = do_not_expand_templates_value

	## getter function
	def getDoNotExpandTemplates(self):
		return self.do_not_expand_templates

	## write in file method
	## intermediate method (you don't need to do it)
	def writeInFile(self, text_value):
		with open('input.xml', 'w') as file:
			file.write(text_value)

	## set text value
	## appends prefix and suffix to text and sets them to
	## the internal variable for further processing
	def setTextValue(self, text_value):

		prefix = """<page>
    <id></id>
    
      <text xml:space="preserve" bytes="1182"> """

		suffix = """</text>
     
  </page> """

		self.text = prefix + text_value + suffix
		self.writeInFile(self.text)


	## gives text value 
	def getTextValue(self):
		return self.text





	## querybuilder method
	## used to build query using presetted descriptors
	## Note: queries always run in --silent mode
	def buildQuery(self):
		cmd = 'python WikiExtractor.py input.xml '# --processes 4 --links --output lol --quiet'

		if(self.json):
			cmd += '--json '
		if(self.html):
			cmd += '--html '

		cmd += '--output ' + self.output + ' '

		cmd += '--processes ' + str(self.processes) + ' '

		if(self.bytes != 1000000):
			cmd += '--bytes ' + str(self.bytes) + ' '

		if(self.compress):
			cmd += '--compress '

		if(self.links):
			cmd += '--links '

		if(self.sections):
			cmd += '--sections '

		if(self.lists):
			cmd += '--lists '

		if(self.namespaces != ''):
			cmd += '--namespaces ' + str(self.namespaces) + ' '

		if(self.templates != ''):
			cmd += '--templates ' + str(self.templates) + ' '

		if(self.do_not_expand_templates):
			cmd += '--no-templates '

		if(self.path_of_category_file != ''):
			cmd += '--filter_category '

		if(self.filter_disambig_pages):
			cmd += '--filter_disambig_pages '

		if(self.ignored_tags != ''):
			cmd += '--ignored_tags ' + str(self.ignored_tags)

		if(self.discard_elements != ''):
			cmd += '--discard_elements ' + str(self.discard_elements) + ' '

		if(self.keep_tables):
			cmd += '--keep_tables '

		if(self.log_file != ''):
			cmd += '--log_file ' + str(self.log_file) + ' '


		cmd += '--quiet'

		self.query = cmd

		#print(cmd)
		#os.system(cmd)

	## callquery method
	## uses system call to run the query command
	def callQuery(self):
		os.system(self.query)

	## queryrunner method
	## builds the query using query text and then runs it
	def runQuery(self):
		self.buildQuery()
		self.callQuery()

	## returns the result in pure text form
	## result is coming from file from self.output/AA/wiki_00 file
	## wiki_00 is generated using wikiExtractor
	def result(self):
		final_output = ''
		file_path = self.output + "/AA/wiki_00"
		with open(file_path) as file:
			final_output = file.read()
			return final_output


##############################################################################################

                                             ### Testing ###
'''
input_text = """
==Impact==
[[Image:DCP 7760.JPG|thumb|right|Tornado damage near a forested area]]
The tornado took a path through [[Rockland County, New York|Rockland]], [[Westchester County, New York|Westchester]], and [[Fairfield County, Connecticut|Fairfield]] counties, downing or uprooting thousands of trees and damaging several structures, including significant structural damage to the California Closest Warehouse. Six minor injuries were also reported. In all, the tornado inflicted $12.1&amp;nbsp;million (2006&amp;nbsp;[[United States Dollar|USD]]; $12.9&amp;nbsp;million 2008 USD) in damage.&lt;ref name="MSSum"/&gt;

Minor damage was reported in Rockland County. One dock and one boat were damaged by the tornado.&lt;ref name="MSSum"/&gt; After crossing the [[Hudson River]], the tornado entered Westchester County, where the worst of the damage took place. It struck the town of [[Sleepy Hollow, New York|Sleepy Hollow]], damaging roofs and tearing the siding off numerous homes and businesses.&lt;ref name="MSSum"/&gt; A 10&amp;nbsp;foot (3&amp;nbsp;m) tall stained-glass window in the St. Teresa of Avila Church was shattered.&lt;ref name="USAT"/&gt; Afterwards, the town of [[Pocantico Hills, New York|Pocantico Hills]] was struck as the tornado intensified to F2 intensity. Several trees were uprooted and two barns were destroyed. The California Closet Warehouse suffered severe structural damage; two concrete walls were destroyed.&lt;ref name="MSSum"/&gt; An interior staircase, which employees used as a shelter, collapsed causing four injuries. Concrete blocks from the building were blown about, some of which struck cars in a nearby parking lot.&lt;ref name="USAT"/&gt; A nearby [[Comfort Inn]] had part of its roof torn off.&lt;ref name="WESH"&gt;{{cite web| date=2006-7-13|author=Associated Press| title=Tornado Rips Through Suburban New York| publisher=[[Internet Broadcasting|Internet Broadcasting Systems, Inc]]| accessdate=2008-11-30|url=http://www.wesh.com/news/9510358/detail.html}}&lt;/ref&gt; After a [[tornado warning]] was issued, a school near the warehouse was evacuated.&lt;ref name="NYTimes"&gt;{{cite news| author=Lisa W. Foderaro| date=2006-07-13| title=Tornado in Westchester Tosses Around Trees and Damages Property| work=[[The New York Times]]| accessdate=2008-11-30|url=http://www.nytimes.com/2006/07/13/nyregion/13weather.html?pagewanted=print}}&lt;/ref&gt; 

[[File:Westchester Tornado damage1.JPG|thumb|left|An area where numerous trees were knocked down, the white tubes support saplings being grown to re-populate the affected area.]]
As the tornado crossed [[New York State Route 9A]], it picked up a state trooper car and flipped it several times before it fell to the ground; the officer inside suffered only minor injuries.&lt;ref name="USAT"/&gt; Moving towards the east-northeast, the tornado struck the towns of [[Mount Pleasant, New York|Mount Pleasant]] and [[Hawthorne, New York|Hawthorne]], damaging numerous trees and causing minor structural damage.&lt;ref name="MSSum"/&gt; Damage along the [[Saw Mill River Parkway]] prompted officials to shut down a section of the highway near Mount Pleasant.&lt;ref name="CNN"&gt;{{cite news| author= Rose Arce | date=2006-07-13| title=Tornado hits north of Manhattan, Winds damage store, close highway; no serious injuries reported| publisher=[[CNN|Cable News Network]]| accessdate=2008-11-30|url=http://www.cnn.com/2006/WEATHER/07/12/ny.tornado/index.html
}}&lt;/ref&gt;  Trees fell on streets and railroad tracks, halting [[Metro-North Railroad]] service and creating major traffic delays.&lt;ref name="NYTimes"/&gt; After passing by the [[Kensico Reservoir]] in [[Valhalla, New York|Valhalla]], the tornado crossed into [[Connecticut]],&lt;ref name="MSSum"/&gt; where it knocked down numerous power lines, cutting power to about 10,000 residences in the county.&lt;ref name="USAT"/&gt; In all, six people sustained minor injuries and damages amounted to $10.1&amp;nbsp;million (2006 USD).&lt;ref name="Tornado2"/&gt;

The weakening tornado ended its duration in Fairfield County, Connecticut in the town of [[Greenwich, Connecticut|Greenwich]]. Thousands of trees were either uprooted or snapped along the tornado's {{convert|2|mi|km|abbr=on}} path through the state. Minor damage was inflicted upon several structures.&lt;ref name="MSSum"/&gt; The tornado left 1,700 residences in Greenwich without power and blocked six roads. Most of the damage was concentrated to the northwestern corner of the town.&lt;ref name="NYTimes2"&gt;{{cite news| author=Avi Salzman and Anahad O'Connor| date=2006-07-16| title=The Week; Rare Tornado Snaps Trees and Power Lines| publisher=The New York Times| accessdate=2008-12-01|url=http://query.nytimes.com/gst/fullpage.html?res=9F04E2D91F30F935A25754C0A9609C8B63}}&lt;/ref&gt; Damages in the state totaled to  $2&amp;nbsp;million (2006 USD).&lt;ref name="Tornado3"/&gt;

==External links==
*[http://wcbstv.com/video/?id=89570@wcbs.dayport.com Doppler Radar image of the tornadic supercell nearing Tarrytown]
*[http://www.youtube.com/watch?v=_fLZLrZAB0M Video of the tornado damage in Westchester]
*[http://wcbstv.com/topstories/Tornado.Tornado.Warning.2.236314.html WCBS article and video of damage/press reports of the tornado]

{{featured article}}
[[Category:F2 tornadoes]]
[[Category:New York tornadoes]]
[[Category:Connecticut tornadoes]]
[[Category:Tornadoes of 2006]]
[[Category:2006 in the United States]]


"""

qe = QueryExecutor()
qe.setOutputFileDirectoryName('lol')
#qe.sethtml()
qe.setNumberOfProcesses(5)
qe.setNumberOfBytes(2000000000)
qe.setTextValue(input_text)
#print(qe.getTextValue())
#qe.setCompress(True)
#qe.setPreserveLinks(True)
qe.runQuery()
print(qe.result())
'''
