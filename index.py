#TODO
#Light system
#Relative projection

#Libraries
import math
import pygame
import sys
import time
from os import system
from pygame import (
    QUIT
)
#Initializing pygame, mixer (for future sounds), and display
display = pygame.display.set_mode((700,700))
pygame.mixer.init()
pygame.init()

#Functions 
#Orthographic projection.
def orthoProjection(vector):
    return (vector[0],vector[1])

def rotateX(vector, angle):
    matrix = [
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]
    return (vector[0]*matrix[0][0]+vector[1]*matrix[0][1]+vector[2]*matrix[0][2], vector[0]*matrix[1][0]+vector[1]*matrix[1][1]+vector[2]*matrix[1][2],vector[0]*matrix[2][0]+vector[1]*matrix[2][1]+vector[2]*matrix[2][2])

def rotateY(vector, angle):
    matrix = [
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)],
    ]
    return (vector[0]*matrix[0][0]+vector[1]*matrix[0][1]+vector[2]*matrix[0][2], vector[0]*matrix[1][0]+vector[1]*matrix[1][1]+vector[2]*matrix[1][2],vector[0]*matrix[2][0]+vector[1]*matrix[2][1]+vector[2]*matrix[2][2])

def rotateZ(vector, angle):
    matrix = [
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1],
    ]
    return (vector[0]*matrix[0][0]+vector[1]*matrix[0][1]+vector[2]*matrix[0][2], vector[0]*matrix[1][0]+vector[1]*matrix[1][1]+vector[2]*matrix[1][2],vector[0]*matrix[2][0]+vector[1]*matrix[2][1]+vector[2]*matrix[2][2])
#Manage keyboard, window and mouse events
def manageEvents():
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
#Check if faces are showing front surface or back surface
def facingSide(vector1, vector2, vector3):
    return (vector2[0] - vector1[0]) * (vector3[1] - vector1[1]) - (vector3[0] - vector1[0]) * (vector2[1] - vector1[1])
#Calculating distance between 3D points
def distance3D(vector1,vector2):
    return math.sqrt(math.pow(vector1[0] - vector2[0], 2) + math.pow(vector1[1] - vector2[1], 2) + math.pow(vector1[2] - vector2[2], 2))
#Classes
class Mesh:
    def __init__(self, vectors = [], faces = [], colors = []):
        self.vectors = vectors
        self.faces = faces
        self.colors = colors
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
        self.x = 250
        self.y = 450
        self.zoom = 6
    def draw(self):
        i = 0
        global light
        for face in self.faces:
            #Calculating distance to light
            distance1 = distance3D(rotateZ(rotateY(rotateX(self.vectors[face[0]],self.angleX),self.angleY),self.angleZ),(light["x"],light["y"],light["z"]))
            distance2 = distance3D(rotateZ(rotateY(rotateX(self.vectors[face[1]],self.angleX),self.angleY),self.angleZ),(light["x"],light["y"],light["z"]))
            distance3 = distance3D(rotateZ(rotateY(rotateX(self.vectors[face[2]],self.angleX),self.angleY),self.angleZ),(light["x"],light["y"],light["z"]))
            #Projecting vectors
            vector1 = orthoProjection(rotateZ(rotateY(rotateX(self.vectors[face[0]],self.angleX),self.angleY),self.angleZ))
            vector2 = orthoProjection(rotateZ(rotateY(rotateX(self.vectors[face[1]],self.angleX),self.angleY),self.angleZ))
            vector3 = orthoProjection(rotateZ(rotateY(rotateX(self.vectors[face[2]],self.angleX),self.angleY),self.angleZ))
            vector4 = ()
            if len(face) == 4:
                vector4 = orthoProjection(rotateZ(rotateY(rotateX(self.vectors[face[3]],self.angleX),self.angleY),self.angleZ))
            #Moving vectors
            vector1=((vector1[0]*self.zoom)+self.x,(vector1[1]*self.zoom)+self.y)
            vector2=((vector2[0]*self.zoom)+self.x,(vector2[1]*self.zoom)+self.y)
            vector3=((vector3[0]*self.zoom)+self.x,(vector3[1]*self.zoom)+self.y)
            if len(face)==4:
                vector4=((vector4[0]*self.zoom)+self.x,(vector4[1]*self.zoom)+self.y)
            #Drawing vectors
            color = self.colors[i]
            if facingSide(vector1,vector2,vector3)>0:
                if len(face) >= 4:
                    pygame.draw.polygon(display, self.colors[i],(vector1,vector2,vector3,vector4))
                else:
                    pygame.draw.polygon(display, self.colors[i],(vector1,vector2,vector3))
            i+=1
#Simple .obj models loader
def loadModel(direction):
    faces = []
    vertices = [0]
    newLine = None
    try:
        model = open(direction,"r")
        for line in model: 
            if line[0] == "v" and line[1] == " ":
                newLine = line.replace("v ","")
                newLine = newLine.split(" ")
                for i in range(len(newLine)):
                    newLine[i] = float(newLine[i])
                vertices.append((newLine[0],newLine[1],newLine[2]))
            elif line[0] == "f" and line[1] == " ":
                newLine = line.replace("f ","")
                newLine = newLine.replace("\n","")
                newLine = newLine.split(" ")
                for i in range(len(newLine)):
                    newLine[i] = newLine[i].split("/")
                    newLine[i] = int(newLine[i][0])
                if len(newLine)==4:
                    faces.append((newLine[0],newLine[1],newLine[2],newLine[3]))
                else:
                    faces.append((newLine[0],newLine[1],newLine[2]))
    except:
        print("ERROR")
    return (faces,vertices)
#Loop function
def loop():
    global Time
    global fps
    global lastFps
    while True:
        #Clearing display
        display.fill((0,0,0))
        #Info title with fps, faces and vectors information
        infoTitle = "<STARSHIPCODE RENDERER> FPS "+str(lastFps)+" Faces:"+str(len(masterChiefFaces))+" Vertices:"+str(len(masterChiefVertices))
        pygame.display.set_caption(infoTitle)
        #Calculating FPS
        if time.time()-Time>=1:
            Time = time.time()
            lastFps = fps
            fps = 0
        else:
            fps+=1
        #Rotating model
        mesh.angleY+=math.pi/180*2
        #Calling event manager function
        manageEvents()
        #Draw mesh
        mesh.draw()
        #Update pygame display
        pygame.display.update()
#Some light
light = {
    "x":0,
    "y":0,
    "z":0
}
#Loading model
model = loadModel("./master_chief.obj")
masterChiefVertices = model[1]
masterChiefFaces = model[0]
masterChiefColors = []
for i in range(len(masterChiefFaces)):
    masterChiefColors.append((100,100,100))
mesh = Mesh(masterChiefVertices,masterChiefFaces,masterChiefColors)
mesh.angleZ=math.pi/180*180

#Loading cube model
"""mesh = Mesh([
    (-100, -100, 100),
    (-100, 100, 100),
    (100, 100, 100),
    (100, -100, 100),
    (-100, -100, -100),
    (-100, 100, -100),
    (100, 100, -100),
    (100, -100, -100)
],[
    (0, 1, 2),
    (0, 2, 3),
    (6, 5, 4),
    (7, 6, 4),
    (4, 5, 0),
    (5, 1, 0),
    (3, 2, 6),
    (6, 7, 3),
    (3, 4, 0),
    (3, 7, 4),
    (1, 5, 2),
    (5, 6, 2),
],
[
    (0, 100, 200),
    (0, 100, 200),
    (0, 200, 100),
    (0, 200, 100),
    (200, 100, 0),
    (200, 100, 0),
    (100, 200, 0),
    (100, 200, 0),
    (0, 150, 0),
    (0, 150, 0),
    (0, 0, 150),
    (0, 0, 150),
])"""
#Stadistics
fps = 0
lastFps = 0
Time = time.time()
loop()