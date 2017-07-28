from langid import classify
from bs4 import BeautifulSoup
import unicodecsv as csv
import requests
from termcolor import colored
import sys

importcsv= sys.argv[1]

results = {}

class Manager:

	def __init__(self):
		global results
		self.urls_list = []
		self.writer = ''

	def import_csv(self, importcsv):
		with open(importcsv, 'rb') as f:
			reader = csv.reader(f, encoding='utf-8')
			for row in reader:
				
				self.urls_list.append(row)
			print self.urls_list

	def open_book_writer(self):	
		f = open('results.csv', 'wb')
		self.writer = csv.writer(f, lineterminator='\n', encoding='utf-8')
		self.writer.writerow(('url', 'language', 'confidence'))


	def open_book_append(self):
		f = open('results.csv', 'ab') 
		self.writer = csv.writer(f, lineterminator='\n', encoding='utf-8')	

	def export(self):
		
		self.writer.writerow((results['url'], results['language'], results['confidence']))
		print colored('Exporting results', 'cyan' )



class WebExtractor:
	def __init__(self):
		global results
		self.url = ''
		self.soup= ''
		self.status = ''



	def build_url(self):
		if (self.url[:7]) == 'http://':
			print colored('URL is correct', 'green')

			return self.url
		else:
			print colored('this url is NOT invalid', 'red')
			print colored (' Correcting ...', 'cyan')
			self.url = ('http://' + self.url)
			results['url'] = self.url
			return self.url

	def get_soup(self):
		try:	
			response = requests.get(self.url)
			self.status = response.status_code
			if self.status == 200:
				print colored ('Active Host', 'green')
				html = response.text
				self.soup = BeautifulSoup(html, "html.parser")
				try:
					if self.soup.body:
						self.soup = self.soup.body.getText(separator=u' ')
					else:
						self.soup = self.soup.frameset.getText(separator=u' ')
				except:
					print colored('Don\'t have the tags searched', 'red')
				#print self.soup
				return self.soup
		except:
			print colored('Connection error', 'red')

	def get_language(self):
		language, confidence = classify(self.soup)
		results['language'] = language
		results['confidence'] = confidence
		return results



def main():

	global results
	manager = Manager()
	web_extractor = WebExtractor()
	manager.import_csv()
	count = 0
	#--------------------------------
	
	manager.open_book_writer()

	#--------------------------------
	for urls in manager.urls_list:
		for web_extractor.url in urls:
			count += 1	
			if count >= 5:
				manager.open_book_append()
			print colored("#####################   Url number -->  " + repr(count) , 'green')
			results = {'url': '', 'language': '', 'confidence': ''}
			print web_extractor.url
			web_extractor.url = web_extractor.build_url()
			print web_extractor.url 
			web_extractor.get_soup()
			print web_extractor.get_language()

	#--------------------------------
			manager.export()
			del results


if __name__== '__main__':
	main()