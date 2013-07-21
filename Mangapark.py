from urllib import urlopen
import re, os, zipfile, shutil, sys, time
from threading import Thread

def download(url, retries):
        tries = 0
        while tries < retries:
                try:
                        content = urlopen(url)
                        return content
                except:
                        tries = tries + 1
        return None 

def i_download(url, path):
	buffer=download(url, 4)
        buffer = buffer.read()
        image=file(path, "wb")
        image.write(buffer)
        del image
			
def manga_download(manga, chapter, chapter_url):
	output_path=os.path.join(os.getcwd(), manga+" "+'{:0>3}'.format(chapter))
	if os.path.isdir(output_path)==False:
		os.mkdir(output_path);
	url = chapter_url       
	webpage = download(url, 4)
	if webpage == None:
                print manga, chapter, "Fail"
                return
	webpage = webpage.read()
	s = re.findall(r'href="http.*jpg"', webpage)
	page = 1        
	c_s = '{:0>3}'.format(chapter)	

	for u in s:
		p_s = '{:0>3}'.format(page) 
		u = re.search(r'http.*jpg', u).group(0)
                ext = u.rsplit('.', 1)
		ext = ext[1]
		
		path=os.path.join(output_path, "ch"+c_s+"_pg"+p_s+"."+ext) 
		i_download(u, path)
		page = page + 1
        
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
	html = urlopen("http://www.mangapark.com/manga/"+manga).read()
	b_url = "http://www.mangapark.com"
	while i<=j:
		while thread_count >= max_count:
			time.sleep(5)
			
		i_url = b_url + re.search(r'/manga/.*/c'+str(i)+'/all', html).group(0)
		t=Thread(target=manga_download, args=(manga, i, i_url))
		t.start()
		threadlist.append(t)
		i=i+1
		thread_count=thread_count+1

	for t in threadlist:
		t.join()

