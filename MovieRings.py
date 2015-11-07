from PIL import Image
import os
import pygame

def drawRings(frameavg, movie, flag):
	if flag:
		##Reading file
		frameavg=[]
		temp2=[]
		asdf = open("index.txt", "r")
		temp = asdf.readlines()
		asdf.close()
		for i in xrange(len(temp)/3):
			frameavg.append([temp[3*i], temp[3*i+1], temp[3*i+2]]) 	
	else:
		##Writing to file
		asdf = open("index.txt", "w")
		for i in xrange(len(frameavg)):
			for j in xrange(3):		
				asdf.write(str(frameavg[i][j]))
				asdf.write("\n")
		asdf.close()	
			
	#Initializing pygame
	pygame.init()
	SIZE = [1050, 1050]
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption(movie)

	#Drawing circles using the average color of each frame
	for i in xrange(len(frameavg)):
		(r, b, g)=(int(frameavg[i][0]), int(frameavg[i][1]), int(frameavg[0][2]))
		color=r, b, g
		pygame.draw.circle(screen, color, [SIZE[0]/2, SIZE[1]/2],3*(len(frameavg))+3-3*(i+1))
	pygame.display.flip()


movielist=[name for name in os.listdir('.') if os.path.isdir(name)]
#Getting movie name:
while True:
	flag=False
	movie=raw_input("Please enter the name of the movie (or list for a list of movies): ")
	os.system('cls' if os.name == 'nt' else 'clear')
	#movie="Batman Begins"
	
	#os.chdir(os.getcwd()+'/'+movie+'/')
	#drawRings()
	#break
	
	if movie=="list":
		for name in movielist:
			print "\t"+name
		continue	
	if os.path.exists(movie) and os.path.isdir(movie):
		#Changing Direcotry and getting file names:
		os.chdir(os.getcwd()+'/'+movie+'/')
		if os.path.exists("index.txt"):
			flag=True
		if flag:
			drawRings([], movie, flag)
			os.chdir('..')	
			continue	
		frameavg=[]

		moviefile=""
		for name in os.listdir('.'):
			if name.startswith(movie) and not name.endswith('.jpg'):
				moviefile=name

		files=[name for name in os.listdir('.') if os.path.isfile(name) and name.endswith('.jpg')]
		if len(files)==0:
			os.system("ffmpeg -i \""+moviefile+"\" -r 0.0167 %02d.jpg")
		for name in files:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ("proccessing frame "+name[:-4]+" of "+files[len(files)-1][:-4])
			im = Image.open(name)
			pix=im.load()
			x, y =im.size 
			cone=[]
			ctwo=[]
			cthree=[]
			c=[]
			avgo=0
			avgt=0
			avgth=0
			for i in xrange(100):
				for j in xrange(100):
					temp, temp1, temp2 = pix[int(i*(x/100)), int(j*(y/100))]
					c.append([temp, temp1, temp2])
					#print temp, temp1, temp2
					# cone.append(temp)
					# ctwo.append(temp1)
					# cthree.append(temp2)
			# for i in xrange(10000):
			# 	avgo+=cone[i]
			# 	avgt+=ctwo[i]
			# 	avgth+=cthree[i]
			# avgo/=10000	
			# avgt/=10000
			# avgth/=10000
			passer=False
			maximum=[c.count(c[0]), c[0]]
			for color in c:
				counter=c.count(color)
				if counter<maximum[0]:
					c.remove(color)
				else:
					if maximum[1] in c:
						c.remove(maximum[1])
					maximum[1]=color
					maximum[0]=counter	
					
								
			#print maximum[1]
			frameavg.append(maximum[1])
		drawRings(frameavg, movie, flag)	
		os.chdir('..')	
		continue
	else:
		suggestions=[]
		for name in os.listdir('.'):
			if name.startswith(movie) or movie in name:
				suggestions.append(name)
		if not len(suggestions)==0:
			print "Movie not found! Did you mean: "
			for suggestion in suggestions:
				print ("\t"+suggestion)	
		else:
			print "Movie not found! (Enter list for list of valid names)"		
		continue