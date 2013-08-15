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
        print "download_error -", url
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


#download manga-chapter from a given url
#eg - http://mangapark.com/manga/Pretty_Face/c10/1
def ch_download(url):
	#print url
	global thread_count
	chapter = url.rsplit('/', 2)[1][1:]
	#print chapter
	manga = re.search(r'manga/([a-zA-Z-_]*)/', url).group(1)
	#print manga
	output_path = os.path.join(os.getcwd(), manga+" "+'{:0>3}'.format(chapter))
	#print output_path
	if os.path.isdir(output_path)==False:
		os.mkdir(output_path)
	
	url = url.rsplit('/', 1)[0]+"/all"
	#print url
	webpage = download(url, 4).read()
	#print len(webpage)
	soup = BeautifulSoup(webpage)
	img_list = soup.find_all(class_="img-link")
	#print len(img_list)

	#download
	for i in range(0, len(img_list)):
		img_url = img_list[i].img['src']
		img_path = os.path.join(output_path, "ch" + '{:0>3}'.format(chapter)+ "pg" + '{:0>3}'.format(i+1))
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
	manga = ""
	i = 0
	j = -1
	
	#print len(sys.argv)

	if len(sys.argv) == 4:
		manga=sys.argv[1]
		i=int(sys.argv[2])
		j = int(sys.argv[3])
	
	if len(sys.argv) == 3:
		manga = sys.argv[1]
		i = int(sys.argv[2])
		j = i
	
	url_list = []
	global thread_count
	max_count = 32
	thread_count = 0
	threadlist=[]
	
	#add chapter urls of the range of chapters
	while i<=j:
		url = "http://www.mangapark.com/manga/"+manga+"/c"+str(i)+"/1"
		url_list.append(url)
		i=i+1
	
	if len(sys.argv) == 2:
		url = sys.argv[1]
		webpage = download( url, 4 ).read()
		soup = BeautifulSoup( webpage )
		list = soup(text = "1")
		flag = 0
		if len(list[0].parent['href'][1:].split('/')) == 4:
			flag = 1
		for a in list:
			url = a.parent['href'][1:]
			if flag == 1:
				parts = len(url.split('/'))
				if parts == 4:
					url_list.append("http://www.mangapark.com/"+url)
				else:
					break
			else:
				url_list.append("http://www.mangapark.com/"+url)

	for u in url_list:
		while thread_count >= max_count:
			time.sleep(5)
		t = Thread(target=ch_download, args=(u,))
		t.start()
		threadlist.append(t)
		thread_count = thread_count + 1
	
	for t in threadlist:
		t.join()
