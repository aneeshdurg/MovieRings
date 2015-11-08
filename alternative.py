from PIL import Image
from math import sqrt
import os
import pygame
import subprocess
import re
# from decimal import Decimal
def fulldisplay(img):
	pygame.init()
	SIZE = [1380, 850]
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption("Displaying frame: "+img)
	image=pygame.image.load(img+".jpg")
	screen.blit(image, (0, 0))
	pygame.display.flip()
	raw_input()
	pygame.display.quit()
	pygame.quit()
	return 0	
def menu():
	movielist=[name for name in os.listdir('.') if os.path.isdir(name) and not name==".git"]
	pygame.init()
	SIZE = [1380, 850]
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption("Menu")
	font=pygame.font.Font(None,30)
	i=0
	flag=False
	while True:
		if flag:
			break
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				exit()
			elif event.type==pygame.MOUSEBUTTONDOWN:
				x, y=pygame.mouse.get_pos()	
				if x<SIZE[0]*0.25:
					i-=1
					i=i if i>=0 else len(movielist)+i
					
				elif x>SIZE[0]*0.75:
					i+=1
					i=i if i<len(movielist) else i-len(movielist)
					
				else:
					flag=True
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			exit()			
		movie=movielist[i]
		os.chdir(os.getcwd() + '/' + movie + '/')
		if os.path.exists("RESULT.jpg"):
			img=pygame.image.load("RESULT.jpg") 
	   		img=pygame.transform.scale(img, (SIZE[0], SIZE[1]))
	   		screen.blit(img, (0, 0))
	   		
		else:
			screen.fill((0, 0, 0))
			error=font.render("Click here to render now!", 1, (255, 255, 255))
			screen.blit(error, (SIZE[0]/2-200, SIZE[1]/2))
	  	title=font.render(movie, 1,(255,255,255))
		screen.blit(title, (5, 10))
		pygame.display.flip()

		os.chdir('..')
	pygame.display.quit()
	pygame.quit()					
	return movie	
						

def drawPatterns(frameAvg, movie, flag):
	frameid=""
	if flag:
		##Reading file
		frameAvg = []
		temp2 = []
		foo = open("index.txt", "r")
		temp = foo.readlines()
		foo.close()
		for i in xrange(len(temp) / 3):
			frameAvg.append([temp[3 * i], temp[(3 * i) + 1], temp[(3 * i) + 2]]) 	
	else:
		##Writing to file
		foo = open("index.txt", "w")
		for i in xrange(len(frameAvg)):
			for j in xrange(3):		
				foo.write(str(frameAvg[i][j]))
				foo.write("\n")
		foo.close()	
	done=False
	#Initializing pygame
	pygame.init()
	SIZE = [1380, 850]
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption(movie)
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True 
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			done=True
		
		x, y=pygame.mouse.get_pos()
		r=int(sqrt(((SIZE[0]/2)-x)*((SIZE[0]/2)-x)+((SIZE[1]/2)-y)*((SIZE[1]/2)-y)))
		if r>len(frameAvg):
			frameid=""
		else:
			frameid=str(r-1)
		if len(frameid)<3:
			for i in xrange(3-len(frameid)):
				frameid="0"+frameid
		#print frameid+".jpg"		
		if not os.path.exists(frameid+".jpg"):
			frameid=""
			#while True:
			
				#pygame.display.flip()
				# for event in pygame.event.get():
				# 	if event.type == pygame.MOUSEBUTTONUP:
				# 		break
		screen.fill((0, 0, 0))		
		#Drawing circles using the average color of each frame
		for i in xrange(len(frameAvg)):
			r, b, g=(int(frameAvg[len(frameAvg)-1-i][0]), int(frameAvg[len(frameAvg)-1-i][1]), int(frameAvg[len(frameAvg)-1-i][2]))
			color=(r, b, g)
			pygame.draw.circle(screen, color, [SIZE[0] / 2, SIZE[1] / 2], len(frameAvg)-i)
		if not frameid=="":
			pygame.display.set_caption("Displaying frame "+frameid+" of "+movie)
			img=pygame.image.load(frameid+".jpg") 
			img = pygame.transform.scale(img, (SIZE[0]/4, SIZE[1]/4))
			screen.blit(img,(x, y-SIZE[1]/4))
		else:
			pygame.display.set_caption(movie)
		if pygame.mouse.get_pressed()[0]:
			pygame.display.quit()
			pygame.quit()
			fulldisplay(frameid)
			pygame.init()
			SIZE = [1380, 850]
			screen = pygame.display.set_mode(SIZE)
			pygame.display.set_caption(movie)	
			# ravg, bavg, gavg=0, 0, 0
			# for i in xrange(len(frameAvg)):
			# 	ravg+=int(frameAvg[i][0])
			# 	bavg+=int(frameAvg[i][1])
			# 	gavg+=int(frameAvg[i][2])
			# ravg/=len(frameAvg)	
			# bavg/=len(frameAvg)
			# gavg/=len(frameAvg) 
			#screen.fill((0, 0, 0))
		pygame.display.flip()

	#ensures that RESULT has the avg background
	pygame.display.set_caption(movie)
	ravg, bavg, gavg=0, 0, 0
	for i in xrange(len(frameAvg)):
		ravg+=int(frameAvg[i][0])
		bavg+=int(frameAvg[i][1])
		gavg+=int(frameAvg[i][2])
	ravg/=len(frameAvg)	
	bavg/=len(frameAvg)
	gavg/=len(frameAvg) 
	screen.fill((ravg, bavg, gavg))	
	for i in xrange(len(frameAvg)):
		r, b, g=(int(frameAvg[len(frameAvg)-1-i][0]), int(frameAvg[len(frameAvg)-1-i][1]), int(frameAvg[len(frameAvg)-1-i][2]))
		color=(r, b, g)
		pygame.draw.circle(screen, color, [SIZE[0] / 2, SIZE[1] / 2], len(frameAvg)-i)
	pygame.display.flip()
	pygame.image.save(screen, "RESULT.JPG")
	pygame.display.quit()
	pygame.quit()


def get_video_length(path):
	#process = subprocess.Popen(['ffmpeg', '-i', "\""+path+"\""], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	os.system('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "'+path+'">>duration.txt')
	#stdout, stderr = process.communicate()
	foo = open("duration.txt", "r")
	temp = foo.readline()
	temp=temp.rsplit('.',1)[0]
	temp=int(temp)
	return temp

movielist=[name for name in os.listdir('.') if os.path.isdir(name)]
#menu()
#Getting movie name:
suggestions=[]
while True:
	flag = False
	movie=menu()
	if movie=="quit":
		break
	#movie = raw_input("Enter Movie Name ('list' for all available movies): ")
	if len(suggestions)>0 and movie.isdigit():
		movie=suggestions[int(movie)-1]

	os.system('cls' if os.name == 'nt' else 'clear')
	if movie == "list":
		counter=1
		for name in movielist:
			if not(name.startswith('.')):
				print str(counter)+"\t" + name
				suggestions.append(name)	
				counter+=1
		continue	
	if os.path.exists(movie) and os.path.isdir(movie):
		suggestions=[]
		#Changing Direcotry and getting file names:
		os.chdir(os.getcwd() + '/' + movie + '/')
		if os.path.exists("index.txt") and not os.stat("index.txt").st_size == 0:
			flag = True
			
		if flag:
			drawPatterns([], movie, flag)
			os.chdir('..')	
			continue	
		frameAvg = []

		moviefile = ""
		for name in os.listdir('.'):
			#print name
			if name.startswith(movie) and not name.endswith('.jpg'):
				moviefile = name
		duration = get_video_length(moviefile)
		#duration = os.system("ffmpeg -i file.flv 2>&1 | grep \"Duration\"| cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, \":\"); split(A[3], B, \".\"); print 3600*A[1] + 60*A[2] + B[1] }'")
		frames=0
		if duration==0:
			frames=0.0167
		else:
			frames = 400.0/duration 
		files=[name for name in os.listdir('.') if os.path.isfile(name) and name.endswith('.jpg')]
		if len(files) <= 1:
			os.system("ffmpeg -i \"" + moviefile + "\" -r " + str(frames) + " -s 1380x850 -f image2 %03d.jpg")
			files=[name for name in os.listdir('.') if os.path.isfile(name) and name.endswith('.jpg')]
		for name in files:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ("proccessing frame " +name[:-4] + " of " + files[len(files)-1][:-4])
			im = Image.open(name)
			pix = im.load()
			x, y = im.size 
			RED_VALS = []
			BLUE_VALS = []
			GREEN_VALS =[]
			#ALPHA_VALS = []
			avgRed = 0
			avgBlue = 0
			avgGreen = 0
			#avgAlpha = 0
			for i in xrange(100):
				for j in xrange(100):
					#print pix.getpixels((i, j))
					#raw_input()
					tempR, tempB, tempG = pix[int(i * 13.8), int(j*8.5)]
					RED_VALS.append(tempR)
					BLUE_VALS.append(tempB)
					GREEN_VALS.append(tempG)
					#ALPHA_VALS.append(tempA)
			for i in xrange(10000):
				avgRed += RED_VALS[i]
				avgBlue += BLUE_VALS[i]
				avgGreen += GREEN_VALS[i]
				#avgAlpha += ALPHA_VALS[i]

			avgRed /= 10000	
			avgBlue /= 10000
			avgGreen /= 10000
			#avgAlpha /= 10000
			frameAvg.append([avgRed, avgBlue, avgGreen])
		drawPatterns(frameAvg, movie, flag)	
		os.chdir('..')	
		continue
	else:
		for name in os.listdir('.'):
			if name.startswith(movie) or movie in name:
				suggestions.append(name)
		if not len(suggestions) == 0:
			print "Movie not found! Did you mean: "
			counter=1
			for suggestion in suggestions:
				print (str(counter)+"\t" + suggestion)	
				counter+=1	
		else:
			print "Movie not found! (Enter 'list' for list of valid names)"		
		continue
