from urllib import urlopen
import re, os, zipfile, shutil, sys, time
from threading import Thread

global thread_count
global fail_image

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
        global fail_image

	if buffer != None:
                buffer = buffer.read()
                image=file(path, "wb")
                image.write(buffer)
                del image
        else:
                image = file(path, "wb")
                image.write(fail_image)
                del image
	
			
def manga_download(manga, chapter):
	global thread_count
        
	output_path=os.path.join(os.getcwd(), manga+" "+'{:0>3}'.format(chapter))
	
	if os.path.isdir(output_path)==False:
		os.mkdir(output_path);
	
	url = "http://www.eatmanga.com/Manga-Scan/"+manga+"/"+manga+"-"+'{:0>3}'.format(chapter)+"/page-"
        url1 = url+"1"
	#print url
	webpage = download(url1, 4)
	if webpage == None:
                print manga, chapter, "Fail"
                return
	webpage = webpage.read()
	#print len(webpage)
	
	t_page = int( re.search(r' of (\d*)', webpage).group(1) )
        #print s
	c_s = '{:0>3}'.format(chapter)	

	for i in range(1, t_page+1, 1):
		p_url = url+str(i)
		p_html = download(p_url, 4).read()
		p_string = '{:0>3}'.format(i) 
		
		img_url = re.search(r'eatmanga_image.*(http://.*eatmanga.com/mangas/.*jpg).*alt', p_html).group(1)

                ext = img_url.rsplit('.', 1)
		ext = ext[1]
		
		path=os.path.join(output_path, "ch"+c_s+"_pg"+p_string+"."+ext) 
		i_download(img_url, path)
        
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
	try:	
		j = int(sys.argv[3])
	except:
		j = i
	
	global thread_count
        global fail_image

	max_count = 32
	thread_count = 0
	
	threadlist=[]
	
	while i<=j:
		while thread_count >= max_count:
			time.sleep(5)
		t=Thread(target=manga_download, args=(manga, i))
		t.start()
		threadlist.append(t)
		i=i+1
		thread_count=thread_count+1

	for t in threadlist:
		t.join()
