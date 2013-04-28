from urllib import urlopen
import re, os, zipfile, shutil, sys, time
from threading import Thread

thread_count = 0
max_count = 300

def i_download(url, path):
	tries=1
	while tries!=0 and tries<10:
		try:
			webpage=urlopen(url).read()
			u=re.search(r'onerror.*src=["\'](http.*\.jpg)["\']', webpage).group(1)
			buffer=urlopen(u).read()
			image=file(path, "wb")
			image.write(buffer)
			del image
			return
		except:
			tries=tries+1
	
			
def manga_download(manga, chapter):
	global thread_count
	output_path=os.path.join(os.getcwd(), manga+" "+str(chapter)) 
	
	if os.path.isdir(output_path)==False:
		os.mkdir(output_path);
	
	b_url="http://www.mangafox.me/manga/"+manga+"/c"+str(chapter)+"/"
	
	tries=1
	while tries!=0 and tries<=10:
		try:
			webpage=urlopen(b_url+"1.html").read()
			s=re.search(r'of ([\d]+)', webpage).group(1)
			l=len(s)
			pages=int(s)
			
			threadlist=[]
			for i in range(1, pages+1):
				url=b_url+str(i)+".html"
				p="0"*(l-len(str(i)))+str(i)
				path=os.path.join(output_path, p+".jpg")
				t=Thread(target=i_download, args=(url, path))
				t.start()
				threadlist.append(t)
				
			for t in threadlist:
				t.join()
				
			zip = zipfile.ZipFile(output_path+".cbz", 'w')
			for root, dirs, files in os.walk(output_path):
				for f in files:
					absfile=os.path.join(root, f)
					zip.write(absfile, f)

			shutil.rmtree(output_path)
			thread_count=thread_count-30
			return
					
		except:
			tries=tries+1
			
	shutil.rmtree(output_path)
	print "Fail", manga, chapter
	return
			
			
if __name__=='__main__':
	thread_count=0
	manga=sys.argv[1]
	i=int(sys.argv[2])
	threadlist=[]
	while i<=int(sys.argv[3]):
		while thread_count >= max_count:
			time.sleep(5)
		t=Thread(target=manga_download, args=(manga, i))
		t.start()
		threadlist.append(t)
		i=i+1
		thread_count=thread_count+30
		
	for t in threadlist:
		t.join()