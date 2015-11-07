from PIL import Image
import os
import pygame
import subprocess
import re
from decimal import Decimal

def drawRings(frameAvg, movie, flag):
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
			
	#Initializing pygame
	pygame.init()
	SIZE = [1380, 850]
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption(movie)

	#Drawing circles using the average color of each frame
	for i in xrange(len(frameAvg)):
		r, b, g=(int(frameAvg[i][0]), int(frameAvg[i][1]), int(frameAvg[i][2]))
		color=(r, b, g)
		pygame.draw.circle(screen, color, [SIZE[0] / 2, SIZE[1] / 2], 1 * (len(frameAvg)) + 1 - 1 * (i + 1))
	pygame.display.flip()

	pygame.image.save(screen, "RESULT.JPG")


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
while True:
	flag = False
	movie = raw_input("Enter Movie Name ('list' for all available movies): ")
	os.system('cls' if os.name == 'nt' else 'clear')
	if movie == "list":
		for name in movielist:
			if not(name.startswith('.')):
				print "\t" + name	
		continue	
	if os.path.exists(movie) and os.path.isdir(movie):
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
			if name.startswith(movie) and not name.endswith('.jpg'):
				moviefile = name
		duration = get_video_length(moviefile)
		frames = 410 / duration
		files=[name for name in os.listdir('.') if os.path.isfile(name) and name.endswith('.jpg')]
		if len(files) <= 1:
			os.system("ffmpeg -i " + moviefile + " -r " + str(frames) + " -s 100x100 -f image2 %03d.jpg")
		for name in files:
			#os.system('cls' if os.name == 'nt' else 'clear')
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
					tempR, tempB, tempG = pix[i, j]
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
		drawRings(frameAvg, movie, flag)	
		os.chdir('..')	
		continue
	else:
		suggestions=[]
		for name in os.listdir('.'):
			if name.startswith(movie) or movie in name:
				suggestions.append(name)
		if not len(suggestions) == 0:
			print "Movie not found! Did you mean: "
			for suggestion in suggestions:
				print ("\t" + suggestion)	
		else:
			print "Movie not found! (Enter 'list' for list of valid names)"		
		continue
