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
	
	url = "http://www.starkana.com/manga/"+manga[0]+"/"+manga+"/chapter/"+str(chapter)+"?scroll"
        
	#print url
	webpage = download(url, 4)
	if webpage == None:
                print manga, chapter, "Fail"
                return
	webpage = webpage.read()
	#print len(webpage)

	s=re.findall(r'http://manga\.starkana\.com.*[(jpg)(png)]', webpage)
        #print s
	page = 1        
	c_s = '{:0>3}'.format(chapter)	

	for u in s:
		p_s = '{:0>3}'.format(page) 
		
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
	j=int(sys.argv[3])

	global thread_count

        global fail_image
        fail_image = download("http://www.failfunnies.com/28/images/roomate-of-fail.jpg", 4)
        fail_image = fail_image.read()

	max_count = 32
	thread_count = 0
	
	threadlist=[]
	
	while i<=j:
                #manga_download(manga, i)
                #i = i+1

		while thread_count >= max_count:
			time.sleep(5)
		t=Thread(target=manga_download, args=(manga, i))
		t.start()
		threadlist.append(t)
		i=i+1
		thread_count=thread_count+1

	for t in threadlist:
		t.join()
