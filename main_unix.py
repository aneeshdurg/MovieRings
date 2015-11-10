from PIL import Image
from math import sqrt
import os
import pygame
import subprocess
import re
from decimal import Decimal


def drawRings(frameAvg, movie, flag):
	for name in os.listdir('.'):
			#print name
			if name.startswith(movie) and not name.endswith('.bmp'):
				moviefile = name
	dur = get_video_length(moviefile)
	totalMinute, totalSecond = divmod(dur, 60)
	totalHour, totalMinute = divmod(totalMinute, 60)
	frameID=""
	if flag:
		##Reading file
		frameAvg = []
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
	saveImg = True
	#Initializing pygame
	pygame.init()
	SIZE = [1380, 850]
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption(movie)
	

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True 
		#Fill screen with black
		screen.fill((0, 0, 0))
		#Draw Circles
		for i in xrange(len(frameAvg)):
			r, b, g=(int(frameAvg[len(frameAvg)-1-i][0]), int(frameAvg[len(frameAvg)-1-i][1]), int(frameAvg[len(frameAvg)-1-i][2]))
			color=(r, b, g)
			pygame.draw.circle(screen, color, [SIZE[0] / 2, SIZE[1] / 2], len(frameAvg)-i)
		#Save rings to "RESULT.BMP"	
		if saveImg:
				pygame.image.save(screen, "RESULT.bmp")
				saveImg = not saveImg
		#Get Mouse Position
		x, y=pygame.mouse.get_pos()
		#Get color of position
		#mouseColor = screen.get_at((x, y))
		#Calculate Radius and Frame
		r=int(sqrt(((SIZE[0]/2)-x)*((SIZE[0]/2)-x)+((SIZE[1]/2)-y)*((SIZE[1]/2)-y)))
		if (r - 1) > len(frameAvg):		#If outside rings, frame is null
			frameID=""
		else:
			frameID=str(r-1)
		if len(frameID) < 3:
			for i in xrange(3-len(frameID)):
				frameID="0"+frameID		
		if not os.path.exists(frameID+".bmp"):
			frameID=""
		#Increase current circle radius
		
		#Draw Frame		
		if not frameID=="":
			frameDuration = (int(frameID) * dur)/len(frameAvg)
			frameMinute, frameSecond = divmod(frameDuration, 60)
			frameHour, frameMinute = divmod(frameMinute, 60)
			pygame.display.set_caption("[" + str("%d:%02d:%02d" % (frameHour, frameMinute, frameSecond)) + "]" + "  of  " + "[" + str("%d:%02d:%02d" % (totalHour, totalMinute, totalSecond)) + "]")
			img=pygame.image.load(frameID+".bmp") 
			#img = pygame.transform.scale(img, (700, 350))
			img = img.convert()
			#img.set_alpha(243)
			screen.blit(img,(x, y))
		else:
			pygame.display.set_caption(movie)
		pygame.display.flip()
	pygame.display.quit()
	pygame.quit()


def get_video_length(path):
	process = subprocess.Popen(['ffmpeg', '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
	hours = Decimal(matches['hours'])
	minutes = Decimal(matches['minutes'])
	seconds = Decimal(matches['seconds'])
	total = 0
	total += 60 * 60 * hours
	total += 60 * minutes
	total += seconds
	return total
	
movielist=[name for name in os.listdir('.') if os.path.isdir(name)]
#Getting movie name:
suggestions=[]
while True:
	flag = False
	movie = raw_input("Enter Movie Name ('list' for all available movies): ")
	if len(suggestions) > 0 and movie.isdigit():
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
			drawRings([], movie, flag)
			os.chdir('..')	
			continue	
		frameAvg = []

		moviefile = ""
		for name in os.listdir('.'):
			#print name
			if name.startswith(movie) and not name.endswith('.bmp'):
				moviefile = name

		duration = get_video_length(moviefile)
		fps = 410 / duration
		fps = round(fps, 2)
		files=[name for name in os.listdir('.') if os.path.isfile(name) and name.endswith('.bmp')]
		if len(files) <= 1:
			os.system("ffmpeg -i \"" + moviefile + "\" -r " + str(fps) + " -s 700x350 -f image2 %03d.bmp")
			files=[name for name in os.listdir('.') if os.path.isfile(name) and name.endswith('.bmp')]
		for name in files:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ("proccessing frame " +name[:-4] + " of " + files[len(files)-1][:-4])
			im = Image.open(name)
			pix = im.load()
			x, y = im.size 
			RED_VALS = []
			BLUE_VALS = []
			GREEN_VALS =[]
			avgRed = 0
			avgBlue = 0
			avgGreen = 0
			#avgAlpha = 0
			for i in xrange(200):
				for j in xrange(200):
					tempR, tempB, tempG = pix[int(i * 3.5), int(j * 1.75)]
					RED_VALS.append(tempR)
					BLUE_VALS.append(tempB)
					GREEN_VALS.append(tempG)
			for i in xrange(10000):
				avgRed += RED_VALS[i]
				avgBlue += BLUE_VALS[i]
				avgGreen += GREEN_VALS[i]
			avgRed /= 10000	
			avgBlue /= 10000
			avgGreen /= 10000
			frameAvg.append([avgRed, avgBlue, avgGreen])
		drawRings(frameAvg, movie, flag)	
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
