# Downloads screenshots, description, title and other details of a google play store link
from scraper import PlayStore

def main():
	package_name = str(raw_input("Enter a package name: "))
	play_store = PlayStore(package_name)	
	play_store._parse_soup()

if __name__== "__main__":
	main()

def console_entry():
	""" entry point for console scripts """
	main()

