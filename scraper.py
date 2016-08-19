import re
import sys
import urllib
import os
from bs4 import BeautifulSoup


class PlayStore():
	""" Play Store class includes all methods required for scraping a valid url
		Initialized with a valid package name
	"""

	def __init__(self, package_name):		
		""" init fails on invalid package name """	
		
		self._cover_image = None
		self._description = None
		self._screenshots = None

		try:
			if (self._validate_play_store_package_name(package_name)):
				self.__package_name = package_name
				print("Initialised play store object with package name: %s" %package_name)
			else:
				print("Invlaid package name: %s" %package_name)
				sys.exit(1)
		except Exception as e:
			print(e)
			sys.exit(1)


	def _validate_play_store_package_name(self, p):
		""" validate package name string """
		regex =  "([a-z_]{1}[a-z0-9_]*(\.[a-z_]{1}[a-z0-9_]*)*)$"
		return re.match(regex, p)

	def _generate_play_store_url(self):
		""" generate google play store link for a valid package name """

		# https://play.google.com/store/apps/details?id=com.icicibank.pockets
		return ("https://play.google.com/store/apps/details?id=" + str(self.__package_name))

	def _fetch_url_content(self):
		""" fetch html content of play store link """

		url = self._generate_play_store_url()
		l = urllib.urlopen(url)
		if l.getcode() == 200:
			print("Fetched play store link successfully! (%s)" %url)
			return l.read()
		else:
			print("Error in fetching url! (%s)" %url)
			sys.exit(1)

	def _generate_soup(self):
		""" generates bs4 soup object """

		try:
			content = self._fetch_url_content()
			soup = BeautifulSoup(content, "html.parser")
		except Exception as e:
			print(e)
			sys.exit(1)
		else:
			#print("initialized soup: %s" %str(type(soup)))		
			return soup

	def _parse_soup(self):
		""" parse soup to fetch all required content and save on disk """

		soup = self._generate_soup()
		cover_image = self._fetch_cover_image(soup)
		description = self._fetch_description(soup)
		screenshots = self._fetch_screenshots(soup)

		self._cover_image = cover_image
		self._description = description
		self._screenshots = screenshots

		self._setup_folder()
		self._save_cover_image()
		self._save_screenshots()
		self._save_description()

		# print("\n\nCover Image: %s" %cover_image)
		# print("\nDescription: %s" %description)
		# print("\nScreenshots: %s" %screenshots)

	def _fetch_cover_image(self, soup):
		""" fetches cover image url """

		cover_container = soup.find_all('div', {"class": "cover-container"})
		for c in cover_container:
			cover_image = c.find_all('img', {"class": "cover-image"})			
		if len(cover_image)>0:
			return "https:" + cover_image[0]["src"]
		else:
			print("Cover Image not found!")
			return None

	def _fetch_description(self, soup):
		""" fetches description text """

		content_container = soup.find_all('div', {"class": "show-more-content text-body"})[0]
		description_container = content_container.find_all("div", {"jsname": "C4s9Ed"})
		if len(description_container)>0:
			return (description_container[0].text)
		else:
			print("Description not found!")
			return None
		
	def _fetch_screenshots(self, soup):
		""" fetches screenshots urls """

		img_containers = soup.find_all("img", {"class": "full-screenshot"})
		screenshots = []
		for i in img_containers:
			url = i.get("src", None)
			if url: url = "https:" + url; screenshots.append(url)							
		return screenshots

	def _setup_folder(self):
		""" sets up a folder with package name as folder name and deletes
		if already existing  """

		if not os.path.exists(self.__package_name):
			os.makedirs(self.__package_name)
		else:
			for root, dirs, files in os.walk(self.__package_name, topdown=False):
			    for name in files:
			        os.remove(os.path.join(root, name))
			    for name in dirs:
			        os.rmdir(os.path.join(root, name))
			

	def _download_and_save(self, url, fname):
		""" download and save image file with .png extension """
		urllib.urlretrieve(url, self.__package_name+"/"+fname+".png")

	def _save_cover_image(self):
		""" save cover image to disk """
		self._download_and_save(self._cover_image, "cover_image")

	def _save_screenshots(self):
		""" save screenshots to disk """
		i = 0
		for s in self._screenshots:			
			self._download_and_save(s, "s"+str(i))
			i += 1

	def _save_description(self):
		""" save description to a file on disk """
		f = open(self.__package_name+"/"+"desc", 'wb')
		f.write(self._description.encode("utf8"))
		f.close()

		