from urllib2 import urlopen
import re, os, zipfile, shutil, sys, time
from threading import Thread
import imghdr
from bs4 import BeautifulSoup

global thread_count

def download(url, retries):
        tries = 0
        while tries < retries:
                try:
                        content = urlopen(url)
                        return content
                except:
                        tries = tries + 1
        return None 

def image_download(url, path):
	buffer=download(url, 4)
	if buffer != None:
                buffer = buffer.read()
                image=file(path, "wb")
                image.write(buffer)
                del image
		ext = imghdr.what(path)
		os.rename(path, path+"."+ext)
	
	else:
		print "Error"


#download manga-chapter from a given url
#eg - http://starkana.com/manga/S/Sun-ken_Rock/chapter/12
def ch_download(url):
	global thread_count
	chapter = url.rsplit('/', 1)[1]
	manga = url.rsplit('/', 3)[1]
	output_path = os.path.join(os.getcwd(), manga+" "+'{:0>3}'.format(chapter))
	if os.path.isdir(output_path)==False:
		os.mkdir(output_path);

	webpage = download(url+"?scroll", 4).read()
	soup = BeautifulSoup(webpage)
	img_list = soup.find_all("img", class_="dyn")
	if len(img_list) != 0:
		#download
		for i in range(0, len(img_list)):
			img_url = img_list[i]['src']
			img_path = os.path.join(output_path, "ch" + '{:0>3}'.format(chapter)+ "pg" + '{:0>3}'.format(i+1))
			image_download(img_url, img_path)
	
	else:
		#sequential download
		webpage = download(url, 4).read()
		soup = BeautifulSoup(webpage)
		t_pages = int( soup.find(id='reader-nav').strong.text )
		for i in range(1, t_pages+1):
			webpage = download(url+"/"+str(i), 4).read()
			soup = BeautifulSoup(webpage)
			img_url = soup.find(class_='dyn')['src']
			img_path = os.path.join(output_path, "ch" + '{:0>3}'.format(chapter)+"pg"+"{:0>3}".format(i))
			image_download(img_url, img_path)


	zip = zipfile.ZipFile(output_path+".cbz", 'w')
	for root, dirs, files in os.walk(output_path):
                for f in files:
                        absfile=os.path.join(root, f)
	 		zip.write(absfile, f)

	shutil.rmtree(output_path)
        thread_count = thread_count - 1
	return


if __name__=='__main__':
	manga=sys.argv[1]
	i=int(sys.argv[2])
	j = int(sys.argv[3])
	
	global thread_count
	max_count = 32
	thread_count = 0
	threadlist=[]
	
	while i<=j:
		while thread_count >= max_count:
			time.sleep(5)
		url = "http://www.starkana.com/manga/"+manga[0]+"/"+manga+"/chapter/"+str(i)
		t=Thread(target=ch_download, args=(url,))
		t.start()
		threadlist.append(t)
		i=i+1
		thread_count=thread_count+1

	for t in threadlist:
		t.join()
