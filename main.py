from PIL import Image
import os
import pygame

def drawRings(frameAvg, movie, flag):
	if flag:
		##Reading file
		frameAvg = []
		temp2 = []
		foo = open("index.txt", "r")
		temp = foo.readlines()
		foo.close()
		for i in xrange(len(temp)/3):
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
	SIZE = [1050, 1050]
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption(movie)

	#Drawing circles using the average color of each frame
	for i in xrange(len(frameAvg)):
		(r, b, g)=(int(frameAvg[i][0]), int(frameAvg[i][1]), int(frameAvg[i][2]))
		color=(r, b, g)
		pygame.draw.circle(screen, color, [SIZE[0] / 2, SIZE[1] / 2], 3 * (len(frameAvg)) + 3 - 3 * (i + 1))
	pygame.display.flip()


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
		if os.path.exists("index.txt"):
			flag = True
		if flag:
			drawRings([], movie, flag)
			os.chdir('..')	
			continue	
		frameAvg = []

		moviefile = ""
		for name in os.listdir('.'):
			if name.startswith(movie) and not name.endswith('.jpg'):
				moviefile = name

		files=[name for name in os.listdir('.') if os.path.isfile(name) and name.endswith('.jpg')]
		if len(files) == 0:
			os.system("ffmpeg -i \"" + moviefile + "\" -r 0.0167 %02d.jpg")
		for name in files:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ("proccessing frame " +name[:-4] + " of " + files[len(files)-1][:-4])
			im = Image.open(name)
			pix=im.load()
			x, y =im.size 
			RED_VALS = []
			BLUE_VALS = []
			GREEN_VALS =[]
			avgRed = 0
			avgBlue = 0
			avgGreen = 0
			for i in xrange(100):
				for j in xrange(100):
					temp, temp1, temp2 = pix[int(i * (x / 100)), int(j * (y / 100))]
					RED_VALS.append(temp)
					BLUE_VALS.append(temp1)
					GREEN_VALS.append(temp2)
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