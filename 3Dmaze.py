import sys
import math
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy
import pygame
import time

WIDTH = 1280
HEIGHT = 720


GAMEDELAY = 25
PLAYERSPEED = 0.05
GHOSTSPEED = 0.1

FILENAME = 'test.txt'
FINISHSOUND = 'finish.mp3'
GHOSTSOUND = 'ghost.mp3'
GAMEBGM = 'bgm.mp3'

field = []
angle = 0

initStartFlag = False
gameStart = False
gameFinish = False
ghostFlag = False
ghostGo = True
soundFlag = True

playerPos = [1,1,1]
startPos = [1,1,1]
finishPos = [1,1,1]

ghostTrans = [0,1,0]
ghostPos = [0,1,0]
ghostStart = [0,1,0]
ghostFinish = [0,1,0]
ghostRange = [0,1,0]

look = [-1000,1,1000]
enemy = [-100,0,-100]

file = open(FILENAME,'r')
while(True):
    l = file.readline()
    if not l: break
    l = l[:len(l)-1]
    field.append(l.split(','))
file.close()

def initField():
    global initStartFlag, lookFlag, ghostGo, ghostFlag
    ghostCount = 0
    glEnable(GL_TEXTURE_2D)
    h = 0
    w = 0
    i = 0
    while(True) :
       w = 0
       if(i==len(field)):
          glPushMatrix()
          glTranslatef(enemy[0],0,enemy[2])
          glTranslatef(ghostTrans[0],0.75,ghostTrans[2])
          glBlendFunc(GL_SRC_ALPHA, GL_ONE)
          glEnable(GL_BLEND)
          glBindTexture(GL_TEXTURE_2D, texEnemy)
          glScalef(0.5,0.5,0.5)
          glBegin(GL_QUADS)
          if angle == 0:
                       glTexCoord2f(0.0,0.0); glVertex3f(0.0,1.0,0.0)
                       glTexCoord2f(0.0,1.0); glVertex3f(0.0,0.0,0.0)
                       glTexCoord2f(1.0,1.0); glVertex3f(1,0.0,0.0)
                       glTexCoord2f(1.0,0.0); glVertex3f(1,1.0,0.0)
               
          elif angle == -90:
                       glTexCoord2f(0.0,0.0); glVertex3f(0,1.0,0)
                       glTexCoord2f(0.0,1.0); glVertex3f(0,0.0,0)
                       glTexCoord2f(1.0,1.0); glVertex3f(0,0.0,1)
                       glTexCoord2f(1.0,0.0); glVertex3f(0,1.0,1)
               
          elif angle == 90:
                       glTexCoord2f(0.0,0.0); glVertex3f(1,1.0,0)
                       glTexCoord2f(0.0,1.0); glVertex3f(1,0.0,0)
                       glTexCoord2f(1.0,1.0); glVertex3f(1,0.0,1)
                       glTexCoord2f(1.0,0.0); glVertex3f(1,1.0,1)
               
          elif angle == 180:
                       glTexCoord2f(0.0,0.0); glVertex3f(0,1.0,1)
                       glTexCoord2f(0.0,1.0); glVertex3f(0,0.0,1)
                       glTexCoord2f(1.0,1.0); glVertex3f(1,0.0,1)
                       glTexCoord2f(1.0,0.0); glVertex3f(1,1.0,1)
          glEnd();
          glDisable(GL_BLEND)
          glPopMatrix()
          break
        
       for block in field[i]:
           glPushMatrix()
           glTranslatef(w,0,h)
           if block == 'a':
               glBindTexture(GL_TEXTURE_2D, texWall)
               glScalef (1.0, 1.0, 1.0)
               glBegin(GL_QUADS)
               glTexCoord2f(0.0,0.0); glVertex3f(-0.5,2.0,-0.5)
               glTexCoord2f(0.0,1.0); glVertex3f(-0.5,0.0,-0.5)
               glTexCoord2f(1.0,1.0); glVertex3f(0.5,0.0,-0.5)
               glTexCoord2f(1.0,0.0); glVertex3f(0.5,2.0,-0.5)
               
               glTexCoord2f(0.0,0.0); glVertex3f(-0.5,2.0,-0.5)
               glTexCoord2f(0.0,1.0); glVertex3f(-0.5,0.0,-0.5)
               glTexCoord2f(1.0,1.0); glVertex3f(-0.5,0.0,0.5)
               glTexCoord2f(1.0,0.0); glVertex3f(-0.5,2.0,0.5)
               
               glTexCoord2f(0.0,0.0); glVertex3f(0.5,2.0,-0.5)
               glTexCoord2f(0.0,1.0); glVertex3f(0.5,0.0,-0.5)
               glTexCoord2f(1.0,1.0); glVertex3f(0.5,0.0,0.5)
               glTexCoord2f(1.0,0.0); glVertex3f(0.5,2.0,0.5)
               
               glTexCoord2f(0.0,0.0); glVertex3f(-0.5,2.0,0.5)
               glTexCoord2f(0.0,1.0); glVertex3f(-0.5,0.0,0.5)
               glTexCoord2f(1.0,1.0); glVertex3f(0.5,0.0,0.5)
               glTexCoord2f(1.0,0.0); glVertex3f(0.5,2.0,0.5)
               glEnd()
               
           else :
               glBindTexture(GL_TEXTURE_2D, texFloor)
               glScalef (1.0, 1.0, 1.0)
               glBegin(GL_QUADS)
               glTexCoord2f(0.0,0.0); glVertex3f(-0.5,0.01,-0.5)
               glTexCoord2f(0.0,1.0); glVertex3f(0.5,0.01,-0.5)
               glTexCoord2f(1.0,1.0); glVertex3f(0.5,0.01,0.5)
               glTexCoord2f(1.0,0.0); glVertex3f(-0.5,0.01,0.5)
               glEnd()

               glBindTexture(GL_TEXTURE_2D, texCeil)
               glBegin(GL_QUADS)
               glTexCoord2f(0.0,0.0); glVertex3f(-0.5,1.99,-0.5)
               glTexCoord2f(0.0,1.0); glVertex3f(0.5,1.99,-0.5)
               glTexCoord2f(1.0,1.0); glVertex3f(0.5,1.99,0.5)
               glTexCoord2f(1.0,0.0); glVertex3f(-0.5,1.99,0.5)
               glEnd()
               
               if block == 's' and initStartFlag == False:
                   playerPos[0] = w
                   playerPos[2] = h
                   startPos[0] = w
                   startPos[2] = h
                   initStartFlag = True
                   
               elif block == 'v':
                   glBindTexture(GL_TEXTURE_2D, texKey)
                   glTranslatef(0,1,0)
                   glScalef (0.3, 0.3, 0.3)
                   glBegin(GL_QUADS)
                   th = float(2*math.pi)            
                   pi = math.pi    
                   for st in range(0,20,1):
                       s = float(st/20)
                       s2 = s + 0.05
                       for te in range(0,20,1):
                           t = float(te/20)
                           t2 = t + 0.05
                           glTexCoord2f(s,t)
                           glVertex3f(math.cos(pi*t-pi/2)*math.sin(th*s),
                                      -math.sin(pi*t-pi/2),math.cos(th*s)*math.cos(pi*t-pi/2))
                           glTexCoord2f(s,t2)
                           glVertex3f(math.cos(pi*t2-pi/2)*math.sin(th*s),
                                      -math.sin(pi*t2-pi/2),math.cos(th*s)*math.cos(pi*t2-pi/2))
                           glTexCoord2f(s2,t2)
                           glVertex3f(math.cos(pi*t2-pi/2)*math.sin(th*s2),
                                      -math.sin(pi*t2-pi/2),math.cos(th*s2)*math.cos(pi*t2-pi/2))
                           glTexCoord2f(s2,t)
                           glVertex3f(math.cos(pi*t-pi/2)*math.sin(th*s2),
                                      -math.sin(pi*t-pi/2),math.cos(th*s2)*math.cos(pi*t-pi/2))
                   glEnd();
                   finishPos[0]=w
                   finishPos[2]=h
               
               elif block == 'k':
                   enemy[0]=w
                   enemy[2]=h
                   if ghostRange[2] > 0:
                       if round(ghostTrans[2]*10) == round(ghostRange[2]*10):
                           ghostGo = False
                       elif round(ghostTrans[2]) == 0:
                           ghostGo = True
                       
                       if ghostGo:
                           ghostTrans[2] += GHOSTSPEED
                           ghostPos[2] += GHOSTSPEED
                       else:
                           ghostTrans[2] -= GHOSTSPEED
                           ghostPos[2] -= GHOSTSPEED

                   elif ghostRange[2] < 0:
                       if round(ghostTrans[2]*10) == 0:
                           ghostGo = False
                       elif round(ghostTrans[2]*10) == round(ghostRange[2]*10):
                           ghostGo = True
                       
                       if ghostGo:
                           ghostTrans[2] += GHOSTSPEED
                           ghostPos[2] += GHOSTSPEED
                       else:
                           ghostTrans[2] -= GHOSTSPEED
                           ghostPos[2] -= GHOSTSPEED

                   elif ghostRange[0] > 0:
                       if round(ghostTrans[0]*10) == round(ghostRange[0]*10):
                           ghostGo = False
                       elif round(ghostTrans[0]) == 0:
                           ghostGo = True
                       
                       if ghostGo:
                           ghostTrans[0] += GHOSTSPEED
                           ghostPos[0] += GHOSTSPEED
                       else:
                           ghostTrans[0] -= GHOSTSPEED
                           ghostPos[0] -= GHOSTSPEED

                   elif ghostRange[0] < 0:
                       if round(ghostTrans[0]*10) == round(ghostRange[0]*10):
                           ghostGo = True
                       elif round(ghostTrans[0]) == 0:
                           ghostGo = False
                       
                       if ghostGo:
                           ghostTrans[0] += GHOSTSPEED
                           ghostPos[0] += GHOSTSPEED
                       else:
                           ghostTrans[0] -= GHOSTSPEED
                           ghostPos[0] -= GHOSTSPEED
                           
                   ghostStart[0] = w
                   ghostStart[2] = h
                   ghostCount += 1
                   
                   if ghostCount == 2 and ghostFlag == False:
                       ghostRange[0] = ghostFinish[0] - ghostStart[0]
                       ghostRange[2] = ghostFinish[2] - ghostStart[2]
                       ghostPos[0] = w
                       ghostPos[2] = h
                       ghostFlag = True
                   
               elif block == 'y':
                   ghostFinish[0] = w
                   ghostFinish[2] = h
                   ghostCount += 1
                   
                   if ghostCount == 2 and ghostFlag == False:
                       ghostRange[0] = ghostFinish[0] - ghostStart[0]
                       ghostRange[2] = ghostFinish[2] - ghostStart[2]
                       ghostPos[0] = w
                       ghostPos[2] = h
                       ghostFlag = True
               
           glPopMatrix()
           w += 1
       h += 1
       i += 1

def display():
   global angle, gameStart, gameFinish
   glClear (GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
   glEnable(GL_DEPTH_TEST)
   glLoadIdentity ()
   
   gluPerspective(90, float(WIDTH/HEIGHT), 0.1, 20.0)
   gluLookAt(playerPos[0],playerPos[1],playerPos[2], look[0] * math.sin(math.radians(angle)), look[1], look[2] * math.cos(math.radians(angle)), 0.0, 1.0, 0.0)
   
   initField()

   if angle == 0:
       x = int(playerPos[0] + 0.001)
       z = int(playerPos[2]) + 1
   elif angle == 90:
       x = math.ceil(playerPos[0]) - 1
       z = int(playerPos[2])
   elif angle == 180:
       x = int(playerPos[0])
       z = math.ceil(playerPos[2]) - 1
   elif angle == -90:
       x = int(playerPos[0]) + 1
       z = int(playerPos[2])
       
   if gameStart == True and gameFinish == False:
       if field[z][x] != 'a':
           playerPos[0] += -1 * PLAYERSPEED * math.sin(math.radians(angle))
           playerPos[2] += PLAYERSPEED * math.cos(math.radians(angle))
           
           if finishPos[0] == round(playerPos[0]) and finishPos[2] == round(playerPos[2]):
               gameStart = False
               gameFinish = True
               soundFlag = False
               pygame.mixer.init()
               pygame.mixer.music.load(FINISHSOUND)
               pygame.mixer.music.play(0)
               
           if round(ghostPos[0]) == round(playerPos[0]) and round(ghostPos[2]) == round(playerPos[2]):
               gameStart = False
               soundFlag = False
               pygame.mixer.init()
               pygame.mixer.music.load(GHOSTSOUND)
               pygame.mixer.music.play(0)
               time.sleep(3)
               playerPos[0] = startPos[0]
               playerPos[2] = startPos[2]
               angle = 0
               soundFlag = True
               backgroundSound()

   glColor3f(0.9, 0.9, 0.9);
   glBegin(GL_QUADS);
   glVertex3f(-100.0, 0.0, -100.0);
   glVertex3f(-100.0, 0.0,  100.0);
   glVertex3f( 100.0, 0.0,  100.0);
   glVertex3f( 100.0, 0.0, -100.0);
   glEnd();
   
   glutSwapBuffers()

def reshape (w, h):
   glViewport (0, 0, w, h)

def keyboard(bkey, x, y):
    global angle, gameStart
    key = bkey.decode("utf-8")
    if key == 'a':
        angle -= 90
    elif key == 'd':
        angle += 90
    elif key == 'w':
        gameStart = True  
    elif key == 's':
        angle -= 180

    if angle >= 360:
        angle = 0
    elif angle == 270:
        angle = -90
    elif angle <= -270:
        angle = 90
    elif angle == -180:
         angle = 180

def glutTimer(v):
    glutPostRedisplay()
    glutTimerFunc(GAMEDELAY, glutTimer, GAMEDELAY)

def backgroundSound():
    global soundFlag
    
    if soundFlag == True:
        pygame.mixer.init()
        pygame.mixer.music.load(GAMEBGM)
        pygame.mixer.music.play(-1)
    elif soundFlag == False:
        pygame.mixer.music.quit()

def read_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    tmp = os.path.splitext(filename)[0]
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    if tmp == 'pacman': glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    else : glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

glutInit(sys.argv)
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize (WIDTH, HEIGHT)
glutInitWindowPosition (100, 100)
glutCreateWindow (b'3Dmaze')
glClearColor (0.0, 0.0, 0.0, 0.0)
glShadeModel (GL_FLAT)
backgroundSound()

texFloor = read_texture('floor.jpg')
texWall = read_texture('wall.jpg')
texCeil = read_texture('ceiling.png')
texKey = read_texture('gold.jpg')
texEnemy = read_texture('pacman.png')
glutDisplayFunc(display)
glutTimerFunc(GAMEDELAY,glutTimer,GAMEDELAY)

glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMainLoop()


