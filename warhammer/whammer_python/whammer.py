
# TODO:
#
# class walls/doors
#
# get equipment 
#
# different controls for types


# PyInstaller --onefile whammer.py


########## CODE: ##########
import os, pygame, sys, random, pickle, struct, threading, socket, json#, socketserver, eztext, math
from pygame.locals import *   # only import needed functions and variables?
from win32api import GetSystemMetrics  # for getting the screen resolution

class Game_variables():
    def __init__(self, size, screen):
        #replace global variables with self.var
        #global online, online2
        self.online=False
        self.socksend=0
        self.sockrec=0
        #self.online2=True
        
        self.playerkind=0
        self.gamesize=size
        
        #global background
        #background= pygame.image.load('sprites/Background/backgrounddetailed8.png')
        
        #global gamew, gameh
        self.gamew, self.gameh = 0,0 # background.get_size()
    
        # Define the colors
        # remember: http://www.colorpicker.com
        # Delete?
        
#        BLACK = ( 0, 0, 0)
#        WHITE = ( 255, 255, 255)
#        GREEN = ( 0, 255, 0)
#        RED = ( 255, 0, 0)
#        BLUE = ( 0, 0, 255)
#        GREY = ( 175, 175, 175)
        
        # for now, user is a minion object:
        #global user, main_players, server_parent
        
        self.user=0
        self.main_players=[]
        #online_players=pygame.sprite.Group()
        #online_ships=[]   # turn this into a pygame group?
        
        #global clientlist
        self.clientlist=[]  # delete?
        
        self.server_parent=""
        
        #global walls, screensquares, left_rect, right_rect, toprect, bottomrect, spawningoffscreen
    
        #self.walls = [] # List to hold the walls
        
        self.screensquares=[]
        
        self.left_rect = 0
        self.right_rect = 0
        self.toprect = 0
        self.bottomrect = 0
        
        self.spawningoffscreen=False
        
        #global myTick, keyTime
        self.myTick=0
        self.keyTime=0
        
        #global socksend, sockrec, host, port
        
        self.fullwidth = GetSystemMetrics(0)
        self.fullheight = GetSystemMetrics(1)
        self.fullscrn=0
        
        self.dragging=False
        
        self.current_location=0
        self.botbar=0
        self.game_map=[]
        self.host=0
        self.port=0
        self.my_screen=screen
        
    def set_boundaries(self):
        #left_rect = pygame.Rect(0, 0, .3*size[0], size[1])
        if self.fullscrn==0:
            width, height=self.gamesize
        elif self.fullscrn==1:
            width=self.fullwidth
            height=self.fullheight
        self.left_rect = ScreenBoundary(0, 0, .3*width, height)
        self.left_rect.setsize()
        self.right_rect = ScreenBoundary(width-.3*width, 0, .3*width, height)
        self.right_rect.setsize()
        self.toprect = ScreenBoundary(0, 0, width, .3*height)
        self.toprect.setsize()
        self.bottomrect = ScreenBoundary(0, height-.3*height, width, .3*height)
        self.bottomrect.setsize()
        self.screensquares=[self.left_rect,
                            self.right_rect,
                            self.toprect,
                            self.bottomrect]

class ScreenBoundary(pygame.Rect):
    def __init__(self, x, y, w,h):
        #global gamesize, fullscrn, fullwidth, fullheight
        self.x=x
        self.y=y
        self.width=w
        self.height=h
    def setsize(self):
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        

#class Environment():
#    self.all=[]

#TODO:
class Buildings(pygame.sprite.Sprite):
    def __init__(self,name,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.x=x
        self.y=y
        #pick jumpspots or doors:
        self.doors=[]
        self.jumpspots=[]
        #
        self.spawnpoints=[]
        self.health=1000
        self.damage=0
        self.built=100 # percentage
        self.set_image()
    def set_image(self):
        self.image=pygame.image.load('sprites/environment/buildings/{}.png'.format(self.name))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
        #self.width
        #self.height
        
    
class Spawnpoints():
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        self.conditions=[]
        self.spawns=[]
        self.set_image()
    def set_image(self):
        self.image=pygame.image.load('sprites/environment/red.png')
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
        #self.rect=pygame.Rect(self.x,self.y,30,30)
    
class Jumpspot():
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        #self.width=
        #self.height=
        self.to_use=[] #'touch' or 'key'
        self.conditions=[]
        self.set_image()
    def set_image(self):
        self.image=pygame.image.load('sprites/environment/blue.png')
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
        #self.rect=pygame.Rect(self.x,self.y,30,30)
    
class Trees():
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        self.health=50
        self.wood=80
        self.set_image()
    def set_image(self):
        self.image=pygame.image.load('sprites/environment/trees/{}.png'.format(self.name))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
    
class Sandbags():
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        self.health=200
        self.set_image()
    def set_image(self):
        self.image=pygame.image.load('sprites/environment//{}.png'.format(self.name))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
    
class Goldmine():
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        self.health=200
        self.gold=10000 
        self.set_image()
    def set_image(self):
        self.image=pygame.image.load('sprites/environment/resources/{}.png'.format(self.name))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
    

#TODO:
# make a function that imports quests from a text file
class Quests():
    def __init__(self):
        self.questlist=[]
        self.flaglist=[]
    def newquest(self, quest):
        for objective in quest:
            self.questlist.append(objective)
    def new_objective(self, mission):
        self.questlist.append(mission)
        if mission.requires==[]:
            self.unlock_quest(mission)
#         for flags in mission.actions:
#             self.flaglist.append(Flag(flags, mission))
    def unlock_quest(self, mission):
        for quest in self.questlist:
            if quest.name==mission.name:
                print('new quest!')
                #print(mission.say)
                templist=quest.unlock()
                for flags in templist:
                    newflag=Flag(flags, mission)
                    #print(newflag.name)
                    self.flaglist.append(newflag)
    def missioncomplete(self, mission):
        for reward in mission.reactions:
            if reward[0]=="xp":
                global gamevars
                #print(user.xp)
                gamevars.user.xp+=reward[1]
                print("new xp: {}".format(gamevars.user.xp))
        for objective in self.questlist:
            if objective.parent==mission.parent:
                del objective
    def check_quests(self, donemission):
        if donemission.complete() ==1:
            return 1
        else:
            return 0
    def check_flaglist(self):
        """This gets checked every cycle for completed flags, 
        and completes/deletes the related objectives.
        """
        for flag in self.flaglist:
            if flag.done==True:
                self.flaglist.remove(flag)
                flag.parent.actions.remove(flag.name)
                #print(flag.parent.actions)
                if flag.parent.complete()==1:
                    self.missioncomplete(flag.parent)
                del flag
    def doneflags(self,doneflag):
        """This gets called every time a potential objective 
        or requirement is performed (kill, collect, level up, etc).
        """
        for flag in self.flaglist:
            if flag.name==doneflag:
                flag.done=True
                flag.parent.action_done(flag.name)
                print('flag done')
                return
                
    #TODO: copy this to all possible quest objectives:
    #check_flaglist('kill {}'.format(guy.name))
    #check_flaglist('kill npc/player')
        
    
class Objective():
    def __init__(self, name, mission):
        self.name=name
        self.parent=mission
        self.locked=True
        self.requires=[]
#                        [('skill level',8),
#                        ('crystal',1)]
        self.add=[]
#                     ['npc', 'weapon', 'key', 'map']
        self.actions=[]
#                       ['collect thing',
#                       'kill npc', kill statue]
        self.completed=False
        #TODO: some add elements (keys?) need flags,
        # if flag = Mission: delete element
        self.reactions=[]
#                         [('unlock item',[]),
#                         ('unlock quest',[]),
#                         ('unlock space',[]),
#                         ('load space/planet',[]),
#                         ('xp',[]),
#                         ('reward',[])
#                         ('say','')
#                         ('add', ['building','spacestation'])]
        self.say=''
        # this is said when the quest is unlocked
        # to say something at the end of the quest,
        # put in self.reactions list with keyword 'say'

    def unlock(self):
        if self.requires==[]:
            self.locked=False
            print(self.say)
            for thing in self.add:
                self.add_to_map(thing)
            self.add=[]
            return self.actions
        else:
            #print("Objective not ready yet")
            return self.requires
    def action_done(self, done):
        for action in self.actions:
            if action==done:
                del action
                return 1
    def complete(self):
        if self.actions==[]:
            self.completed=True
            print('mission complete!')
            return 1
        else:
            #print("Objective not complete yet")
            return 0
    def add_to_map(self, add):
        global gamevars
        if add=='statue':
            gamevars.current_location.npc.add(Statue("Statue"))
        
        
class Flag():
    def __init__(self, name, parent):
        self.done=False
        self.name=name
        self.parent=parent
        

class Wearing_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = pygame.image.load('sprites/ui/wearing_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.pic, (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.pic, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        
class Skills_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = pygame.image.load('sprites/ui/skills_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.pic, (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.pic, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        
class Troop_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = pygame.image.load('sprites/ui/troops_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.pic, (self.width, self.height))
        self.visible=False
        button1=Menu_Button('button1', 'buy_troop', self.width/4, self.y)
        button1.contains=BuyTroopObj(0,0,0,0) # TODO: button contents don't need rect?
        square1=UI_square("buy troop obj", self.x, self.y)
        square1.contains=BuyTroopObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square1.contains.pic='sprites/ui/troop.png'
        square1.contains.image=pygame.transform.scale( pygame.image.load(square1.contains.pic), square1.rect.size)
        self.mybuttons=[button1]
        self.mysquares=[square1]
        
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.pic, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        
class Groups_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = pygame.image.load('sprites/ui/groups_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.pic, (self.width, self.height))
        self.visible=False
        button1=Menu_Button('button1', 'square_formation', self.x+self.width/4, self.y)
        button1.contains=SquareFormationObj(0,0,0,0) # TODO: button contents don't need rect?
        button2=Menu_Button('button2', 'line_formation', self.x+self.width/4, self.y+self.height/6)
        button2.contains=LineFormationObj(0,0,0,0)
        square1=UI_square("square formation obj", self.x, self.y)
        square1.contains=SquareFormationObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square1.contains.pic='sprites/ui/groups.png'
        square2=UI_square("line formation obj", self.x, self.y+self.height/6)
        square2.contains=LineFormationObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square2.contains.pic='sprites/ui/groups.png'
        square1.contains.image=pygame.transform.scale( pygame.image.load(square1.contains.pic), square1.rect.size)
        square2.contains.image=pygame.transform.scale( pygame.image.load(square2.contains.pic), square2.rect.size)
        self.mybuttons=[button1, button2]
        self.mysquares=[square1, square2]
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale( self.pic, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        


class Inventory_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = 'sprites/ui/inventory_menu.png'
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
#         for square in range(12):
#             self.myhotkeys.append(UI_square('inventory_square',
#                                             (self.width//55)+(square)*(self.width//27.2), 
#                                             self.y+self.height//3))
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()


class Weapon_skills_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = 'sprites/ui/weapon_skills_menu.png'
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()

class Small_structures_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = 'sprites/ui/small_structures_menu.png'
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()

class Ship_menu():
    def __init__(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//5
        self.height=height//2
        self.pic = 'sprites/ui/ship_menu.png'
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        self.visible=False
        button1=Menu_Button('button1', 'buy_ship', self.x+self.width/4, self.y)
        button1.contains=BuyShipObj(0,0,0,0) # TODO: button contents don't need rect?
        square1=UI_square("buy ship obj", self.x, self.y)
        square1.contains=BuyShipObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square1.contains.pic='sprites/ui/ship.png'
        #print(square1.rect.size)
        square1.contains.image=pygame.transform.scale( pygame.image.load(square1.contains.pic), square1.rect.size)
        self.mybuttons=[button1]
        self.mysquares=[square1]
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()

class ActionObject():
    def __init__(self, x,y,width,height):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            Twidth, Theight=gamevars.gamesize
        elif gamevars.fullscrn==1:
            Twidth=gamevars.fullwidth
            Theight=gamevars.fullheight
        self.image='none'
        self.pic='none'
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.posratio=(self.x/Twidth,self.y/Theight)
        self.sizeratio=(self.width/Twidth,self.height/Theight)
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        if self.pic!='none':
            self.image=pygame.image.load(self.pic)
            self.image=pygame.transform.scale(self.image, (self.width, self.height))
        
class BuyTroopObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global gamevars
        user=gamevars.user
        if user.biomatter>=100:
            user.biomatter=user.biomatter-100
            user.myarmy.append(Character(gamevars.playerkind,gamevars.server_parent,name="minion"))
            print("Biomatter: "+str(user.biomatter))
        else:
            print("Not enough biomatter.")
            
class BuyShipObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global gamevars
        spawn_ship(gamevars.user)
    

class SquareFormationObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global gamevars
        troop_formations_square(gamevars.user.mysprite, gamevars.user.myarmy)
    
class LineFormationObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global gamevars
        troop_formations_line(gamevars.user.mysprite, gamevars.user.myarmy)

#TODO: move all if statements (functions) in "my click",
# instead the function should be in whatever it "self.opens"
# the thing in self.opens should be an object, can be dragged, remembers click function 
class Menu_Button():
    def __init__(self, name, kind, x, y, opens='none'):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//38
        self.height=height//38 
        self.posratio=(x/width,y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.name=name
        self.visible=True
        self.x=x
        self.y=y
        self.contains='empty'
        self.kind=kind
        self.opens=opens
        self.image='none'
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        if self.name=='newgamebutton':
            self.pic = 'sprites/ui/newgamebutton.png'
        elif self.name=='loadgamebutton':
            self.pic = 'sprites/ui/loadgamebutton.png'
        elif self.name=='quitgamebutton':
            self.pic = 'sprites/ui/quitgamebutton.png'
        elif self.name=='wearing_menu':
            self.pic = 'sprites/ui/armor.png'
        elif self.name=='skills_menu':
            self.pic = 'sprites/ui/skills.png'
        elif self.name=='troops_menu':
            self.pic = 'sprites/ui/troop.png'
        elif self.name=='groups_menu':
            self.pic = 'sprites/ui/groups.png'
        elif self.name=='closeright' or self.name=='closeleft':
            self.pic = 'sprites/ui/close.png'
        elif self.name=='inventory_menu':
            self.pic = 'sprites/ui/backpack.png'
        elif self.name=='weapon_skills_menu':
            self.pic = 'sprites/ui/weapon_skills.png'
        elif self.name=='buildings_menu':
            self.pic = 'sprites/ui/buildings.png'
        elif self.name=='ship_menu':
            self.pic = 'sprites/ui/ship.png'
        else:
            self.pic='none'
        if (self.pic!='none' and self.kind!='startmenu'):
            self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        if self.image!='none':
            self.image=pygame.transform.scale(pygame.image.load(self.pic), (self.width, self.height))
    def myclick(self):
        global gamevars
        if self.kind=='startmenu':
            if self.name=='button1':
                return 'human'
            if self.name=='button2':
                return 'tyranid'
            if self.name=='button3':
                print('\n\n\nERROR: NOT READY YET\n\n')
            if self.name=='button4':
                print('\n\n\nERROR: NOT READY YET\n\n')
            if self.name=='button5':
                print('\n\n\nERROR: NOT READY YET\n\n')
            if self.name=='button6':
                print('\n\n\nERROR: NOT READY YET\n\n')
            if self.name=='button7':
                print('\n\n\nERROR: NOT READY YET\n\n')
        elif self.opens!='none':
            if self.opens.visible==False:
                self.opens.visible=True
                if self.name!='wearing_menu' and self.kind=='leftmenu':
                    gamevars.botbar.wearing.visible=False
                if self.name!='skills_menu' and self.kind=='leftmenu':
                    gamevars.botbar.myskills.visible=False
                if self.name!='troops_menu' and self.kind=='leftmenu':
                    gamevars.botbar.mytroops.visible=False
                if self.name!='groups_menu' and self.kind=='leftmenu':
                    gamevars.botbar.mygroups.visible=False
                if self.name!='inventory_menu' and self.kind=='rightmenu':
                    gamevars.botbar.inventory.visible=False
                if self.name!='weapon_skills_menu' and self.kind=='rightmenu':
                    gamevars.botbar.weapon_skills.visible=False
                if self.name!='buildings_menu' and self.kind=='rightmenu':
                    gamevars.botbar.buildings.visible=False
                if self.name!='ship_menu' and self.kind=='rightmenu':
                    gamevars.botbar.ship.visible=False
            else:
                self.opens.visible=False
        elif self.kind=='close':
            if self.name=='closeleft':
                gamevars.botbar.wearing.visible=False
                gamevars.botbar.myskills.visible=False
                gamevars.botbar.mytroops.visible=False
                gamevars.botbar.mygroups.visible=False
            elif self.name=='closeright':
                gamevars.botbar.inventory.visible=False
                gamevars.botbar.weapon_skills.visible=False
                gamevars.botbar.buildings.visible=False
                gamevars.botbar.ship.visible=False

        # TODO: everything uses this myclick, instead of the button knowing functions:
        else:
            self.contains.myclick()
        

class UI_bar():
    def __init__(self, view_mode):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.visible=True
        self.x=0
        self.y=0
        self.myhotkeys=[]
        self.myleftbuttons=[]
        self.myrightbuttons=[]
        if view_mode=='player':
            self.pic = pygame.image.load('sprites/ui/botbar.png')
            self.width=width
            self.height=height//9
            self.x=0
            self.y=height*(4/4.5)
            self.image = pygame.transform.scale(self.pic, (self.width, self.height))
            
            # Build side menus:
            self.wearing=Wearing_menu()
            self.myskills=Skills_menu()
            self.mytroops=Troop_menu()
            self.mygroups=Groups_menu()
            self.inventory=Inventory_menu()
            self.weapon_skills=Weapon_skills_menu()
            self.buildings=Small_structures_menu()
            self.ship=Ship_menu()
            self.mymenus=[self.wearing,
                          self.myskills,
                          self.mytroops,
                          self.mygroups,
                          self.inventory,
                          self.weapon_skills, 
                          self.buildings,
                          self.ship]
            
            
            self.hotkey1=UI_square('hot_key',
                                (self.width//55)+(0)*(self.width//27.2), 
                                self.y+self.height//3)
            self.hotkey2=UI_square('hot_key',
                                (self.width//55)+(1)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey3=UI_square('hot_key',
                                (self.width//55)+(2)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey4=UI_square('hot_key',
                                (self.width//55)+(3)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey5=UI_square('hot_key',
                                (self.width//55)+(4)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey6=UI_square('hot_key',
                                (self.width//55)+(5)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey7=UI_square('hot_key',
                                (self.width//55)+(6)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey8=UI_square('hot_key',
                                (self.width//55)+(7)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey9=UI_square('hot_key',
                                (self.width//55)+(8)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey10=UI_square('hot_key',
                                (self.width//55)+(9)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey11=UI_square('hot_key',
                                (self.width//55)+(10)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.hotkey12=UI_square('hot_key',
                                (self.width//55)+(11)*(self.width//27.2), 
                                self.y+self.height//3)
            
            self.myhotkeys=[self.hotkey1,
                            self.hotkey2,
                            self.hotkey3,
                            self.hotkey4,
                            self.hotkey5,
                            self.hotkey6,
                            self.hotkey7,
                            self.hotkey8,
                            self.hotkey9,
                            self.hotkey10,
                            self.hotkey11,
                            self.hotkey12]
            
            # Left menu buttons:
            self.myleftbuttons.append(Menu_Button('wearing_menu', 'leftmenu',
                                            (self.width//55)+( 0 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.wearing))
            self.myleftbuttons.append(Menu_Button('skills_menu', 'leftmenu',
                                            (self.width//55)+( 1 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.myskills))
            self.myleftbuttons.append(Menu_Button('troops_menu', 'leftmenu',
                                            (self.width//55)+( 2 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.mytroops))
            self.myleftbuttons.append(Menu_Button('groups_menu', 'leftmenu',
                                            (self.width//55)+( 3 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.mygroups))
            self.myleftbuttons.append(Menu_Button('closeleft', 'close',
                                            (self.width//55)+( 4 )*(self.width//26.8), 
                                            (height*5.7)//6.4))
            
            # Right menu buttons:
            self.myrightbuttons.append(Menu_Button('inventory_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 0 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.inventory))
            self.myrightbuttons.append(Menu_Button('weapon_skills_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 1 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.weapon_skills))
            self.myrightbuttons.append(Menu_Button('buildings_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 2 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.buildings))
            self.myrightbuttons.append(Menu_Button('ship_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 3 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.ship))
            self.myrightbuttons.append(Menu_Button('closeright', 'close',
                                            ((self.width*6.3)//8)+( 4 )*(self.width//26.8), 
                                            (height*5.7)//6.4))
            
    def resize_image(self, width, height):
        if width==0:
            width=self.width
        else:
            self.width=width
        if height==0:
            height=self.height
        else:
            self.height=height//9
        self.image = pygame.transform.scale(self.pic, (self.width, self.height))
        
        self.wearing.resize()
        self.myskills.resize()
        self.mytroops.resize()
        self.mygroups.resize()
        self.inventory.resize()
        self.weapon_skills.resize()
        self.buildings.resize()
        self.ship.resize()
        
        #count=0
        for square in self.myhotkeys:
            square.resize()
            #count+=1
            
        count=0
        for bttn in self.myleftbuttons:
            bttn.resize()
            count+=1
            
        
        count=0
        for bttn in self.myrightbuttons:
            bttn.resize()
            count+=1
        

class UI_square():
    def __init__(self, kind, x, y):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//36
        self.height=height//36
        self.posratio=(x/width,y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.visible=True
        self.x=x
        self.y=y
        self.moving=False
        self.image='none'
        self.pic='none'
        self.contains='empty'
        self.kind=kind
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        if type(self.contains)!=str:
            self.contains.resize()
    def assign(self, contains):
        self.contains=contains
    def myclick(self):
        #global dragging
        global gamevars
        gamevars.dragging=Moving_square(self.rect, self.contains, self)

class Icon_square():
    def __init__(self, kind):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//36
        self.height=height//36
        self.visible=True
        self.quantity=1
        self.kind=kind
        if kind=='pistol':
            self.pic= 'sprites/ui/pistol.png'
            self.abilities=['hip shot','scope shot','pistol whip']
        elif kind=='club':
            self.pic= 'sprites/ui/club.png'
            self.abilities=['swing','throw','block']
        else:
            self.pic='none'
            self.abilities=[]
        self.kind=kind
        if self.pic!='none':
            self.image=pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
        #self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def resize(self):
        #global gamesize, fullscrn, fullwidth, fullheight
        global gamevars
        if gamevars.fullscrn==0:
            width, height=gamevars.gamesize
        elif gamevars.fullscrn==1:
            width=gamevars.fullwidth
            height=gamevars.fullheight
        self.width=width//36
        self.height=height//36
        if self.kind=='pistol':
            self.pic= 'sprites/ui/pistol.png'
            self.abilities=['hip shot','scope shot','pistol whip']
        elif self.kind=='club':
            self.pic= 'sprites/ui/club.png'
            self.abilities=['swing','throw','block']
        self.image = pygame.transform.scale( pygame.image.load(self.pic), (self.width, self.height))
    def move_me(self):
        pass
    def myclick(self):
        print(self.kind)
        
class Moving_square():
    def __init__(self, rect, holding, parent):
        self.parent=parent
        self.holding=holding
        self.rect=pygame.Rect(rect)

    
def unclicked(bttn):
    #global dragging
    global gamevars
    if bttn.contains=='empty':
        bttn.contains=gamevars.dragging.holding
        if gamevars.dragging.parent.kind=='hot_key':
            gamevars.dragging.parent.contains='empty'
    elif bttn!=gamevars.dragging.parent:
        if gamevars.dragging.parent.kind=='hot_key':
            gamevars.dragging.parent.contains=bttn.contains
            bttn.contains=gamevars.dragging.holding
    gamevars.dragging=False
    
    
class Planet(pygame.sprite.Sprite):
    def __init__(self, name, parent, spacex=0, spacey=0, 
                 size=(12000, 12000), planet_type='none'):
        pygame.sprite.Sprite.__init__(self)
        self.hosting=0
        self.environment=[]
        self.above_planet=False
        self.size=size
        self.name=name
        self.space_type="none"
        self.parent=parent
        self.spacex=spacex
        self.spacey=spacey
        self.gamex=0    # these are to replace game x 
        self.gamey=0    # and game y
        self.planet_type=planet_type
        #self.background='none'
        self.npc=pygame.sprite.Group()
        self.other_players=[]
        self.online_players=pygame.sprite.Group()
        self.online_npcs=pygame.sprite.Group()
        self.online_troops=pygame.sprite.Group()
        self.online_ships=[]
        try:
            self.set_image()
        except AttributeError:
            print("No picture for planet.")
    def set_image(self):
        self.planetpic=setplanetpic(self.planet_type) # this function will pick a random planet that matches background
        self.rect = pygame.Rect(self.planetpic.get_rect())
        self.rect.move_ip(self.spacex, self.spacey)
        self.big_pic=setplanetpic('big')

    
class Space(pygame.sprite.Sprite):
    def __init__(self, name, space_type):
        pygame.sprite.Sprite.__init__(self)
        self.environment=[]
        self.name=name
        self.space_type=space_type
        self.environment=[]
        self.planets=[]
        self.background='none'
        self.screenx=0#delete?
        self.screeny=0#delete?
        self.gamex=0        # these are to replace game x 
        self.gamey=0        # and game y
        self.npc=pygame.sprite.Group()
        self.other_players=[]
        self.online_players=pygame.sprite.Group()
        self.online_npcs=pygame.sprite.Group()
        self.online_troops=pygame.sprite.Group()
        self.online_ships=[]
    def set_image(self):
        pass
    

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, faction):
        pygame.sprite.Sprite.__init__(self)
        self.faction=faction
        self.x=100
        self.y=100
        self.contents=[]
        self.speed=0.0
        self.set_image()
    def set_image(self):
        self.image = pygame.image.load('sprites/space/'+self.faction+'.png')
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)

            
class Main_Player():
    def __init__(self, kind, serverparent):
        self.myarmy=pygame.sprite.Group()
        self.myships=[]
        self.myarmy=[]
        self.biomatter=0
        self.xp=0
        if kind=='tyranid':
            self.mysprite=Tyranid(serverparent, "Player")
        elif kind=='human':
            self.mysprite=Human(serverparent, "Player")
        self.character=kind
        self.in_ship=False
        self.myquests=Quests()

# rename Player into character
class Character(pygame.sprite.Sprite):
    """Each minion can receive commands from the user and give commands to other minions.
    All minions can level up, earn xp, and be killed.
    For now the variable user is also a minion with the name player.
    Later, add inventory for each minion.
    """
    def __init__(self, kind, serverparent, name="none"):
        """When instance is created set the name and default stats.
        Make a function for default names if no name is entered.
        """
        #global parent
        
        #TODO: get if statements out of __init__,
        #use child classes instead
        pygame.sprite.Sprite.__init__(self)
        
        # remove these when MainPlayer is working:
        #self.myarmy=[]
        self.myarmy=pygame.sprite.Group()
        self.persist=False
        self.duplicates=False
        self.myships=[]
        self.biomatter=0
        self.character=kind
        #
        self.chaos=0
        self.anchor=0
        self.serverparent=serverparent
        self.onlineID=id(self)
        self.eating=False
        self.following=False
        self.mytick=0
        self.rest=0
        self.cooldown=0
        self.moving_count=0
        self.selected=False
        self.attacking=False
        self.go_here="none"
        self.inventory=[]
        self.equipped={"hand":"none", "head":"none", "body":"none"} #equipped list is a dictionary
        self.name=name
        self.xp=0
        self.level=0
        self.health=100
        self.alive=True
        self.tasks=[]
        self.crouch = False
        self.jump=False
        self.kind=kind
        # move this to a better place:
        if self.name=="Player":
            self.x = 400
            self.y = 200
            if kind == "tyranid":
                change_character(self, 'tyranid/player')
            elif kind=="human":
                change_character(self, 'human/player')
            self.controlling=True
            self.age="adult"
            #self.armor=""
            #self.image = pygame.transform.scale(self.image, (70, 130))
            #self.image2= pygame.transform.scale(self.image2,(70, 130))
            # change this to fit
            
        else:
            self.controlling=False
            self.x = random.randint(10,690)
            self.y = random.randint(10,490)
            self.age=0
            if kind == "tyranid":
                change_character(self,'tyranid/kid')
            elif kind=="human":
                change_character(self, 'human/troop')
        self.facing='left'
        self.direction="none"
        print("A {} was born!".format(self.character)) # this lets us know it was successfully created
        global gamevars# current_location
        if type(gamevars.current_location)!=int:
            if self.name=="Player":
                send_to_host(["spawnplayer", self, self.x-gamevars.current_location.gamex, self.y-gamevars.current_location.gamey, gamevars.current_location.name])
            else:
                send_to_host(["spawnsoldier", self, self.x-gamevars.current_location.gamex, self.y-gamevars.current_location.gamey, gamevars.current_location.name])


    def set_image(self):
        if self.kind == "tyranid":
            if self.name == 'Player':
                change_character(self,'tyranid/player')
            else:
                if self.age == 'adult':
                    change_character(self,'tyranid/adult')
                else:
                    change_character(self,'tyranid/kid')
        elif self.kind=="human":
            if self.name == 'Player':
                change_character(self,'human/player')
            else:
                if self.age == 'adult':
                    change_character(self,'human/adult')
                else:
                    change_character(self, 'human/troop')
        
    def set_rect(self):
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
     
    def add_xp(self, more):
        """Adds xp. If xp reaches 100 then level increases by 1 and xp goes down 100."""
        self.xp=self.xp+more
        if self.xp>=100:
            while self.xp>=100:
                self.level=self.level+1
                self.xp=self.xp-100
            return self.level

            
    def heal(self,hlth):
        """Adds health to this minion."""
        self.health=self.health+hlth

    def armor(self): #add input: body or head or sheild
        """Returns the armor as a percentage of damage they take
        1 = take full damage.
        0 = take no damage.
        """
        if self.equipped['body']=="metal":
            return 0.3
        elif self.equipped['body']=="leather":
            return 0.8
        elif self.equipped['body']=="cactus":
            return 2
        elif self.equipped['body']=="paper":
            return 0.95
        elif self.equipped['body']=="studded":
            return 0.75
        elif self.equipped['body']=="chain":
            return 0.5
        else:
            return 1

    #def stab(direction):
    #^^^^erase?        
        
    # Move this to a global function to cut down on transmitted data
    # (each sprite gets sent when created)
    def take_damage(self, damage):
        """Removes health from this minion."""
        if self.alive==True:
            self.health=self.health-(damage*self.armor())
            print(self.name, self.health)
            if self.health <=0:
                self.alive=False
                #self.image=pygame.image.load('sprites/statue/dead.png')
                send_to_host(['killnpc',self.onlineID])
                print("{} has died!".format(self.name))
                global gamevars
                #TODO: dont just remove it, dead sprites list?
                gamevars.user.myarmy.remove(self)
                return 'kill'
        return self.alive

class Human(Character):
    def __init__(self, serverparent, name):
        Character.__init__(self, 'human', serverparent, name)
        change_character(self, 'human/player')

class Tyranid(Character):
    def __init__(self, serverparent, name):
        Character.__init__(self, 'tyranid', serverparent, name)
        change_character(self, 'tyranid/player')
        
class Ork(Character):
    def __init__(self, serverparent, name):
        Character.__init__(self, 'ork', serverparent, name)
        change_character(self, 'ork/player')
        
class Tau(Character):
    def __init__(self, serverparent, name):
        Character.__init__(self, 'tau', serverparent, name)
        change_character(self, 'tau/player')
        
class Eldar(Character):
    def __init__(self, serverparent, name):
        Character.__init__(self, 'eldar', serverparent, name)
        change_character(self, 'eldar/player')
        
class DarkEldar(Character):
    def __init__(self, serverparent, name):
        Character.__init__(self, 'dark_eldar', serverparent, name)
        change_character(self, 'dark_eldar/player')

class Chaos(Character):
    def __init__(self, serverparent, name):
        Character.__init__(self, 'chaos', serverparent, name)
        change_character(self, 'chaos/player')


class Statue(pygame.sprite.Sprite):
    """A statue cannot attack, but can be destroyed."""
    
    def __init__(self, name):
        """When created, set name and default stats."""
        pygame.sprite.Sprite.__init__(self)
        self.persist=False
        self.duplicates=False
        self.serverparent=0
        self.onlineID=id(self)
        self.eating=False
        self.rest=0
        self.cooldown=0
        self.attacking=False
        self.go_here="none"
        self.name=name
        self.health=100
        self.alive=True
        self.x = random.randint(10,690)
        self.y = random.randint(10,490)
        
        
        self.load="sprites/statue/"+str(random.randint(1,4))+'.png'
        self.image = pygame.image.load(self.load)
        
        print("A statue appears.") # this lets you know the object was successfully created
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
        global gamevars
        send_to_host(["spawnstatue", self, self.x-gamevars.current_location.gamex,self.y-gamevars.current_location.gamey, gamevars.current_location.name])

    def set_image(self):
        self.image = pygame.image.load(self.load)
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
    def set_rect(self):
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.x, self.y)
    def take_damage(self, damage):
        """Removes a given amount of health."""
        if self.alive==True:
            self.health=self.health-damage
            print(self.name, self.health)
            if self.health <=0:
                self.alive=False
                send_to_host(['killnpc',self.onlineID])
                self.load='sprites/statue/dead.png'
                self.image=pygame.image.load(self.load)
                print("The {} statue has been destroyed.".format(self.name))
                return 'kill'
                #for guy in npc.sprites():
                #    if guy==self:
                #        npc.remove(guy)
        return self.alive

    def heal(self,hlth):
        """This adds a given amount of health to this statue."""
        self.health=self.health+hlth


class Swarm_attackThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass
        #put the swarm-attack button code in here

class Swarm_eatThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass
        #put the swarm-eat button code in here

class CollidingThread (threading.Thread):
    def __init__(self, guy):
        threading.Thread.__init__(self)
        self.guy=guy
    def run(self):
        pass
        #put swinging function in here 

class UpdatescreenThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass
        #put all screen.blit for loops in here

class WarpmenuThread (threading.Thread):
    """not being used"""
    def __init__(self, crnt):
        threading.Thread.__init__(self)
        self.current=crnt
    def run(self):
        if self.current.space_type!="none":
            tempchoice=input("Press 1 to warp to other solar systems.\n"
                            "Press 2 to land on a planet.\n\n")
            if tempchoice==1:
                print("\n\nKnown solar systems:")
                tmpcount=1
                for spaceplace in gamevars.game_map:
                    print(str(tmpcount)+spaceplace.name)
                    tmpcount+=1
                tempchoice=input("\nEnter the number of the destination.")
                load_space(gamevars.game_map[tempchoice])
            elif tempchoice==2:
                print("\n\nPlanets in the area:")
                tmpcount=1
                for planetplace in gamevars.game_map:
                    print(str(tmpcount)+planetplace.name)
                    tmpcount+=1
                tempchoice=input("\nEnter the number of the destination.")
                load_space(gamevars.current_location.planets[tempchoice])
            else:
                print("Warp cancelled.")

def troop_formations_line(leader, guys):
    #guys=leader.myarmy
    trooplength=len(guys)
    #global user
    #change_character(user.mysprite, "human/charles")
    try:
        unitlength=trooplength//4
        if unitlength>0:
            troopspace=300/unitlength
            troopcount=0
            done_troops=0
            for guy in guys[0: unitlength]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(-60,(-150+troopcount*troopspace))
                #change_character(guy, "human/archers")
                done_troops+=1
            troopcount=0
            for guy in guys[unitlength: unitlength*2]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(120,(-350+troopcount*troopspace))
                #change_character(guy, "human/hwan")
                #pygame.transform.scale(guy.image, (30, 50))
                done_troops+=1
            troopcount=0
            for guy in guys[2*unitlength: unitlength*3]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(150,(-150+troopcount*troopspace))
                #change_character(guy, "human/hwan")
                done_troops+=1
            troopcount=0
            for guy in guys[3*unitlength: unitlength*4]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(120,(50+troopcount*troopspace))
                #change_character(guy, "human/hwan")
                #pygame.transform.scale(guy.image, (30, 50))
                done_troops+=1
            if done_troops<trooplength:
                troop_formations_square(leader, guys[done_troops:])
#         else:
#             guys[0].following=leader
#             guys[0].direction="formation"
#             guys[0].anchor=(-150, 0)
#             guys[1].following=leader
#             guys[1].direction="formation"
#             guys[1].anchor=(0,-150)
#             guys[2].following=leader
#             guys[2].direction="formation"
#             guys[2].anchor=(150, 0)
#             guys[3].following=leader
#             guys[3].direction="formation"
#             guys[3].anchor=(0, 150)
    except IndexError:
        pass



def troop_formations_square(leader, guys):
    #guys=leader.myarmy
    trooplength=len(guys)
    try:
        unitlength=trooplength//4
        if unitlength==2:
            guys[0].following=leader
            guys[0].direction="formation"
            guys[0].anchor=(-150,-100)
            guys[1].following=leader
            guys[1].direction="formation"
            guys[1].anchor=(-150,100)
            guys[2].following=leader
            guys[2].direction="formation"
            guys[2].anchor=(-100,-150)
            guys[3].following=leader
            guys[3].direction="formation"
            guys[3].anchor=(100,-150)
            guys[4].following=leader
            guys[4].direction="formation"
            guys[4].anchor=(150,-100)
            guys[5].following=leader
            guys[5].direction="formation"
            guys[5].anchor=(150,100)
            guys[6].following=leader
            guys[6].direction="formation"
            guys[6].anchor=(-100,150)
            guys[7].following=leader
            guys[7].direction="formation"
            guys[7].anchor=(100,150)
        elif unitlength>=3:
            troopspace=300/unitlength
            troopcount=0
            done_troops=0
            for guy in guys[0: unitlength]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(-150,(-150+troopcount*troopspace))
                done_troops+=1
            troopcount=0
            for guy in guys[unitlength: unitlength*2]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=((-150+troopcount*troopspace),-150)
                done_troops+=1
            troopcount=0
            for guy in guys[2*unitlength: unitlength*3]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(150,(-150+troopcount*troopspace))
                done_troops+=1
            troopcount=0
            for guy in guys[3*unitlength: unitlength*4]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=((-150+troopcount*troopspace),150)
                done_troops+=1
            if done_troops<trooplength:
                troop_formations_square(leader, guys[done_troops:])
        else:
            guys[0].following=leader
            guys[0].direction="formation"
            guys[0].anchor=(-150, 0)
            guys[1].following=leader
            guys[1].direction="formation"
            guys[1].anchor=(0,-150)
            guys[2].following=leader
            guys[2].direction="formation"
            guys[2].anchor=(150, 0)
            guys[3].following=leader
            guys[3].direction="formation"
            guys[3].anchor=(0, 150)
    except IndexError:
        pass


def setplanetpic(planet_type):
    if planet_type=="desert":
        temp_rand=random.randint(1,1)
        return pygame.image.load('sprites/space/planets/desert'+str(temp_rand)+'.png')
    elif planet_type=="grass":
        temp_rand=random.randint(1,2)
        return pygame.image.load('sprites/space/planets/grass'+str(temp_rand)+'.png')
    elif planet_type=="dying":
        temp_rand=random.randint(1,1)
        return pygame.image.load('sprites/space/planets/dying'+str(temp_rand)+'.png')
    elif planet_type=="dead":
        temp_rand=random.randint(1,1)
        return pygame.image.load('sprites/space/planets/dead'+str(temp_rand)+'.png')
    elif planet_type=="water":
        temp_rand=random.randint(1,1)
        return pygame.image.load('sprites/space/planets/water'+str(temp_rand)+'.png')
    elif planet_type=="dry":
        temp_rand=random.randint(1,1)
        return pygame.image.load('sprites/space/planets/dry'+str(temp_rand)+'.png')
    elif planet_type=="scorched":
        temp_rand=random.randint(1,1)
        return pygame.image.load('sprites/space/planets/scorched'+str(temp_rand)+'.png')
    elif planet_type=="burned":
        temp_rand=random.randint(1,1)
        return pygame.image.load('sprites/space/planets/burned'+str(temp_rand)+'.png')
    elif planet_type=='ice':                  # not used yet, but i have the pics ready. need a matching background
        temp_rand=random.randint(1,2)
        return pygame.image.load('sprites/space/planets/ice'+str(temp_rand)+'.png')
    elif planet_type == 'big':
        return pygame.image.load('sprites/space/planets/giant.png')


def fill_background(my_screen):
    #global gamesize, current_location
    #global fullscrn, fullwidth,fullheight
    global gamevars
    gameh=gamevars.gameh
    gamew=gamevars.gamew
    if gamevars.fullscrn==0:
        size=gamevars.gamesize
    elif gamevars.fullscrn==1:
        size=(gamevars.fullwidth,gamevars.fullheight)
        
    ## This is for the background:
    if gamevars.current_location.gamex>0:
        if gamevars.current_location.gamey<=0:
            tempx=gamevars.current_location.gamex
            while tempx<size[0]:
                tempx+=gamew
            for y in range(gamevars.current_location.gamey,size[1]+gameh,gameh):
                if y+gameh>=0:# and y<=size[1]:
                    for x in range(tempx,-gamew,-gamew):
                        my_screen.blit(gamevars.background,(x,y))
        elif gamevars.current_location.gamey>0:
            tempx=gamevars.current_location.gamex
            tempy=gamevars.current_location.gamey
            while tempx<size[0]:
                tempx+=gamew
            while tempy<size[1]:
                tempy+=gameh
            for y in range(tempy,-gameh,-gameh):
                for x in range(tempx,-gamew,-gamew):
                    my_screen.blit(gamevars.background,(x,y))
                    
    elif gamevars.current_location.gamex<=0:
        if gamevars.current_location.gamey<=0:
            for y in range(gamevars.current_location.gamey, size[1]+gameh, gameh):
                if y+gameh>=0 and y<=size[1]:
                    for x in range(gamevars.current_location.gamex, size[0]+gamew, gamew):
                        if x+gamew>=0: #and x<=size[0]:
                            my_screen.blit(gamevars.background, (x, y))
        elif gamevars.current_location.gamey>0:
            tempy=gamevars.current_location.gamey
            while tempy<size[1]:
                tempy+=gameh
            for y in range(tempy,-gameh,-gameh):
                for x in range(gamevars.current_location.gamex,size[0]+gamew,gamew):
                    if x+gamew>=0:# and x<=size[0]:
                        my_screen.blit(gamevars.background,(x,y))
                    
                    

def tyranid_inputs():
    pass

def human_inputs():
    pass

def tau_inputs():
    pass

def ork_inputs():
    pass

def eldar_inputs():
    pass

def darkeldar_inputs():
    pass

def chaos_inputs():
    pass


def user_inputs():
    #global user, current_location
    #global playerkind, online
    #global spawningoffscreen
    #global botbar, dragging
    global gamevars
    user=gamevars.user
    current_location=gamevars.current_location
    botbar=gamevars.botbar
    
    # events for txtbx?

    #this tells you the index number of the keys being pressed
    #    thekeys=pygame.key.get_pressed()
    #    for indexed in thekeys:
    #        if indexed==True:
    #            print(thekeys.index(indexed))

    pushed_keys=pygame.key.get_pressed()


    #TODO if in_ship==False:

    if pushed_keys[119] == True:  # "w" key
        user.mysprite.direction="up"
    elif pushed_keys[115] == True:  # "s" key
        user.mysprite.direction="down"
    elif pushed_keys[97] == True:  # "a" key
        user.mysprite.direction="left"
    elif pushed_keys[100] == True:  # "d" key
        user.mysprite.direction="right"
    else:
        user.mysprite.direction="none"

    if pushed_keys[273] == True:  # "UP" key
        for thing in user.myarmy:
            if thing.selected==True:
                thing.direction = "up"
    elif pushed_keys[274] == True:  # "DOWN" key
        for thing in user.myarmy:
            if thing.selected==True:
                thing.direction = "down"
    elif pushed_keys[276] == True:  # "LEFT" key
        for thing in user.myarmy:
            if thing.selected==True:
                thing.direction = "left"
    elif pushed_keys[275] == True:  # "RIGHT" key
        for thing in user.myarmy:
            if thing.selected==True:
                thing.direction = "right"
    else:
        for thing in user.myarmy:
            if (thing.selected==True
                and thing.direction!="here"
                and thing.direction!="follow"):
                thing.direction = "none"

    events = pygame.event.get()

    for event in events:  # User did something

        if event.type == pygame.QUIT: # User clicked close
            end_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button)==1:      #  Left mouse click
                pos = pygame.mouse.get_pos()
                
                ## check if cursor is on button ##
                
                found=False
                
                for bttn in botbar.myhotkeys:
                        if bttn.rect.collidepoint(pos)==True and type(bttn.contains)!=str:
                            bttn.myclick()
                            found=True 
                
                for bttn in botbar.myleftbuttons:
                    if bttn.rect.collidepoint(pos)==True:
                        bttn.myclick()
                        found=True
                for bttn in botbar.myrightbuttons:
                    if bttn.rect.collidepoint(pos)==True:
                        bttn.myclick()
                        found=True
                
                for menu in botbar.mymenus:
                    if menu.visible==True:
                        for button in menu.mybuttons:
                            if button.rect.collidepoint(pos)==True:
                                button.myclick()
                                found=True 
                        for square in menu.mysquares:
                            if square.rect.collidepoint(pos)==True:
                                square.myclick()
                                found=True 
                        
                # TODO, replace clicked on function, use collide instead
                if found==False and clicked_on(pos)==False:  
                    for kid in user.myarmy:
                        if kid.selected==True:
                            kid.attacking=False
                            kid.eating=False
                            kid.go_here=pos
                            kid.direction="here"
                            
            if event.button==3:       #  Right mouse click
                for kid in user.myarmy:
                    kid.selected=True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if gamevars.dragging!=False:
                pos= pygame.mouse.get_pos()
                for bttn in botbar.myhotkeys:
                    if bttn.rect.collidepoint(pos)==True:
                        unclicked(bttn)
                gamevars.dragging=False

        elif event.type == KEYDOWN:
            #mykeys=pygame.key.get_pressed()
            
            if (event.key==K_a or
                event.key==K_d or
                event.key==K_s or
                event.key==K_w or
                event.key==K_UP or
                event.key==K_DOWN or
                event.key==K_LEFT or
                event.key==K_RIGHT):
                gamevars.keyTime=gamevars.myTick

                
            if event.key == K_BACKSLASH:
                togfullscreen()

            if event.key == K_f:
                for guy in user.myarmy:
                    guy.direction="follow"
                    guy.following=user.mysprite
                    guy.attacking=False
                    guy.eating=False

            if event.key == K_r:
                for guy in user.myarmy:
                    guy.direction="none"
                    guy.attacking=False
                    guy.eating=False

            if event.key == K_z:
                if current_location.space_type=='none':
                    current_location.npc.add(Statue("Statue"))
                else:
                    # this is for "planet assault" mode
                    # TODO this loads the giant planet, 
                    # and a new space matching planets gamex and gamey
                    for planets in current_location.planets:
                        if planets.rect.colliderect(user.mysprite.rect):
                            load_planet_space(planets)
                            current_location=planets
                    
                
            if event.key == K_ESCAPE:
                end_game()

            if event.key == K_e:
                eat(user.mysprite)
                for guy in user.myarmy:
                    if guy.selected==True:
                        eat(guy)
                        
            if event.key == K_SPACE:
                fight(user.mysprite)
                #user.jump = True  # or call a jump function

            if event.key == K_RSHIFT or event.key == K_LSHIFT:
                for guy in user.myarmy:
                    if guy.selected==True:
                        fight(guy)

            if event.key==K_c:
                any_kids=[]
                eat_it=[]
                for each in user.myarmy:
                    if each.age!="adult":
                        any_kids.append(each)
                for thing in current_location.online_npcs:
                    if thing.alive==False:
                        eat_it.append(thing)
                for thing in current_location.npc:
                    if thing.alive==False:
                        eat_it.append(thing)
                if eat_it!=[] and any_kids!=[]:
                    for kid in any_kids:
                        if eat_it!=[]:
                            kid.go_here=eat_it[0].rect.center
                            kid.direction="here"
                            kid.eating=True
                            kid.attacking=False
                            del eat_it[0]
                if eat_it!=[]:
                    for each in user.myarmy:
                        if each.age=="adult":
                            if eat_it!=[]:
                                each.attacking=False
                                each.eating=True
                                each.go_here=eat_it[0].rect.center
                                each.direction="here"
                                del eat_it[0]

            if event.key==K_x:
                any_adults=[]
                kill_it=[]
                for each in user.myarmy:
                    if each.age=="adult":
                        any_adults.append(each)
                for thing in current_location.online_npcs:
                    if thing.alive==True:
                        kill_it.append(thing)
                for thing in current_location.npc:
                    if thing.alive==True:
                        kill_it.append(thing)
                if kill_it!=[] and any_adults!=[]:
                    for each in any_adults:
                        if kill_it!=[]:
                            each.attacking=True
                            each.eating=False
                            each.go_here=kill_it[0].rect.center
                            each.direction="here"
                            del kill_it[0]
                        
                if kill_it!=[]:
                    for each in user.myarmy:
                        if each.age!="adult":
                            if kill_it!=[]:
                                each.attacking=True
                                each.eating=False
                                each.go_here=kill_it[0].rect.center
                                each.direction="here"
                                del kill_it[0]

            #TODO: change how controlling character works,
            # it should not replace the main player sprite
            # with the controlled guy, it's temporary (unless he dies)
            if event.key==K_TAB:
                save_game(gamevars)
                
                # old TAB function:
#                 selected_troops=[]
#                 for guy in user.myarmy:
#                     if guy.age=="adult" and guy.selected==True:
#                         selected_troops.append(guy)
#                 if selected_troops!=[]:
#                     user.mysprite.controlling=False
#                     user.mysprite.selected=False
#                     if user.mysprite.character=='tyranid':
#                         change_character(user.mysprite,"tyranid/adult")
#                     elif user.mysprite.character=='human':
#                         change_character(user.mysprite,"human/adult")
#                     user.mysprite.myarmy.add(user.mysprite)
#                     gamevars.main_players.remove(user.mysprite)
#                     temp_num=random.randint(0,len(selected_troops)-1)
#                     newmainguy=selected_troops[temp_num]
#                     #newmainguy.myarmy=user.myarmy
#                     #user.myarmy=[]
#                     user.mysprite=newmainguy
#                     
#                     gamevars.main_players.append(user.mysprite)
# 
#                     user.myarmy.remove(user.mysprite)
# 
#                     user.mysprite.controlling=True
#                     user.mysprite.selected=False
#                     if user.character=='tyranid':
#                         change_character(user.mysprite,"tyranid/player")
#                     elif user.character=='human':
#                         change_character(user.mysprite,"human/player")
#                     jump_here()

            if event.key==K_p:
                print("You have "+str(len(user.myarmy))+" troops.")

            if event.key==K_o:
                print("There are "+str(len(current_location.npc.sprites()))+" enemies.")
                
            if event.key==K_i:
                print("Your screen location:\n"+
                      "X = "+str(-current_location.gamex)+
                      "\nY = "+str(-current_location.gamey))

            if event.key==K_u:
                if gamevars.spawningoffscreen==False:
                    gamevars.spawningoffscreen=True
                    print("spawning on")
                else:
                    gamevars.spawningoffscreen=False
                    print("spawning off")
                    
                 
                 
            
            if event.key==K_BACKQUOTE:
                user.biomatter+=1000000
                print("YouRich BEEEITCH!!!!")
            

            if event.key==K_BACKSPACE:
                if gamevars.online==False:
                    #online2=True
                    go_online()

            if event.key==K_DELETE:
                if gamevars.online==True:
                    try:
                        #send_to_host('close_me')
                        #sock.send('close'.encode('utf-8'))
                        gamevars.socksend.close()
                        gamevars.sockrec.close()
                        gamevars.online=False
                        remove_online_sprites()
                    except ConnectionResetError:
                        gamevars.online=False
                        print("ERROR: Connection was lost. Please reconnect.")
                        remove_online_sprites()

            if event.key==K_INSERT:
                if gamevars.online==True:
                    try:
                        send_to_host('helllooooo'.encode('utf-8'))
                        #sock.send('hellooooo'.encode('utf-8'))
                    except ConnectionResetError:
                        gamevars.online=False
                        print("ERROR: Connection was lost. Please reconnect.")
                        remove_online_sprites()

            if event.key==K_EQUALS:
                if gamevars.online==True:
                    try:
                        send_to_host('testing')
                        #sock.send('testing'.encode('utf-8'))
                    except ConnectionResetError:
                        gamevars.online=False
                        print("ERROR: Connection was lost. Please reconnect.")
                        remove_online_sprites()
            
            if event.key==K_q:
                if current_location.space_type=="none": # check if its a planet
                    load_space(current_location.parent)
                    #current_location=current_location.parent
                else:
                    for planets in current_location.planets:
                        if planets.rect.colliderect(user.mysprite.rect):
                            load_planet(planets)
                            #current_location=planets
                
            if event.key == K_RETURN:
                if current_location.space_type!="none":
                    #warp=WarpmenuThread(current_location)
                    #warp.start()
                    current_location=warpmenu(current_location)
                    
            if event.key==K_1:
                if type(botbar.hotkey1.contains)!=str:
                    botbar.hotkey1.contains.myclick()
                    
            if event.key==K_2:
                if type(botbar.hotkey2.contains)!=str:
                    botbar.hotkey2.contains.myclick()
            
            if event.key==K_3:
                if type(botbar.hotkey3.contains)!=str:
                    botbar.hotkey3.contains.myclick()
                    
            if event.key==K_4:
                if type(botbar.hotkey4.contains)!=str:
                    botbar.hotkey4.contains.myclick()
                    
            if event.key==K_5:
                if type(botbar.hotkey5.contains)!=str:
                    botbar.hotkey5.contains.myclick()
                    
            if event.key==K_6:
                if type(botbar.hotkey6.contains)!=str:
                    botbar.hotkey6.contains.myclick()
                    
            if event.key==K_7:
                if type(botbar.hotkey7.contains)!=str:
                    botbar.hotkey7.contains.myclick()
                    
            if event.key==K_8:
                if type(botbar.hotkey8.contains)!=str:
                    botbar.hotkey8.contains.myclick()
                
            if event.key==K_9:
                if type(botbar.hotkey9.contains)!=str:
                    botbar.hotkey9.contains.myclick()
                    
            if event.key==K_0:
                if type(botbar.hotkey10.contains)!=str:
                    botbar.hotkey10.contains.myclick()
                    
            if event.key==K_MINUS:
                if type(botbar.hotkey11.contains)!=str:
                    botbar.hotkey11.contains.myclick()
                    
            if event.key==K_EQUALS:
                if type(botbar.hotkey12.contains)!=str:
                    botbar.hotkey12.contains.myclick()
                
                
            # ???? [[
            #if (mykeys[K_`]):
                #ask_player()  # this is what gets the input from the player

            #if (mykeys[K_b]):
                #words_box=eztext.Input(maxlength=45, color=(255,0,0), prompt='type here: ')
                    #boxx(30,50)
                #using_menu=True
                #words_box.typing()

            #if e is pressed:
                #action=True
            #else:
                #action=False
        
            #if p is pressed:  #planning mode  (for commanding and building)
                #who=ask who, map or grid?
                #command(who)
            # ]]

    
def move_me(who):
    global gamevars 
    current_location=gamevars.current_location
    user=gamevars.user
    who.mytick+=1
    if who==user.mysprite:
        if gamevars.toprect.colliderect(user.mysprite.rect) and user.mysprite.direction=="up":
            antimove('up')
        if gamevars.bottomrect.colliderect(user.mysprite.rect) and user.mysprite.direction=="down":
            antimove('down')
        if gamevars.left_rect.colliderect(user.mysprite.rect) and user.mysprite.direction=="left":
            antimove('left')
        if gamevars.right_rect.colliderect(user.mysprite.rect) and user.mysprite.direction=="right":
            antimove('right')
            
    if who.direction == 'right':
        send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
        who.facing="right"
        who.x += 5
        who.rect=who.rect.move(5,0)
        
        # TODO: put these in its own function 'cycle image'
        # less typing in the future
        count=0
        if who.mytick<=2:
            who.image=who.walking_right[count]
        else:
            thistick=who.mytick
            while thistick>2:
                count+=1
                thistick-=2
            try:
                who.image=who.walking_right[count]
            except IndexError:
                who.mytick=1
                who.image=who.walking_right[0]


    elif who.direction == 'down':
        send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
        #this is for the 3d setting:
        
        # TODO: get up and down pics for tyranids,
        # and get rid of this "if != tyranid":
        if who.character!="tyranid":
            who.facing='down'
            count=0
            if who.mytick<=3:
                who.image=who.walking_down[count]
            else:
                thistick=who.mytick
                while thistick>3:
                    count+=1
                    thistick-=3
                try:
                    who.image=who.walking_down[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_down[0]
        who.y += 5
        who.rect=who.rect.move(0,5)
        #this is for the 2d setting:
        #if user.facing == 'left':
        #    user.image=user.lookdown_left
        #if user.facing == 'right':
        #    user.image=user.lookdown_right
    elif who.direction == 'left':
        send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
        who.facing="left"
        who.x -= 5
        who.rect=who.rect.move(-5,0)
        count=0
        if who.mytick<=2:
            who.image=who.walking_left[count]
        else:
            thistick=who.mytick
            while thistick>2:
                count+=1
                thistick-=2
            try:
                who.image=who.walking_left[count]
            except IndexError:
                who.mytick=1
                who.image=who.walking_left[0]
    elif who.direction == 'up':
        send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
        #this is for the 3d setting:
        if who.character!="tyranid":
            who.facing='up'
            count=0
            if who.mytick<=3:
                who.image=who.walking_up[count]
            else:
                thistick=who.mytick
                while thistick>3:
                    count+=1
                    thistick-=3
                try:
                    who.image=who.walking_up[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_up[0]
        who.y -= 5
        who.rect=who.rect.move(0,-5)
        #this is for the 2d setting:
        #if user.facing == 'left':
        #    user.image=user.lookup_left
        #if user.facing == 'right':
        #    user.image=user.lookup_right
    elif who.direction=="none":
        #if user.jump==True
        if who.facing=="right":
            who.image=who.standing_right
        elif who.facing=="left":
            who.image=who.standing_left
        elif who.facing=="down":
            who.image=who.standing_down
        elif who.facing=="up":
            who.image=who.standing_up
    elif who.direction=="follow":
        if who.x<who.following.x-30:
            send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="right"
            who.x += 5
            who.rect=who.rect.move(5,0)
            count=0
            if who.mytick<=2:
                who.image=who.walking_right[count]
            else:
                thistick=who.mytick
                while thistick>2:
                    count+=1
                    thistick-=2
                try:
                    who.image=who.walking_right[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_right[0]
        elif who.x>who.following.x+30:
            send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="left"
            who.x -= 5
            who.rect=who.rect.move(-5,0)
            count=0
            if who.mytick<=2:
                who.image=who.walking_left[count]
            else:
                thistick=who.mytick
                while thistick>2:
                    count+=1
                    thistick-=2
                try:
                    who.image=who.walking_left[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_left[0]
        elif who.y<who.following.y-30:
            send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y += 5
            who.rect=who.rect.move(0,5)
            if who.character!='tyranid':
                who.facing="down"
                count=0
                if who.mytick<=3:
                    who.image=who.walking_down[count]
                else:
                    thistick=who.mytick
                    while thistick>3:
                        count+=1
                        thistick-=3
                    try:
                        who.image=who.walking_down[count]
                    except IndexError:
                        who.mytick=1
                        who.image=who.walking_down[0]
        elif who.y>who.following.y+30:
            send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y -= 5
            who.rect=who.rect.move(0,-5)
            if who.character!='tyranid':
                who.facing="up"
                count=0
                if who.mytick<=3:
                    who.image=who.walking_up[count]
                else:
                    thistick=who.mytick
                    while thistick>3:
                        count+=1
                        thistick-=3
                    try:
                        who.image=who.walking_up[count]
                    except IndexError:
                        who.mytick=1
                        who.image=who.walking_up[0]
        else:
            if who.facing=="right":
                who.image=who.standing_right
            elif who.facing=="left":
                who.image=who.standing_left
            elif who.facing=="down":
                who.image=who.standing_down
            elif who.facing=="up":
                who.image=who.standing_up
    elif who.direction=="here":
        if who.x<who.go_here[0]-5-(who.rect.height/2):
            send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.x += 5
            who.rect=who.rect.move(5,0)
            who.facing="right"
            count=0
            if who.mytick<=2:
                who.image=who.walking_right[count]
            else:
                thistick=who.mytick
                while thistick>2:
                    count+=1
                    thistick-=2
                try:
                    who.image=who.walking_right[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_right[0]
        elif who.x>who.go_here[0]+5-(who.rect.height/2):
            send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="left"
            who.x -= 5
            who.rect=who.rect.move(-5,0)
            count=0
            if who.mytick<=2:
                who.image=who.walking_left[count]
            else:
                thistick=who.mytick
                while thistick>2:
                    count+=1
                    thistick-=2
                try:
                    who.image=who.walking_left[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_left[0]
        elif who.y<who.go_here[1]-5-(who.rect.height/2):
            send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y += 5
            who.rect=who.rect.move(0,5)
            if who.character!='tyranid':
                who.facing="down"
                count=0
                if who.mytick<=3:
                    who.image=who.walking_down[count]
                else:
                    thistick=who.mytick
                    while thistick>3:
                        count+=1
                        thistick-=3
                    try:
                        who.image=who.walking_down[count]
                    except IndexError:
                        who.mytick=1
                        who.image=who.walking_down[0]
        elif who.y>who.go_here[1]+5-(who.rect.height/2):
            send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y -= 5
            who.rect=who.rect.move(0,-5)
            if who.character!='tyranid':
                who.facing="up"
                count=0
                if who.mytick<=3:
                    who.image=who.walking_up[count]
                else:
                    thistick=who.mytick
                    while thistick>3:
                        count+=1
                        thistick-=3
                    try:
                        who.image=who.walking_up[count]
                    except IndexError:
                        who.mytick=1
                        who.image=who.walking_up[0]
        else:
            who.direction="none"
#     elif who.direction=="follow":
#         if who.x<who.following.x-30:
#             send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
#             who.facing="right"
#             who.x += 5
#             who.rect=who.rect.move(5,0)
#             if who.mytick<=2:
#                 who.image=who.walking_rightA
#             elif who.mytick<=4:
#                 who.image=who.walking_rightB
#             elif who.mytick<=6:
#                 who.image=who.walking_rightC
#             else:
#                 who.mytick=0
#         elif who.x>who.following.x+30:
#             send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
#             who.facing="left"
#             who.x -= 5
#             who.rect=who.rect.move(-5,0)
#             if who.mytick<=2:
#                 who.image=who.walking_leftA
#             elif who.mytick<=4:
#                 who.image=who.walking_leftB
#             elif who.mytick<=6:
#                 who.image=who.walking_leftC
#             else:
#                 who.mytick=0
#         elif who.y<who.following.y-30:
#             send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
#             who.y += 5
#             who.rect=who.rect.move(0,5)
#             if who.character!='tyranid':
#                 who.facing="down"
#                 if who.mytick<=3:
#                     who.image=who.walking_downA
#                 elif who.mytick<=6:
#                     who.image=who.walking_downB
#                 else:
#                     who.mytick=0
#         elif who.y>who.following.y+30:
#             send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
#             who.y -= 5
#             who.rect=who.rect.move(0,-5)
#             if who.character!='tyranid':
#                 who.facing="up"
#                 if who.mytick<=3:
#                     who.image=who.walking_upA
#                 elif who.mytick<=6:
#                     who.image=who.walking_upB
#                 else:
#                     who.mytick=0
#         else:
#             if who.facing=="right":
#                 who.image=who.standing_right
#             elif who.facing=="left":
#                 who.image=who.standing_left
#             elif who.facing=="down":
#                 who.image=who.standing_down
#             elif who.facing=="up":
#                 who.image=who.standing_up
                
                
    elif who.direction=="formation":
        if who.x<who.following.x-5+who.anchor[0]:
            send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="right"
            who.x += 5
            who.rect=who.rect.move(5,0)
            count=0
            if who.mytick<=2:
                who.image=who.walking_right[count]
            else:
                thistick=who.mytick
                while thistick>2:
                    count+=1
                    thistick-=2
                try:
                    who.image=who.walking_right[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_right[0]
        elif who.x>who.following.x+5+who.anchor[0]:
            send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="left"
            who.x -= 5
            who.rect=who.rect.move(-5,0)
            count=0
            if who.mytick<=2:
                who.image=who.walking_left[count]
            else:
                thistick=who.mytick
                while thistick>2:
                    count+=1
                    thistick-=2
                try:
                    who.image=who.walking_left[count]
                except IndexError:
                    who.mytick=1
                    who.image=who.walking_left[0]
        elif who.y<who.following.y-5+who.anchor[1]:
            send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y += 5
            who.rect=who.rect.move(0,5)
            if who.character!='tyranid':
                who.facing="down"
                count=0
                if who.mytick<=3:
                    who.image=who.walking_down[count]
                else:
                    thistick=who.mytick
                    while thistick>3:
                        count+=1
                        thistick-=3
                    try:
                        who.image=who.walking_down[count]
                    except IndexError:
                        who.mytick=1
                        who.image=who.walking_down[0]
                
        elif who.y>who.following.y+5+who.anchor[1]:
            send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y -= 5
            who.rect=who.rect.move(0,-5)
            if who.character!='tyranid':
                who.facing="up"
                count=0
                if who.mytick<=3:
                    who.image=who.walking_up[count]
                else:
                    thistick=who.mytick
                    while thistick>3:
                        count+=1
                        thistick-=3
                    try:
                        who.image=who.walking_up[count]
                    except IndexError:
                        who.mytick=1
                        who.image=who.walking_up[0]
        else:
            if who.facing=="right":
                who.image=who.standing_right
            elif who.facing=="left":
                who.image=who.standing_left
            elif who.facing=="down":
                who.image=who.standing_down
            elif who.facing=="up":
                who.image=who.standing_up
    
def togfullscreen():
    #global fullscrn, my_screen, fullwidth, fullheight, botbar, screensquares, user
    global gamevars
    #print(my_screen.get_surface())
    if gamevars.fullscrn == 0:
        gamevars.fullscrn=1
        gamevars.my_screen = pygame.display.set_mode((gamevars.fullwidth,gamevars.fullheight),pygame.FULLSCREEN)
        
        # TODO: move this to botbar.resize
        gamevars.botbar.y=gamevars.fullheight*(4/4.5)
        gamevars.botbar.resize_image(gamevars.fullwidth, gamevars.fullheight)
    elif gamevars.fullscrn == 1:
        #global gamesize
        gamevars.fullscrn=0
        gamevars.my_screen = pygame.display.set_mode(gamevars.gamesize)
        # TODO: move this to botbat.resize
        gamevars.botbar.y=gamevars.gamesize[1]*(4/4.5)
        gamevars.botbar.resize_image(gamevars.gamesize[0], gamevars.gamesize[1])
    for square in gamevars.screensquares:
        square.resize()
    jump_here()
        

def space_display(my_screen):
        #global current_location, main_players
        global gamevars
        current_location=gamevars.current_location
        #main_players=gamevars.main_players
        #after setplanetpic() function is set up, uncomment:
        for it in current_location.planets:
            my_screen.blit(it.planetpic, (it.spacex, it.spacey))
        
        for it in current_location.online_ships:
            try:
                my_screen.blit(it.image, (it.x, it.y))
                #pygame.draw.rect(my_screen,WHITE,it.rect)
            except pygame.error:
                print(it)
                
        for it in current_location.online_troops.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
                #pygame.draw.rect(my_screen,WHITE,it.rect)
            except pygame.error:
                print(it)
                
        for it in current_location.online_npcs.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
                #pygame.draw.rect(my_screen,WHITE,it.rect)
            except pygame.error:
                print(it)
    
        for players in current_location.online_players:
            my_screen.blit(players.image, (players.x, players.y))
            #pygame.draw.rect(my_screen,WHITE,players.rect)

        for ship in gamevars.user.myships:
            my_screen.blit(ship.image, (ship.x, ship.y))
        for guy in gamevars.user.myarmy:
            move_me(guy)
            if guy.age!="adult":
                if guy.age>=1:
                    guy.age="adult"
                    change_character(guy, guy.character+'/adult')
            my_screen.blit(guy.image, (guy.x, guy.y))
            #pygame.draw.rect(my_screen,WHITE,guy.rect)
    
        for it in current_location.npc.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
            except pygame.error:
                print(it)
            #pygame.draw.rect(my_screen,WHITE,it.rect)
    
        #for players in main_players:
        move_me(gamevars.user.mysprite)
        my_screen.blit(gamevars.user.mysprite.image, (gamevars.user.mysprite.x, gamevars.user.mysprite.y))


def planet_display(my_screen):
        global gamevars
        current_location=gamevars.current_location 
        #main_players= gamevars.main_players 
        user=gamevars.user
        if current_location.above_planet==True: #this is if you are in planet assault mode
            my_screen.blit(current_location.big_pic, (current_location.gamex, current_location.gamey))
            
            for it in current_location.online_troops.sprites():
                try:
                    my_screen.blit(it.image, (it.x, it.y))
                    #pygame.draw.rect(my_screen,WHITE,it.rect)
                except pygame.error:
                    print(it)
                    
            for it in current_location.online_npcs.sprites():
                try:
                    my_screen.blit(it.image, (it.x, it.y))
                    #pygame.draw.rect(my_screen,WHITE,it.rect)
                except pygame.error:
                    print(it)
        
            for players in current_location.online_players:
                my_screen.blit(players.image, (players.x, players.y))
                #pygame.draw.rect(my_screen,WHITE,players.rect)
                
            for it in current_location.online_ships:
                try:
                    my_screen.blit(it.image, (it.x, it.y))
                    #pygame.draw.rect(my_screen,WHITE,it.rect)
                except pygame.error:
                    print(it)
                    
        for things in current_location.environment:
            #if things[0]=='buildings':
            for thing in things[1]:
                my_screen.blit(thing.image, (thing.x, thing.y))
            
        for guy in user.myarmy:
            move_me(guy)
            if guy.age!="adult":
                if guy.age>=1:
                    guy.age="adult"
                    change_character(guy, guy.character+'/adult')
            my_screen.blit(guy.image, (guy.x, guy.y))
            #pygame.draw.rect(my_screen,WHITE,guy.rect)
        
        for it in current_location.npc.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
            except pygame.error:
                print(it)
            #pygame.draw.rect(my_screen,WHITE,it.rect)
                
        for it in current_location.online_troops.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
                #pygame.draw.rect(my_screen,WHITE,it.rect)
            except pygame.error:
                print(it)
                
        for it in current_location.online_npcs.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
                #pygame.draw.rect(my_screen,WHITE,it.rect)
            except pygame.error:
                print(it)
    
        for players in current_location.online_players:
            my_screen.blit(players.image, (players.x, players.y))
            #pygame.draw.rect(my_screen,WHITE,players.rect)
    
        for it in current_location.npc.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
            except pygame.error:
                print(it)
            #pygame.draw.rect(my_screen,WHITE,it.rect)
            
        for it in current_location.online_ships:
            try:
                my_screen.blit(it.image, (it.x, it.y))
                #pygame.draw.rect(my_screen,WHITE,it.rect)
            except pygame.error:
                print(it)
                
        for ship in user.myships:
            my_screen.blit(ship.image, (ship.x, ship.y))
    
        move_me(user.mysprite)
        my_screen.blit(user.mysprite.image, (user.mysprite.x, user.mysprite.y))
        
        #pygame.draw.rect(my_screen,(200,200,200),user.mysprite.rect)
        #pygame.draw.rect(my_screen,(200,200,200),toprect)
        #pygame.draw.rect(my_screen,(200,200,200),bottomrect)
        #pygame.draw.rect(my_screen,(200,200,200),left_rect)
        #pygame.draw.rect(my_screen,(200,200,200),right_rect)
    
    
    # delete?  :
    #    for wall in walls:
    #        if user.rect.colliderect(wall.rect):
    #            if user.direction=="right": # Moving right; Hit the left side of the wall
    #                user.direction="none"
    #            if user.direction=="left": # Moving left; Hit the right side of the wall
    #                user.direction="none"
    #            if user.direction=="up": # Moving down; Hit the top side of the wall
    #                user.direction="none"
    #            if user.direction=="right": # Moving up; Hit the bottom side of the wall
    #                user.direction="none"
                    
    #    if (words_box)!="none":
    #        words_box.update(events)
    #        words_box.draw(my_screen)
    #        #my_screen.blit(words_box.image, words_box.position) # add self.contents or self.text
    
    #    for wall in walls:
    #        pygame.draw.rect(my_screen, (RED), wall)
    

     
def player_view(my_screen, botbar):
    #global dragging
    global gamevars
    
    if botbar.visible==True:
        my_screen.blit(botbar.image, (botbar.x, botbar.y))
        
        # Only for testing:
        for bttn in botbar.myleftbuttons:
            if (type(bttn.image) != str and 
                bttn.visible==True):
                my_screen.blit(bttn.image, (bttn.x, bttn.y))
            else:
                pygame.draw.rect(my_screen,(0, 0, 0),bttn.rect)
           
        for bttn in botbar.myrightbuttons:
            if (type(bttn.image) != str and 
                bttn.visible==True):
                my_screen.blit(bttn.image, (bttn.x, bttn.y))
            else:
                pygame.draw.rect(my_screen,(0, 0, 0),bttn.rect)
            
        for square in botbar.myhotkeys:
            if type(square.contains)!=str:
                my_screen.blit(square.contains.image, (square.x, square.y))
            else:
                pygame.draw.rect(my_screen,(0, 0, 0),square.rect)
                
        #TODO: put these in a for-loop through botbar.mymenus:
        for menu in botbar.mymenus:
            if menu.visible==True:
                my_screen.blit(menu.image, (menu.x, menu.y))
                for button in menu.mybuttons:
                    pygame.draw.rect(my_screen,(200, 0, 0),button.rect)
                for square in menu.mysquares:
                    my_screen.blit(square.contains.image, (square.x, square.y))

        if gamevars.dragging!=False:
            posx,posy=pygame.mouse.get_pos()
            posx-=gamevars.dragging.holding.width/2
            posy-=gamevars.dragging.holding.height/2
            my_screen.blit(gamevars.dragging.holding.image, (posx,posy))
    

def warpmenu(current):
    global gamevars
    if current.space_type!="none":
        try:
            tempchoice=int(input("Press 1 to warp to other solar systems.\n"
                           "Press 2 to land on a planet.\n\n"))
            if tempchoice==1:
                print("\n\nKnown solar systems:")
                tmpcount=1
                for spaceplace in gamevars.game_map:
                    if spaceplace==current:
                        print(str(tmpcount)+":  "+spaceplace.name+"   <--current location")
                    else:
                        print(str(tmpcount)+":  "+spaceplace.name)
                    tmpcount+=1
                tempchoice=int(input("\nEnter the number of the destination."))
                load_space(gamevars.game_map[tempchoice-1])
                return gamevars.game_map[tempchoice-1]
            elif tempchoice==2:
                print("\n\nPlanets in the area:    (coordinates)")
                tmpcount=1
                for planetplace in current.planets:
                    print(str(tmpcount)+":  "+planetplace.name +"       ("
                          +str(planetplace.spacex-gamevars.current_location.gamex)
                          +", "+str(planetplace.spacey-gamevars.current_location.gamey)+")")
                    tmpcount+=1
                tempchoice=int(input("\nEnter the number of the destination."))
                load_planet(current.planets[tempchoice-1])
                return current.planets[tempchoice-1]
            else:
                print("Warp cancelled.")
                return current
        except ValueError:
            print("Warp cancelled.")
            return current




    

def spawn_ship(guy):
    """"""
    guy.myships.append(Spaceship(guy.character))
    

def change_character(me, who):
    """This takes a Player and folder containing the pictures
    ("spritetype/spriteage"), then loads the pictures for the sprite.
    """
    # this is a function that searches for left1,left2, until it can't find one
    # also, if next position (right1) doesn't have a pic, use last pic (left1)
    # so if there is only one pic (standing left) it will use it for all positions

    #if me.character=='human':
    load='sprites/'+who
    try:
        me.standing_left = pygame.image.load(load+'/left.png')
    except pygame.error:
        print("Sorry, I can't do that.")
        return
    try:
        me.standing_right= pygame.image.load(load+'/right.png')
    except pygame.error:
        me.standing_right=me.standing_left
    try:
        me.standing_up=pygame.image.load(load+'/standing_up.png')
    except pygame.error:
        me.standing_up=me.standing_left
    try:
        me.standing_down=pygame.image.load(load+'/standing_down.png')
    except pygame.error:
        me.standing_down=me.standing_left
        
    try:
        me.walking_left=[pygame.image.load(load+'/left_running1.png')]
    except pygame.error:
        me.walking_left=[me.standing_left]
    count=2
    done=False
    while not done:
        try:
            me.walking_left.append(pygame.image.load(load+'/left_running{}.png'.format(count)))
            count+=1
        except pygame.error:
            done=True
    try:
        me.walking_right=[pygame.image.load(load+'/right_running1.png')]
    except pygame.error:
        me.walking_right=[me.standing_right]
    count=2
    done=False
    while not done:
        try:
            me.walking_right.append(pygame.image.load(load+'/right_running{}.png'.format(count)))
            count+=1
        except pygame.error:
            done=True

    try:
        me.walking_up=[pygame.image.load(load+'/walking_up1.png')]
    except pygame.error:
        me.walking_up=[me.standing_up]
    count=2
    done=False
    while not done:
        try:
            me.walking_up.append(pygame.image.load(load+'/walking_up{}.png'.format(count)))
            count+=1
        except pygame.error:
            done=True
            
    try:
        me.walking_down=[pygame.image.load(load+'/walking_down1.png')]
    except pygame.error:
        me.walking_down=[me.standing_down]
    count=2
    done=False
    while not done:
        try:
            me.walking_down.append(pygame.image.load(load+'/walking_down{}.png'.format(count)))
            count+=1
        except pygame.error:
            done=True
    
    # for 2D:
    try:
        me.lookup_left= pygame.image.load(load+'/left_lookup.png')
    except pygame.error:
        me.lookup_left= me.standing_left
    try:
        me.lookdown_left= pygame.image.load(load+'/left_lookdown.png')
    except pygame.error:
        me.lookdown_left= me.standing_left
    try:
        me.lookup_right= pygame.image.load(load+'/right_lookup.png')
    except pygame.error:
        me.lookup_right= me.standing_right
    try:
        me.lookdown_right= pygame.image.load(load+'/right_lookdown.png')
    except pygame.error:
        me.lookdown_right= me.standing_right
        
    me.image = me.standing_left
    me.rect = pygame.Rect(me.image.get_rect())
    me.rect.move_ip(me.x, me.y)
        
    # TODO: Delete?  :  
#     elif me.character=="tyranid":
#         load='sprites/'+who
#         me.standing_left = pygame.image.load(load+'/left.png')
#         me.standing_right= pygame.image.load(load+'/right.png')
#         me.walking_leftA= pygame.image.load(load+'/left_runningA.png')
#         me.walking_leftB= pygame.image.load(load+'/left_runningB.png')
#         me.walking_leftC= pygame.image.load(load+'/left_runningC.png')
#         me.walking_rightA= pygame.image.load(load+'/right_runningA.png')
#         me.walking_rightB= pygame.image.load(load+'/right_runningB.png')
#         me.walking_rightC= pygame.image.load(load+'/right_runningC.png')
#         me.lookup_left= pygame.image.load(load+'/left_lookup.png')
#         me.lookup_right= pygame.image.load(load+'/right_lookup.png')
#         me.lookdown_left= pygame.image.load(load+'/left_lookdown.png')
#         me.lookdown_right= pygame.image.load(load+'/right_lookdown.png')
#         # add these functions:
#         #me.jump_leftA=pygame.image.load(load+'/jump_leftA.png')
#         #me.jump_leftB=pygame.image.load(load+'/jump_leftB.png')   # troy is the only one with 3 jump animations
#         #me.jump_rightA=pygame.image.load(load+'/jump_rightA.png') # everybody else only has 1
#         #me.jump_rightB=pygame.image.load(load+'/jump_rightB.png')
#         # separate this next part somehow, too many pictures being loaded for each character
#         # maybe have a function addpic(who, pic)?
#         # That would work well for characters with different numbers of pics
#         # like troy and his 3 jumping pictures
#         me.standing_up=pygame.image.load(load+'/standing_up.png')
#         me.standing_down=pygame.image.load(load+'/standing_down.png')
#         me.image = me.standing_left
#         me.rect = pygame.Rect(me.image.get_rect())
#         me.rect.move_ip(me.x, me.y)


def jump_here():
    """If the player "jumps" to a spot offscreen,
    move everything else in the opposite direction
    to create the illusion of moving the screen to follow the player.
    """
    #TODO: add the ships, online players, and environment to this
    #global current_location, user
    #global left_rect, right_rect, toprect, bottomrect
    global gamevars
    current_location=gamevars.current_location
    user=gamevars.user
    if user.mysprite.x < gamevars.left_rect.width:
        difference=gamevars.left_rect.width-user.mysprite.x
        user.mysprite.x=gamevars.left_rect.width
        user.mysprite.rect=pygame.Rect(user.mysprite.image.get_rect())
        user.mysprite.rect.move_ip(user.mysprite.x,user.mysprite.y)
        current_location.gamex+= difference
        for guy in user.myarmy:
            guy.x += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]+difference,guy.go_here[1])
        for thing in current_location.npc.sprites():
            thing.x += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in current_location.online_troops:
            guy.x += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]+difference,guy.go_here[1])
        for thing in current_location.online_npcs:
            thing.x += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for things in current_location.environment:
            for thing in things[1]:
                thing.x += difference
                #TODO: fix these
                #thing.rect.move_ip(thing.x,thing.y)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacex+= difference
    elif user.mysprite.x > gamevars.right_rect.x:
        difference=user.mysprite.x-gamevars.right_rect.x
        user.mysprite.x=gamevars.right_rect.x
        user.mysprite.rect=pygame.Rect(user.mysprite.image.get_rect())
        user.mysprite.rect.move_ip(user.mysprite.x,user.mysprite.y)
        current_location.gamex-= difference
        for guy in user.myarmy:
            guy.x -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]-difference,guy.go_here[1])
        for thing in current_location.npc.sprites():
            thing.x -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in current_location.online_troops:
            guy.x -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]-difference,guy.go_here[1])
        for thing in current_location.online_npcs:
            thing.x -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for things in current_location.environment:
            for thing in things[1]:
                thing.x -= difference
                #thing.rect.move_ip(thing.x,thing.y)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacex-= difference
    if user.mysprite.y < gamevars.toprect.height:
        difference=gamevars.toprect.height-user.mysprite.y
        user.mysprite.y=gamevars.toprect.height
        user.mysprite.rect=pygame.Rect(user.mysprite.image.get_rect())
        user.mysprite.rect.move_ip(user.mysprite.x,user.mysprite.y)
        current_location.gamey+= difference
        for guy in user.myarmy:
            guy.y += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]+difference)
        for thing in current_location.npc.sprites():
            thing.y += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in current_location.online_troops:
            guy.y += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]+difference)
        for thing in current_location.online_npcs:
            thing.y += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for things in current_location.environment:
            for thing in things[1]:
                thing.y += difference
                #thing.rect.move_ip(thing.x,thing.y)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacey+= difference
    elif user.mysprite.y > gamevars.bottomrect.y:
        difference=user.mysprite.y-gamevars.bottomrect.y
        user.mysprite.y=gamevars.bottomrect.y
        user.mysprite.rect=pygame.Rect(user.mysprite.image.get_rect())
        user.mysprite.rect.move_ip(user.mysprite.x,user.mysprite.y)
        current_location.gamey-= difference
        for guy in user.myarmy:
            guy.y -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]-difference)
        for thing in current_location.npc.sprites():
            thing.y -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in current_location.online_troops:
            guy.y -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]-difference)
        for thing in current_location.online_npcs:
            thing.y -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for things in current_location.environment:
            for thing in things[1]:
                thing.y -= difference
                #thing.rect.move_ip(thing.x,thing.y)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacey-= difference
        

def spawnoffscreen(direction):
    #global spawningoffscreen, current_location, gamesize
    global gamevars
    if gamevars.spawningoffscreen==True:
        if direction=="up":
            if (random.randint(1,25))==1:
                newguy=Statue("Statue")
                newguy.y=-50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                gamevars.current_location.npc.add(newguy)
        elif direction=="down":
            if (random.randint(1,40))==1:
                newguy=Statue("Statue")
                newguy.y=gamevars.gamesize[1]+50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                gamevars.current_location.npc.add(newguy)
        if direction=="left":
            if (random.randint(1,1))==1:
                newguy=Statue("Statue")
                newguy.x=-50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                gamevars.current_location.npc.add(newguy)
        elif direction=="right":
            if (random.randint(1,50))==1:
                newguy=Statue("Statue")
                newguy.x=gamevars.gamesize[0]+50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                gamevars.current_location.npc.add(newguy)
        try:
            send_to_host(["movenpc", newguy.onlineID, newguy.x-gamevars.current_location.gamex,newguy.y-gamevars.current_location.gamey])
        except UnboundLocalError:
            pass


def antimove(direction):
    global gamevars
    current_location=gamevars.current_location
    spawnoffscreen(direction)
    user=gamevars.user
    if direction=="up":
        current_location.gamey+=5
        user.mysprite.y += 5
        user.mysprite.rect=user.mysprite.rect.move(0,5)
        for things in current_location.environment:
            for thing in things[1]:
                thing.y += 5
                #thing.rect=thing.rect.move(0,5)
        for ship in user.myships:
            ship.y += 5
            #ship.rect=ship.rect.move(0,5)
        for guy in user.myarmy:
            guy.y += 5
            guy.rect=guy.rect.move(0,5)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]+5)
        for thing in current_location.npc.sprites():
            thing.y += 5
            thing.rect=thing.rect.move(0,5)
        for players in current_location.online_players:
            players.y += 5
            players.rect=players.rect.move(0,5)
        for guy in current_location.online_troops.sprites():
            guy.y += 5
            guy.rect=guy.rect.move(0,5)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]+5)
        for thing in current_location.online_npcs.sprites():
            thing.y += 5
            thing.rect=thing.rect.move(0,5)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacey+= 5
                it.rect=it.rect.move(0,5)
    if direction=="down":
        current_location.gamey-=5
        user.mysprite.y -= 5
        user.mysprite.rect=user.mysprite.rect.move(0,-5)
        for things in current_location.environment:
            for thing in things[1]:
                thing.y -= 5
                #thing.rect=thing.rect.move(0,-5)
        for ship in user.myships:
            ship.y -= 5
            #ship.rect=ship.rect.move(0,-5)
        for guy in user.myarmy:
            guy.y -= 5
            guy.rect=guy.rect.move(0,-5)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]-5)
        for thing in current_location.npc.sprites():
            thing.y -= 5
            thing.rect=thing.rect.move(0,-5)
        for players in current_location.online_players:
            players.y -= 5
            players.rect=players.rect.move(0,-5)
        for guy in current_location.online_troops.sprites():
            guy.y -= 5
            guy.rect=guy.rect.move(0,-5)
        for thing in current_location.online_npcs.sprites():
            thing.y -= 5
            thing.rect=thing.rect.move(0,-5)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacey-= 5
                it.rect=it.rect.move(0,-5)
    if direction=="right":
        current_location.gamex-=5
        user.mysprite.x -= 5
        user.mysprite.rect=user.mysprite.rect.move(-5,0)
        for things in current_location.environment:
            for thing in things[1]:
                thing.x -= 5
                #thing.rect=thing.rect.move(-5,0)
        for ship in user.myships:
            ship.x -= 5
            #ship.rect=ship.rect.move(-5,0)
        for guy in user.myarmy:
            guy.x -= 5
            guy.rect=guy.rect.move(-5,0)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]-5,(guy.go_here[1]))
        for thing in current_location.npc.sprites():
            thing.x -= 5
            thing.rect=thing.rect.move(-5,0)
        for players in current_location.online_players:
            players.x -= 5
            players.rect=players.rect.move(-5,0)
        for guy in current_location.online_troops.sprites():
            guy.x -= 5
            guy.rect=guy.rect.move(-5,0)
        for thing in current_location.online_npcs.sprites():
            thing.x -= 5
            thing.rect=thing.rect.move(-5,0)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacex-= 5
                it.rect=it.rect.move(-5,0)
    if direction=="left":
        current_location.gamex+=5
        user.mysprite.x += 5
        user.mysprite.rect=user.mysprite.rect.move(5,0)
        for things in current_location.environment:
            for thing in things[1]:
                thing.x += 5
                #thing.rect=thing.rect.move(5,0)
        for ship in user.myships:
            ship.x += 5
            #ship.rect=ship.rect.move(5,0)
        for guy in user.myarmy:
            guy.x += 5
            guy.rect=guy.rect.move(5,0)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]+5,(guy.go_here[1]))
        for thing in current_location.npc.sprites():
            thing.x += 5
            thing.rect=thing.rect.move(5,0)
        for players in current_location.online_players:
            players.x += 5
            players.rect=players.rect.move(5,0)
        for guy in current_location.online_troops.sprites():
            guy.x += 5
            guy.rect=guy.rect.move(5,0)
        for thing in current_location.online_npcs.sprites():
            thing.x += 5
            thing.rect=thing.rect.move(5,0)
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacex+= 5
                it.rect=it.rect.move(5,0)
                        

def clicked_on(position):
    global gamevars
    top=gamevars.user.mysprite.rect.top
    bottom=gamevars.user.mysprite.rect.bottom
    left=gamevars.user.mysprite.rect.left
    right=gamevars.user.mysprite.rect.right
    if (left<position[0]
        and position[0]<right
        and top<position[1]
        and position[1]<bottom):
        for guy in gamevars.user.myarmy:
            guy.selected=False
        return True
    go_here=False
    for thing in gamevars.current_location.npc:
        top=thing.rect.top
        bottom=thing.rect.bottom
        left=thing.rect.left
        right=thing.rect.right
        if (left<position[0]
            and position[0]<right
            and top<position[1]
            and position[1]<bottom):
            go_here=thing
    if go_here!=False:
        attack_it(go_here, position)
        return True
    else:
        for thing in gamevars.user.myarmy:
            top=thing.rect.top
            bottom=thing.rect.bottom
            left=thing.rect.left
            right=thing.rect.right
            if left<position[0] and position[0]<right and top<position[1] and position[1]<bottom:
                if thing.selected==False:
                    thing.selected=True
                    return True
                elif thing.selected==True:
                    thing.selected=False
                    return True
    return False

def attack_it(it, pos):
    global gamevars
    for guy in gamevars.user.myarmy:
        if guy.selected==True:
            if it.alive==False:
                eat(guy)
                guy.eating=True
                guy.attacking=False
            else:
                guy.eating=False
                guy.attacking=True
            guy.go_here=pos
            guy.direction='here'


def swinging():
    #global current_location, user
    global gamevars
    for guy in gamevars.user.myarmy:
        if guy.attacking==True:
            for thing in gamevars.current_location.npc:
                if thing.alive==True:
                    if guy.rect.colliderect(thing.rect):
                        testing_reasons=thing.take_damage(25)
                        if testing_reasons=='kill':
                            gamevars.user.myquests.doneflags('kill npc')
                        #    guy.attacking=False
            for thing in gamevars.current_location.online_npcs:
                if thing.alive==True:
                    if guy.rect.colliderect(thing.rect):
                        testing_reasons=thing.take_damage(25)
                        if testing_reasons=='kill':
                            gamevars.user.myquests.doneflags('kill npc')
                        #   guy.attacking=False
        if guy.eating==True:
            eat(guy)

def fight(who):
    global gamevars #current_location
    #peeps=pygame.sprite.spritecollideany(who, main_player, False)
    peeps=[]
    for guy in gamevars.current_location.npc:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for guy in gamevars.current_location.online_npcs:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for peep in peeps:
        if peep.take_damage(25) == 'kill':
            gamevars.user.myquests.doneflags('kill npc')
        send_to_host(['attack', peep.onlineID, 25])   


def eat(who):
    global gamevars
    current_location=gamevars.current_location
    user=gamevars.user
    peeps=[]
    for guy in current_location.npc:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for guy in current_location.online_npcs:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for peep in peeps:
        if peep.health<=0:
            send_to_host(["deletenpc", peep.onlineID])
            current_location.npc.remove(peep)
            current_location.online_npcs.remove(peep)
            if who.name=="Player" or who.name=='new':
                who.biomatter = who.biomatter+100
                print("Biomatter: "+str(who.biomatter))
            else:
                if who.age=="adult":
                    #mydad=who.groups()[0]
                    user.biomatter = user.biomatter+100
                    print("Biomatter: "+str(user.biomatter))
                else:
                    who.age=who.age+1
            
            del peep
        #else:
        #   print("You can't eat something that's not dead yet.")


def spawn_npcs(number, kind):
    pass
#     """This spawns a given number of
#     characters and returns them in a list.
#     """
#     spawning=[]
#     for i in range(number):
#         #replace with pygame group function
#         spawning.append(Character(kind))
#     return spawning

    
def load_planet_space(level):
    #global background, gamew, gameh, current_location
    global gamevars
    send_to_host(["new_location", level, gamevars.current_location])
    gamevars.current_location=level
    background= pygame.image.load('sprites/space/background'+str(level.parent.space_type)+'.png')
    #level.background=background
    gamevars.gamew, gamevars.gameh = background.get_size()
    #print(level.big_pic.get_size())
    level.gamex=-1032
    level.gamey=-1032
    
    #TODO: there needs to be a new list for above planet stuff
    # anything in level.environment gets scaled down (and different images?)
    # later 'on planet' functions will need to check this variable:
    level.above_planet=True
        
        
def load_space(level):
    """Takes a "Space" object and loads it."""
    #global background, game_map, gamew, gameh, current_location
    global gamevars
    old=gamevars.current_location
    gamevars.current_location=level
    send_to_host(["new_location", gamevars.current_location, old])
    gamevars.background= pygame.image.load('sprites/space/background'+str(level.space_type)+'.png')
    gamevars.gamew, gamevars.gameh = gamevars.background.get_size()

    
    

def load_planet(level):
    #global background, gamew, gameh, current_location
    global gamevars
    old=gamevars.current_location
    send_to_host(["new_location", level, old])
    level.above_planet=False
    if level.planet_type=='grass':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed1.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    elif level.planet_type=='dying':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed2.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    elif level.planet_type=='dry':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed3.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    elif level.planet_type=='water':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed4.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    if level.planet_type=='dead':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed5.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    if level.planet_type=='scorched':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed6.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    if level.planet_type=='burned':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed7.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    if level.planet_type=='desert':
        gamevars.background= pygame.image.load('sprites/Background/backgrounddetailed8.png')
        level.background=gamevars.background
        gamevars.gamew, gamevars.gameh = gamevars.background.get_size()
    gamevars.current_location=level


def ask_player(this_screen, gsize, menu='main'):
    """Temporary function, will be replaced by main menu function"""
    fullscrn = 0
    fullwidth = GetSystemMetrics(0)
    fullheight = GetSystemMetrics(1)
    width,height=this_screen.get_size()
    online = False
    can_save = True
    world='default'
    
################### CREATE MENU BUTTONS ####################### 

#     newgamebutton = Menu_Button('newgamebutton', 'startmenu', width/4, height*1/4)
#     newgamebutton.width=gsize[0]//2
#     newgamebutton.height=gsize[1]//8
#     newgamebutton.rect=pygame.Rect(newgamebutton.x, newgamebutton.y, newgamebutton.width, newgamebutton.height)
#     newgamebutton.image = pygame.transform.scale(pygame.image.load(newgamebutton.pic), (newgamebutton.width,newgamebutton.height))
# 
#     loadgamebutton = Menu_Button('loadgamebutton', 'startmenu', width/4, height/2)
#     loadgamebutton.width=gsize[0]//2
#     loadgamebutton.height=gsize[1]//8
#     loadgamebutton.rect=pygame.Rect(loadgamebutton.x, loadgamebutton.y, loadgamebutton.width, loadgamebutton.height)
#     loadgamebutton.image = pygame.transform.scale(pygame.image.load(loadgamebutton.pic), (loadgamebutton.width,loadgamebutton.height))
#     
#     quitgamebutton = Menu_Button('quitgamebutton', 'startmenu', width/4, height*3/4)
#     quitgamebutton.width=gsize[0]//2
#     quitgamebutton.height=gsize[1]//8
#     quitgamebutton.rect=pygame.Rect(quitgamebutton.x, quitgamebutton.y, quitgamebutton.width, quitgamebutton.height)
#     quitgamebutton.image = pygame.transform.scale(pygame.image.load(quitgamebutton.pic), (quitgamebutton.width,quitgamebutton.height))
#     
#     buttnsA=[newgamebutton, loadgamebutton, quitgamebutton]

    #TODO: clean this mess up:
    #make all pic settings like this for this menu, for consistency?
    newworldbutton = Menu_Button('newworldbutton', 'startmenu', width/4, height*1/6)
    newworldbutton.pic = 'sprites/ui/newworldbutton.png'
    newworldbutton.width=gsize[0]//2
    newworldbutton.height=gsize[1]//8
    newworldbutton.sizeratio=(newworldbutton.width/width,newworldbutton.height/height)
    newworldbutton.rect=pygame.Rect(newworldbutton.x, newworldbutton.y, newworldbutton.width, newworldbutton.height)
    newworldbutton.image = pygame.transform.scale(pygame.image.load(newworldbutton.pic), (newworldbutton.width,newworldbutton.height))

    joinworldbutton = Menu_Button('joinworldbutton', 'startmenu', width/4, height*2/6)
    joinworldbutton.pic = 'sprites/ui/joinworldbutton.png'
    joinworldbutton.width=gsize[0]//2
    joinworldbutton.height=gsize[1]//8
    joinworldbutton.sizeratio=(joinworldbutton.width/width,joinworldbutton.height/height)
    joinworldbutton.rect=pygame.Rect(joinworldbutton.x, joinworldbutton.y, joinworldbutton.width, joinworldbutton.height)
    joinworldbutton.image = pygame.transform.scale(pygame.image.load(joinworldbutton.pic), (joinworldbutton.width,joinworldbutton.height))
    
    buildworldbutton = Menu_Button('buildworldbutton', 'startmenu', width/4, height*3/6)
    buildworldbutton.pic = 'sprites/ui/buildworldbutton.png'
    buildworldbutton.width=gsize[0]//2
    buildworldbutton.height=gsize[1]//8
    buildworldbutton.sizeratio=(buildworldbutton.width/width,buildworldbutton.height/height)
    buildworldbutton.rect=pygame.Rect(buildworldbutton.x, buildworldbutton.y, buildworldbutton.width, buildworldbutton.height)
    buildworldbutton.image = pygame.transform.scale(pygame.image.load(buildworldbutton.pic), (buildworldbutton.width,buildworldbutton.height))
    
    settingsbutton = Menu_Button('settingsbutton', 'startmenu', width/4, height*4/6)
    settingsbutton.pic = 'sprites/ui/settingsbutton.png'
    settingsbutton.width=gsize[0]//2
    settingsbutton.height=gsize[1]//8
    settingsbutton.sizeratio=(settingsbutton.width/width,settingsbutton.height/height)
    settingsbutton.rect=pygame.Rect(settingsbutton.x, settingsbutton.y, settingsbutton.width, settingsbutton.height)
    settingsbutton.image = pygame.transform.scale(pygame.image.load(settingsbutton.pic), (settingsbutton.width,settingsbutton.height))
    
    quitgamebutton = Menu_Button('quitgamebutton', 'startmenu', width/4, height*5/6)
    quitgamebutton.width=gsize[0]//2
    quitgamebutton.height=gsize[1]//8
    quitgamebutton.sizeratio=(quitgamebutton.width/width,quitgamebutton.height/height)
    quitgamebutton.rect=pygame.Rect(quitgamebutton.x, quitgamebutton.y, quitgamebutton.width, quitgamebutton.height)
    quitgamebutton.image = pygame.transform.scale(pygame.image.load(quitgamebutton.pic), (quitgamebutton.width,quitgamebutton.height))
    
    buttnsA=[newworldbutton, joinworldbutton, buildworldbutton, settingsbutton, quitgamebutton]
    
    mainmenubutton = Menu_Button('mainmenubutton', 'startmenu', 0, 0)
    mainmenubutton.pic = 'sprites/ui/mainmenubutton.png'
    mainmenubutton.width=gsize[0]//4
    mainmenubutton.height=gsize[1]//8
    mainmenubutton.sizeratio=(mainmenubutton.width/width,mainmenubutton.height/height)
    mainmenubutton.rect=pygame.Rect(mainmenubutton.x, mainmenubutton.y, mainmenubutton.width, mainmenubutton.height)
    mainmenubutton.image = pygame.transform.scale(pygame.image.load(mainmenubutton.pic), (mainmenubutton.width,mainmenubutton.height))

    playonlinebutton = Menu_Button('playonlinebutton', 'startmenu', width/4, height/3)
    playonlinebutton.pic = 'sprites/ui/playonlinebutton.png'
    playonlinebutton.width=gsize[0]//2
    playonlinebutton.height=gsize[1]//8
    playonlinebutton.sizeratio=(playonlinebutton.width/width,playonlinebutton.height/height)
    playonlinebutton.rect=pygame.Rect(playonlinebutton.x, playonlinebutton.y, playonlinebutton.width, playonlinebutton.height)
    playonlinebutton.image = pygame.transform.scale(pygame.image.load(playonlinebutton.pic), (playonlinebutton.width,playonlinebutton.height))

    playofflinebutton = Menu_Button('playofflinebutton', 'startmenu', width/4, height/3)
    playofflinebutton.pic = 'sprites/ui/playofflinebutton.png'
    playofflinebutton.width=gsize[0]//2
    playofflinebutton.height=gsize[1]//8
    playofflinebutton.sizeratio=(playofflinebutton.width/width,playofflinebutton.height/height)
    playofflinebutton.rect=pygame.Rect(playofflinebutton.x, playofflinebutton.y, playofflinebutton.width, playofflinebutton.height)
    playofflinebutton.image = pygame.transform.scale(pygame.image.load(playofflinebutton.pic), (playofflinebutton.width,playofflinebutton.height))
    
    cansavebutton = Menu_Button('cansavebutton', 'startmenu', width/4, height/2)
    cansavebutton.pic = 'sprites/ui/cansavebutton.png'
    cansavebutton.width=gsize[0]//2
    cansavebutton.height=gsize[1]//8
    cansavebutton.sizeratio=(cansavebutton.width/width,cansavebutton.height/height)
    cansavebutton.rect=pygame.Rect(cansavebutton.x, cansavebutton.y, cansavebutton.width, cansavebutton.height)
    cansavebutton.image = pygame.transform.scale(pygame.image.load(cansavebutton.pic), (cansavebutton.width,cansavebutton.height))
    
    nosavebutton = Menu_Button('nosavebutton', 'startmenu', width/4, height/2)
    nosavebutton.pic = 'sprites/ui/nosavebutton.png'
    nosavebutton.width=gsize[0]//2
    nosavebutton.height=gsize[1]//8
    nosavebutton.sizeratio=(nosavebutton.width/width,nosavebutton.height/height)
    nosavebutton.rect=pygame.Rect(nosavebutton.x, nosavebutton.y, nosavebutton.width, nosavebutton.height)
    nosavebutton.image = pygame.transform.scale(pygame.image.load(nosavebutton.pic), (nosavebutton.width,nosavebutton.height))
    
    defaultworldbutton = Menu_Button('defaultworldbutton', 'startmenu', width/8, height*5/6)
    defaultworldbutton.pic = 'sprites/ui/defaultworldbutton.png'
    defaultworldbutton.width=gsize[0]//4
    defaultworldbutton.height=gsize[1]//8
    defaultworldbutton.sizeratio=(defaultworldbutton.width/width,defaultworldbutton.height/height)
    defaultworldbutton.rect=pygame.Rect(defaultworldbutton.x, defaultworldbutton.y, defaultworldbutton.width, defaultworldbutton.height)
    defaultworldbutton.image = pygame.transform.scale(pygame.image.load(defaultworldbutton.pic), (defaultworldbutton.width,defaultworldbutton.height))
    
    customworldbutton = Menu_Button('customworldbutton', 'startmenu', width/8+width//4, height*5/6)
    customworldbutton.pic = 'sprites/ui/customworldbutton.png'
    customworldbutton.width=gsize[0]//4
    customworldbutton.height=gsize[1]//8
    customworldbutton.sizeratio=(customworldbutton.width/width,customworldbutton.height/height)
    customworldbutton.rect=pygame.Rect(customworldbutton.x, customworldbutton.y, customworldbutton.width, customworldbutton.height)
    customworldbutton.image = pygame.transform.scale(pygame.image.load(customworldbutton.pic), (customworldbutton.width,customworldbutton.height))
    
    savedworldbutton = Menu_Button('savedworldbutton', 'startmenu', width/8+width//2, height*5/6)
    savedworldbutton.pic = 'sprites/ui/savedworldbutton.png'
    savedworldbutton.width=gsize[0]//4
    savedworldbutton.height=gsize[1]//8
    savedworldbutton.sizeratio=(savedworldbutton.width/width,savedworldbutton.height/height)
    savedworldbutton.rect=pygame.Rect(savedworldbutton.x, savedworldbutton.y, savedworldbutton.width, savedworldbutton.height)
    savedworldbutton.image = pygame.transform.scale(pygame.image.load(savedworldbutton.pic), (savedworldbutton.width,savedworldbutton.height))
    
    buttnsB=[mainmenubutton,
             playonlinebutton, 
             playofflinebutton, 
             cansavebutton, 
             nosavebutton, 
             defaultworldbutton, 
             customworldbutton, 
             savedworldbutton]
    
    
    pic=pygame.image.load('sprites/choose.png')
    pic = pygame.transform.scale(pic, gsize)
    button1=Menu_Button('button1', 'startmenu', width/4, height/25)
    button1.width=gsize[0]//6
    button1.height=gsize[1]//6
    button1.rect=pygame.Rect(button1.x, button1.y, button1.width, button1.height)
    button2=Menu_Button('button2', 'startmenu', (width*3/4)-(width//6), height/25)
    button2.width=width//6
    button2.height=gsize[1]//6
    button2.rect=pygame.Rect(button2.x, button2.y, button2.width, button2.height)
    button3=Menu_Button('button3', 'startmenu', (width/17), height/3.4)
    button3.width=gsize[0]//6
    button3.height=gsize[1]//6
    button3.rect=pygame.Rect(button3.x, button3.y, button3.width, button3.height)
    button4=Menu_Button('button4', 'startmenu', (width*13.5/17), height/3.4)
    button4.width=gsize[0]//6
    button4.height=gsize[1]//6
    button4.rect=pygame.Rect(button4.x, button4.y, button4.width, button4.height)
    button5=Menu_Button('button5', 'startmenu', (width/8), height*2.5/4)
    button5.width=gsize[0]//6
    button5.height=gsize[1]//6
    button5.rect=pygame.Rect(button5.x, button5.y, button5.width, button5.height)
    button6=Menu_Button('button6', 'startmenu', (width*5.8/8), height*2.5/4)
    button6.width=gsize[0]//6
    button6.height=gsize[1]//6
    button6.rect=pygame.Rect(button6.x, button6.y, button6.width, button6.height)
    button7=Menu_Button('button7', 'startmenu', (width/2)-width/12, height*5.45/7)
    button7.width=gsize[0]//6
    button7.height=gsize[1]//6
    button7.rect=pygame.Rect(button7.x, button7.y, button7.width, button7.height)
    buttnsC=[button1, button2, button3, button4, button5, button6, button7]
    
    done=False
    while done==False:
        
################### INPUT ####################### 

        # this tells you the index number of the keys being pressed
#         thekeys=pygame.key.get_pressed()
#         for indexed in thekeys:
#             if indexed==True:
#                 print(thekeys.index(indexed))
              
        events = pygame.event.get()
    
        for event in events:  # User did something
            if event.type == pygame.QUIT: # User clicked close
                end_game()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button)==1:
                    pos = pygame.mouse.get_pos()
                    #print(pos)
                    
                    if menu == 'main':
                        for bttn in buttnsA:
                            if bttn.rect.collidepoint(pos)==True:
#                                 if bttn.name == 'newworldbutton':
#                                     menu = 'race'
#                                 elif bttn.name == 'joinworldbutton':
#                                     return ('loadgame',fullscrn)
                                if bttn.name == 'newworldbutton':
                                    menu = 'new'
                                    break
                                elif bttn.name == 'joinworldbutton':
                                    #TODO: for now players have to make new character:
                                    menu = 'race'
                                    online = 'join'
                                elif bttn.name == 'buildworldbutton':
                                    #TODO: this needs to be moved to main game loop
                                    build_world()
                                elif bttn.name == 'settingsbutton':
                                    print("not yet")
                                elif bttn.name == 'quitgamebutton':
                                    end_game()
                    elif menu == 'new':
                        for bttn in buttnsB:
                            if bttn.rect.collidepoint(pos)==True:
#                                 if bttn.name == 'newworldbutton':
#                                     menu = 'race'
#                                 elif bttn.name == 'joinworldbutton':
#                                     return ('loadgame',fullscrn)
                                if bttn.name == 'mainmenubutton':
                                    menu = 'main'
                                elif bttn.name == 'playonlinebutton' and online==True:
                                    online = False
                                    break
                                elif bttn.name == 'playofflinebutton' and online==False:
                                    online = True
                                    break
                                elif bttn.name == 'cansavebutton'and can_save==True:
                                    can_save=False
                                    break
                                elif bttn.name == 'nosavebutton' and can_save==False:
                                    can_save=True
                                    break
                                elif bttn.name == 'defaultworldbutton':
                                    menu = 'race'
                                elif bttn.name == 'customworldbutton':
                                    menu = 'race'
                                    #TODO: switch to other screen
                                    world = input('\nEnter the name of the custom world\n')
                                    print('\nGame resumed')
                                    print('------------')
                                elif bttn.name == 'savedworldbutton':
                                    if online==True:
                                        return ('loadgameonline',fullscrn) #TODO: return can_save
                                    else:
                                        return ('loadgame',fullscrn)
                    elif menu == 'race':
                        for bttn in buttnsC:
                            if bttn.rect.collidepoint(pos)==True:
                                do_it=bttn.myclick()
                                if world=='default':
                                    if do_it != None:
                                        done=True
                                        return ([online,bttn.myclick()], fullscrn)
                                else:
                                    if do_it != None:
                                        done=True
                                        return (['custom', world, online,bttn.myclick()], fullscrn)
                            
                        
                # this will go back a page just like backspace:
#                 if event.button==3:
                    
            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    end_game()

                if event.key==K_BACKSLASH:
                    if fullscrn==0:
                        fullscrn=1
                        this_screen = pygame.display.set_mode((fullwidth,fullheight),pygame.FULLSCREEN)
                        pic = pygame.transform.scale(pic, (fullwidth,fullheight))
                    elif fullscrn==1:
                        fullscrn=0
                        this_screen = pygame.display.set_mode(gsize)
                        pic = pygame.transform.scale(pic, gsize)
                        
                    width, height=this_screen.get_size()
                    
                    
#                     newgamebutton.x=width/4
#                     newgamebutton.y=fullheight/4
#                     newgamebutton.width=width//2
#                     newgamebutton.height=height//8
#                     newgamebutton.rect=pygame.Rect(newgamebutton.x, newgamebutton.y, newgamebutton.width, newgamebutton.height)
#                     newgamebutton.image = pygame.transform.scale(newgamebutton.image, (newgamebutton.width,newgamebutton.height))
#                     
#                     loadgamebutton.x=width/4
#                     loadgamebutton.y=fullheight/2
#                     loadgamebutton.width=width//2
#                     loadgamebutton.height=height//8
#                     loadgamebutton.rect=pygame.Rect(loadgamebutton.x, loadgamebutton.y, loadgamebutton.width, loadgamebutton.height)
#                     loadgamebutton.image = pygame.transform.scale(loadgamebutton.image, (loadgamebutton.width,loadgamebutton.height))

                    newworldbutton.x=width*newworldbutton.posratio[0]
                    newworldbutton.y=height*newworldbutton.posratio[1]
                    newworldbutton.width=width*newworldbutton.sizeratio[0]
                    newworldbutton.height=height*newworldbutton.sizeratio[1]
                    newworldbutton.rect=pygame.Rect(newworldbutton.x, newworldbutton.y, newworldbutton.width, newworldbutton.height)
                    newworldbutton.image = pygame.transform.scale(newworldbutton.image, (int(newworldbutton.width),int(newworldbutton.height)))

                    joinworldbutton.x=width*joinworldbutton.posratio[0]
                    joinworldbutton.y=height*joinworldbutton.posratio[1]
                    joinworldbutton.width=width*joinworldbutton.sizeratio[0]
                    joinworldbutton.height=height*joinworldbutton.sizeratio[1]
                    joinworldbutton.rect=pygame.Rect(joinworldbutton.x, joinworldbutton.y, joinworldbutton.width, joinworldbutton.height)
                    joinworldbutton.image = pygame.transform.scale(joinworldbutton.image, (int(joinworldbutton.width),int(joinworldbutton.height)))
                    
                    buildworldbutton.x=width*buildworldbutton.posratio[0]
                    buildworldbutton.y=height*buildworldbutton.posratio[1]
                    buildworldbutton.width=width*buildworldbutton.sizeratio[0]
                    buildworldbutton.height=height*buildworldbutton.sizeratio[1]
                    buildworldbutton.rect=pygame.Rect(buildworldbutton.x, buildworldbutton.y, buildworldbutton.width, buildworldbutton.height)
                    buildworldbutton.image = pygame.transform.scale(buildworldbutton.image, (int(buildworldbutton.width),int(buildworldbutton.height)))
                    
                    settingsbutton.x=width*settingsbutton.posratio[0]
                    settingsbutton.y=height*settingsbutton.posratio[1]
                    settingsbutton.width=width*settingsbutton.sizeratio[0]
                    settingsbutton.height=height*settingsbutton.sizeratio[1]
                    settingsbutton.rect=pygame.Rect(settingsbutton.x, settingsbutton.y, settingsbutton.width, settingsbutton.height)
                    settingsbutton.image = pygame.transform.scale(settingsbutton.image, (int(settingsbutton.width),int(settingsbutton.height)))
                    
                    quitgamebutton.x=width*quitgamebutton.posratio[0]
                    quitgamebutton.y=height*quitgamebutton.posratio[1]
                    quitgamebutton.width=width*quitgamebutton.sizeratio[0]
                    quitgamebutton.height=height*quitgamebutton.sizeratio[1]
                    quitgamebutton.rect=pygame.Rect(quitgamebutton.x, quitgamebutton.y, quitgamebutton.width, quitgamebutton.height)
                    quitgamebutton.image = pygame.transform.scale(quitgamebutton.image, (int(quitgamebutton.width),int(quitgamebutton.height)))
                    
                    mainmenubutton.x=width*mainmenubutton.posratio[0]
                    mainmenubutton.y=height*mainmenubutton.posratio[1]
                    mainmenubutton.width=width*mainmenubutton.sizeratio[0]
                    mainmenubutton.height=height*mainmenubutton.sizeratio[1]
                    mainmenubutton.rect=pygame.Rect(mainmenubutton.x, mainmenubutton.y, mainmenubutton.width, mainmenubutton.height)
                    mainmenubutton.image = pygame.transform.scale(mainmenubutton.image, (int(mainmenubutton.width),int(mainmenubutton.height)))
                    
                    playofflinebutton.x=width*playofflinebutton.posratio[0]
                    playofflinebutton.y=height*playofflinebutton.posratio[1]
                    playofflinebutton.width=width*playofflinebutton.sizeratio[0]
                    playofflinebutton.height=height*playofflinebutton.sizeratio[1]
                    playofflinebutton.rect=pygame.Rect(playofflinebutton.x, playofflinebutton.y, playofflinebutton.width, playofflinebutton.height)
                    playofflinebutton.image = pygame.transform.scale(playofflinebutton.image, (int(playofflinebutton.width),int(playofflinebutton.height)))
                    
                    playonlinebutton.x=width*playonlinebutton.posratio[0]
                    playonlinebutton.y=height*playonlinebutton.posratio[1]
                    playonlinebutton.width=width*playonlinebutton.sizeratio[0]
                    playonlinebutton.height=height*playonlinebutton.sizeratio[1]
                    playonlinebutton.rect=pygame.Rect(playonlinebutton.x, playonlinebutton.y, playonlinebutton.width, playonlinebutton.height)
                    playonlinebutton.image = pygame.transform.scale(playonlinebutton.image, (int(playonlinebutton.width),int(playonlinebutton.height)))
                    
                    cansavebutton.x=width*cansavebutton.posratio[0]
                    cansavebutton.y=height*cansavebutton.posratio[1]
                    cansavebutton.width=width*cansavebutton.sizeratio[0]
                    cansavebutton.height=height*cansavebutton.sizeratio[1]
                    cansavebutton.rect=pygame.Rect(cansavebutton.x, cansavebutton.y, cansavebutton.width, cansavebutton.height)
                    cansavebutton.image = pygame.transform.scale(cansavebutton.image, (int(cansavebutton.width),int(cansavebutton.height)))
                    
                    nosavebutton.x=width*nosavebutton.posratio[0]
                    nosavebutton.y=height*nosavebutton.posratio[1]
                    nosavebutton.width=width*nosavebutton.sizeratio[0]
                    nosavebutton.height=height*nosavebutton.sizeratio[1]
                    nosavebutton.rect=pygame.Rect(nosavebutton.x, nosavebutton.y, nosavebutton.width, nosavebutton.height)
                    nosavebutton.image = pygame.transform.scale(nosavebutton.image, (int(nosavebutton.width),int(nosavebutton.height)))
                    
                    defaultworldbutton.x=width*defaultworldbutton.posratio[0]
                    defaultworldbutton.y=height*defaultworldbutton.posratio[1]
                    defaultworldbutton.width=width*defaultworldbutton.sizeratio[0]
                    defaultworldbutton.height=height*defaultworldbutton.sizeratio[1]
                    defaultworldbutton.rect=pygame.Rect(defaultworldbutton.x, defaultworldbutton.y, defaultworldbutton.width, defaultworldbutton.height)
                    defaultworldbutton.image = pygame.transform.scale(defaultworldbutton.image, (int(defaultworldbutton.width),int(defaultworldbutton.height)))
                    
                    customworldbutton.x=width*customworldbutton.posratio[0]
                    customworldbutton.y=height*customworldbutton.posratio[1]
                    customworldbutton.width=width*customworldbutton.sizeratio[0]
                    customworldbutton.height=height*customworldbutton.sizeratio[1]
                    customworldbutton.rect=pygame.Rect(customworldbutton.x, customworldbutton.y, customworldbutton.width, customworldbutton.height)
                    customworldbutton.image = pygame.transform.scale(customworldbutton.image, (int(customworldbutton.width),int(customworldbutton.height)))
                    
                    savedworldbutton.x=width*savedworldbutton.posratio[0]
                    savedworldbutton.y=height*savedworldbutton.posratio[1]
                    savedworldbutton.width=width*savedworldbutton.sizeratio[0]
                    savedworldbutton.height=height*savedworldbutton.sizeratio[1]
                    savedworldbutton.rect=pygame.Rect(savedworldbutton.x, savedworldbutton.y, savedworldbutton.width, savedworldbutton.height)
                    savedworldbutton.image = pygame.transform.scale(savedworldbutton.image, (int(savedworldbutton.width),int(savedworldbutton.height)))
                    
                    
                    button1.x=width/4
                    button1.y=fullheight/25
                    button1.width=width//6
                    button1.height=height//6
                    button1.rect=pygame.Rect(button1.x, button1.y, button1.width, button1.height)
                    button2.x=(width*3/4)-(width//6)
                    button2.y=height/25
                    button2.width=width//6
                    button2.height=height//6
                    button2.rect=pygame.Rect(button2.x, button2.y, button2.width, button2.height)
                    button3.x=(width/17)
                    button3.y=height/3.4
                    button3.width=width//6
                    button3.height=height//6
                    button3.rect=pygame.Rect(button3.x, button3.y, button3.width, button3.height)
                    button4.x=(width*13.5/17)
                    button4.y=height/3.4
                    button4.width=width//6
                    button4.height=height//6
                    button4.rect=pygame.Rect(button4.x, button4.y, button4.width, button4.height)
                    button5.x=(width/8)
                    button5.y=height*2.5/4
                    button5.width=width//6
                    button5.height=height//6
                    button5.rect=pygame.Rect(button5.x, button5.y, button5.width, button5.height)
                    button6.x=(width*5.8/8)
                    button6.y=height*2.5/4
                    button6.width=width//6
                    button6.height=height//6
                    button6.rect=pygame.Rect(button6.x, button6.y, button6.width, button6.height)
                    button7.x=(width/2)-width/12
                    button7.y=height*5.45/7
                    button7.width=width//6
                    button7.height=height//6
                    button7.rect=pygame.Rect(button7.x, button7.y, button7.width, button7.height)
                        
                    
                #if event.key==K_BACKSPACE:
                    # go back a page

################## DISPLAY ################################
        
        this_screen.fill((255, 10, 10))
        
        if menu== 'main':
            for bttn in buttnsA:
                this_screen.blit(bttn.image, (bttn.x,bttn.y))
        elif menu== 'new':
            for bttn in buttnsB:
                if bttn.name == 'playonlinebutton':
                    if online == True:
                        this_screen.blit(bttn.image, (bttn.x,bttn.y))
                elif bttn.name == 'playofflinebutton':
                    if online == False:
                        this_screen.blit(bttn.image, (bttn.x,bttn.y))
                elif bttn.name == 'cansavebutton':
                    if can_save == True:
                        this_screen.blit(bttn.image, (bttn.x,bttn.y))
                elif bttn.name == 'nosavebutton':
                    if can_save == False:
                        this_screen.blit(bttn.image, (bttn.x,bttn.y))
                else:
                    this_screen.blit(bttn.image, (bttn.x,bttn.y))
        elif menu == 'race':
            this_screen.blit(pic, (0,0))
        
        
        # This makes the buttons visible:
#        for bttn in buttns:
#            pygame.draw.rect(this_screen, (200,200,200), bttn.rect)

        pygame.display.flip()
        

def build_world():
    game_map=[]
    donebuilding=False
    while donebuilding==False:
        if game_map==[]:
            name=input('What do you want to name the first solar system?\n\n')
            spacetype=input('\nWhat background?\n  (1 - 3)\n')
            game_map.append(Space(name, spacetype))
        
        choice=input('\nEnter 1 to add a solar system\n'+
                     'Enter 2 to add a planet\n'+
                     'Enter 3 to edit\n'+
                     'Enter s to save\n'+
                     'Enter m to return to the main menu.\n')
        if choice=='1':
            name=input('\nWhat is the name of the new solar system?\n\n')
            spacetype=input('\nWhat background?\n  (1 - 3)\n')
            game_map.append(Space(name, spacetype))
        elif choice=='2':
            if len(game_map)==1:
                solarsystem=1
            else:
                count=1
                for space in game_map:
                    print("{} = {}".format(count, space.name))
                    count+=1
                solarsystem=input("Press the number of the solar system that will get this planet.\n")
            name=input("\nWhat is the name of the new planet?\n")
            kind=input('\nWhat is the planet type?\n'+
                        "-desert\n"+
                        "-grass\n"+
                        "-dying\n"+
                        "-dead\n"+
                        "-water\n"+
                        "-dry\n"+
                        "-scorched\n"+
                        "-burned\n"+
                        "-* ice *\n\n")
            game_map[int(solarsystem)-1].planets.append(Planet(name, game_map[int(solarsystem)-1], planet_type=kind))
        elif choice=='3':
            print("editing not ready yet.")
        elif choice=='s':
            name=input('What do you want to name this universe?\n\n')
            file=open('custom worlds/{}'.format(name),'wb')
            pickle.dump(game_map, file)
            file.close()
            print('\nWorld saved')
            print('-----------')
        elif choice == 'm':
            print("\nGame resumed")
            print('------------')
            return game_map
        else:
            print("error")
        
        
        print("\n\n--------------")
        for space in game_map:
            print(space.name)
            for planet in space.planets:
                print("      {}".format(planet.name))
        print("--------------\n\n")


def default_world():
    """This loads before the main game loop begins."""
    # Later this will be called by a function that loads the game title.
    # "Press start" when load (this function) is finished.
    game_map=[]
    space1=Space('space1',1)
    first_planet=Planet('planetA', space1, planet_type='desert')
    space1.planets.append(first_planet)
    game_map.append(space1)
    space2=Space('space2',2)
    space2.planets.append(Planet('planetB', space2,spacex=400, spacey=200,planet_type='grass'))
    space2.planets.append(Planet('planetC', space2,spacex=4400, spacey=2200,planet_type='dying'))
    space2.planets.append(Planet('planetD', space2,spacex=-2000, spacey=200,planet_type='dead'))
    game_map.append(space2)
    space3=Space('space3',1)
    space3.planets.append(Planet('planetE', space3,spacex=0, spacey=200,planet_type='water'))
    space3.planets.append(Planet('planetF', space3,spacex=4000, spacey=-200,planet_type='dry'))
    game_map.append(space3)
    space4=Space('space4',3)
    space4.planets.append(Planet('planetG', space4,spacex=30, spacey=0,planet_type='scorched'))
    space4.planets.append(Planet('planetH', space4,spacex=4000, spacey=200,planet_type='burned'))
    space4.planets.append(Planet('planetI', space4,spacex=-400, spacey=-2000,planet_type='dead'))
    game_map.append(space4)
    
    # create environment:
    # TODO: make environment and objectives an external text list
    # quests and environment get imported from these lists
    building1=Buildings('dump1', 200, 300)
    first_planet.environment=[('buildings',[building1]),
                                  ('spawnpoints',[]),
                                  ('jumpspot',[]),
                                  ('trees',[]),
                                  ('sandbags',[]),
                                  ('mine',[])]
    
    
    return (game_map, first_planet)


def new_game(gamesize, screen, gmap='default'):
    
    # Global variables and lists:
    # Object containing all variables:
    global gamevars # delete this line after this object is sent to the functions that need it

    
    # this loads the saved or default maps of space objects
    if gmap == 'default':
        gamevars.game_map, gamevars.current_location=default_world()
    elif gmap != 'online':
        #name=input("What is the name of the world?\n")
        try:
            file=open('custom worlds/{}'.format(gmap),'rb')
            gamevars.game_map=pickle.load(file)
            file.close()
            starthere='none'
            for space in gamevars.game_map:
                for guy in space.npc:
                    guy.set_image()
                for planet in space.planets:
                    if starthere=='none':
                        starthere=planet
                    planet.set_image()
                    for guy in planet.npc:
                        guy.set_image()
                    for things in planet.environment:
                        for thing in things[1]:
                            thing.set_image()
            if starthere=='none':
                gamevars.current_location=gamevars.game_map[0]
            else:
                gamevars.current_location=starthere
        except pygame.error:
            print("World not found.")
    
    #should the loading go here? 
    if gmap=='online':
        gamevars.current_location=Space('none', 1)
    else:
        load_planet(gamevars.current_location)  # it's in the loading game function right now
    
    
    # this creates the user, must be after current_location is created.
    gamevars.user=Main_Player(gamevars.playerkind, gamevars.server_parent)
    #user=MainCharacter( playerkind, server_parent, name="Player")
    gamevars.main_players.append(gamevars.user.mysprite)
    
    
    #uiunitx, uiunity = gamesize[0]//36, (gamesize[1]*4)//8.5
    
    # for testing, this gives the player 2 starting weapons
    #TODO: make into a quest:
    gamevars.botbar=UI_bar('player')
    
    gamevars.botbar.myhotkeys[0].contains=Icon_square('pistol')
    gamevars.botbar.myhotkeys[1].contains=Icon_square('club')
    

    
    # create quests/missions:
    # TODO: should this be a part of the map?
    # starting/first quests are stored in map
    # once a player gets a quest he gets a copy of the quest
    # the quest object can hold other quests, to start a chain
    # player saves this chain and his progress, but must get them from the map object.
    
    if gmap!='online':
        mission=Objective('start','tutorial')
        mission.requires=[]
        mission.add=['statue','statue','statue','statue','statue','statue']
        mission.actions=['kill npc','kill npc','kill npc','kill npc','kill npc','kill npc']
        mission.reactions=[('xp',10000)]
        mission.say='Try to kill these 6 statues.'
        gamevars.user.myquests.new_objective(mission)
    
    

    # TODO: make this work as a quest, conditions= if playerkind=='tyranid':
    gamevars.user.biomatter=400
    print("biomatter:"+str(gamevars.user.biomatter))
    
    return gamevars


def save_game(game):
#     if game.current_location.space_type=='none':
#         space=game.current_location.name
#         planet='none'
#     else:
#         space=game.current_location.parent.name
#         planet=game.current_location.name
#     #print(game.user.myarmy[0])
#     #print(game.game_map[0].planets[0].name)
#     #print(game.game_map[0].planets[0].environment[0][1][0])
#     saving=0
#     #saving=game.user.myarmy[0]
#     saving=[game]
#     #saving=[game.user.mysprite]
#     print(saving)
#     #saving=[game.current_location.environment[0][1][0]]
#             #game.user,
#             #space,
#             #planet]
    file=open('saved games/SavedGame','wb')
    pickle.dump(game, file)
    file.close()
    print('\nGame saved')
    print('----------')
    

def load_game(gamesize, screen):
    #TODO: get load game functions in here
    global gamevars
    try:
        file=open('saved games/SavedGame','rb')
        loaded=pickle.load(file)
        file.close()
        gamevars.game_map=loaded.game_map
        gamevars.current_location=loaded.current_location
        gamevars.current_location.set_image()
        
        
        for space in gamevars.game_map:
            for guy in space.npc:
                guy.set_image()
            for planet in space.planets:
                planet.set_image()
                for guy in planet.npc:
                    guy.set_image()
                for things in planet.environment:
                    for thing in things[1]:
                        thing.set_image()
        gamevars.playerkind = loaded.playerkind
        gamevars.user=loaded.user
        gamevars.user.mysprite.set_image()
        for guy in gamevars.user.myarmy:
            guy.set_image()
        gamevars.main_players.append(gamevars.user.mysprite)
        #for guy in game.current_location.npc:
        #    guy.set_image()
#         game.game_map=loaded[0]
#         print(game.game_map)
#         game.user=loaded[1]
#         for space in game.game_map:
#             if space.name == loaded[2]:
#                 if loaded[3]=='none':
#                     game.current_location=space
#                 else:
#                     for planet in space.planets:
#                         if planet.name == loaded[3]:
#                             game.current_location=planet
        if gamevars.current_location.space_type=='none':
            load_planet(gamevars.current_location)
        else:
            load_space(gamevars.current_location)
        gamevars.botbar=UI_bar('player')
        gamevars.botbar.hotkey1 = loaded.botbar.hotkey1
        gamevars.botbar.hotkey2 = loaded.botbar.hotkey2
        gamevars.botbar.hotkey3 = loaded.botbar.hotkey3
        gamevars.botbar.hotkey4 = loaded.botbar.hotkey4
        gamevars.botbar.hotkey5 = loaded.botbar.hotkey5
        gamevars.botbar.hotkey6 = loaded.botbar.hotkey6
        gamevars.botbar.hotkey7 = loaded.botbar.hotkey7
        gamevars.botbar.hotkey8 = loaded.botbar.hotkey8
        gamevars.botbar.hotkey9 = loaded.botbar.hotkey9
        gamevars.botbar.hotkey10 = loaded.botbar.hotkey10
        gamevars.botbar.hotkey11 = loaded.botbar.hotkey11
        gamevars.botbar.hotkey12 = loaded.botbar.hotkey12
        gamevars.botbar.myhotkeys = [gamevars.botbar.hotkey1,
                                     gamevars.botbar.hotkey2,
                                     gamevars.botbar.hotkey3,
                                     gamevars.botbar.hotkey4,
                                     gamevars.botbar.hotkey5,
                                     gamevars.botbar.hotkey6,
                                     gamevars.botbar.hotkey7,
                                     gamevars.botbar.hotkey8,
                                     gamevars.botbar.hotkey9,
                                     gamevars.botbar.hotkey10,
                                     gamevars.botbar.hotkey11,
                                     gamevars.botbar.hotkey12]
        
        #gamevars.botbar.myhotkeys = loaded.botbar.myhotkeys
        
        for square in gamevars.botbar.myhotkeys:
            square.resize()
        #return gamevars
    except TypeError:
        print('Save not found, shutting down')
        end_game()

def end_game():
    #global done, online
    global gamevars
    """This stops the game loop and quits pygame."""
    try:
        if gamevars.online==True:
            send_to_host('close_me')
            gamevars.socksend.close()
            gamevars.sockrec.close()
        gamevars.online=False
        gamevars.done = True
    except NameError:
        pass
    pygame.quit()
    os._exit(1)
    sys.exit("You quit the game, not me")


    
#---------------ONLINE FUNCTIONS AND THREADS:---------------


class checkinghostThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global gamevars
        #gamevars.online
        #socksend=gamevars.socksend 
        #sockrec=gamevars.sockrec
        #current_location
##        for guy in npc:
##            send_to_host(['spawnstatue',guy,guy.x-current_location.gamex,guy.y-current_location.gamey])
##        for dude in main_player:
##            for guy in dude.myarmy:
##                send_to_host(['spawnsoldier',guy,guy.x-current_location.gamex,guy.y-current_location.gamey])
##        for guy in main_player:
##            send_to_host(['spawnplayer',guy,guy.x-current_location.gamex,guy.y-current_location.gamey])
        #send_to_host('get_all_sprites')
        #sock.send('get_all_sprites'.encode('utf-8'))
        while gamevars.online==True:
            try:
                message=recv_one_message(gamevars.sockrec)
                #message=sockrec.recv(16000)
                #print(message)
                message=pickle.loads(message)
                translate(message)
            except ConnectionResetError:
                print("ERROR: lost connection")
                gamevars.online=False
                remove_online_sprites()
            except ConnectionAbortedError:
                gamevars.online=False
                remove_online_sprites()
            except EOFError:
                print("lost data")
                #print(message)
                try_again=checkinghostThread()
                try_again.start()
                break
            except OverflowError:
                print("Too much data")
            #except TypeError:
                

class checkingclientThread (threading.Thread):
    def __init__(self, clientsock, addr):
        threading.Thread.__init__(self)
        self.sock=clientsock
        self.addr=addr
        self.running=True
    def run(self):
        global gamevars
        online=gamevars.online
        #current_location=gamevars.current_location
        #, socksend
##        for guy in npc:
##            send_to_host(["just_one",self.addr,['spawnstatue',guy,guy.x-gamex,guy.y-current_location.gamey]])
##        for dude in main_player:
##            for guy in dude.myarmy:
##                send_to_host(["just_one",self.addr,['spawnsoldier',guy,guy.x-gamex,guy.y-current_location.gamey]])
##        for guy in main_player:
##            send_to_host(["just_one",self.addr,['spawnplayer',guy,guy.x-gamex,guy.y-current_location.gamey]])
##            print("hello")
        while self.running==True:
            if online==False:
                self.running=False
            try:
                message=recv_one_message(self.sock)
                message=pickle.loads(message)
#                 if message[0]=='close_him':
#                     for guy in current_location.online_players:
#                         if guy.serverparent==self.addr:
#                             current_location.online_players.remove(guy)
#                     for guy in current_location.online_troops:
#                         if guy.serverparent==self.addr:
#                             current_location.online_troops.remove(guy)
#                     clientlist.remove(self.sock)
#                     self.sock.close()
#                     self.running=False
                #else:
                translate(message)
            except ConnectionResetError:
                print("ERROR: lost connection")
                self.running=False
                remove_online_sprites()
            except ConnectionAbortedError:
                self.running=False
                remove_online_sprites()
            except EOFError:
                print("lost data")
                print(message)
            except OverflowError:
                print("Too much data")
            except TypeError:
                # This means the connection was closed and received a nonetype
                print("NoneType Error, the socket was closed.")
                remove_player_sprites(self.addr)
                gamevars.clientlist.remove(self.sock)
                self.sock.close()
                self.running=False
                
def remove_player_sprites(plyr):
    global gamevars
    for space in gamevars.game_map:
        for guy in space.online_players:
            if guy.serverparent==plyr:
                space.online_players.remove(guy)
        for guy in space.online_troops:
            if guy.serverparent==plyr:
                space.online_troops.remove(guy)
        for guy in space.online_npcs:
            if guy.serverparent==plyr:
                space.online_npcs.remove(guy)
        for planet in space.planets:
            for guy in planet.online_players:
                if guy.serverparent==plyr:
                    print(guy.name)
                    planet.online_players.remove(guy)
            for guy in planet.online_troops:
                if guy.serverparent==plyr:
                    planet.online_troops.remove(guy)
            for guy in planet.online_npcs:
                if guy.serverparent==plyr:
                    planet.online_npcs.remove(guy)
            
    print('deleted')
    # OLD CODE:
#     current_location=gamevars.current_location
#     for guy in current_location.online_players:
#         if guy.serverparent==plyr:
#             current_location.online_players.remove(guy)
#     for guy in current_location.online_troops:
#         if guy.serverparent==plyr:
#             current_location.online_troops.remove(guy)
#     if current_location.space_type=='none':  # this means planet
#         # This is to delete him on all spaces, 
#         # so an old sprite isn't waiting in space
#         for guy in current_location.parent.online_players:
#             if guy.serverparent==plyr:
#                 current_location.parent.online_players.remove(guy)
#         for guy in current_location.parent.online_troops:
#             if guy.serverparent==plyr:
#                 current_location.parent.online_troops.remove(guy)
#                 
#     else:  # this means space
#         for loc in current_location.planets:
#             for guy in loc.online_players:
#                 if guy.serverparent==plyr:
#                     current_location.online_players.remove(guy)
#             for guy in loc.online_troops:
#                 if guy.serverparent==plyr:
#                     current_location.online_troops.remove(guy)

def remove_online_sprites():
    global gamevars #current_location #online_npcs, online_players, online_troops
    try:
        gamevars.current_location.online_npcs.empty()
        gamevars.current_location.online_players.empty()
        gamevars.current_location.online_troops.empty()
    except AttributeError:
        print('Error, no player yet.')

def send_one_message(sck, data):
    length = len(data)
    sck.send(struct.pack('!I', length))
    send_again=recvall(sck, 4)
    while struct.unpack('!I', send_again)[0] != length:
        empty_socket(sck)
        sck.send(struct.pack('!I', 0))
        sck.send(struct.pack('!I', length))
        send_again=recvall(sck, 4)
    sck.send(struct.pack('!I', 1))
    sck.send(data)
    message=recvall(sck, length)
    while message!=data:
        empty_socket(sck)
        sck.send(struct.pack('!I', 0))
        sck.send(data)
        message=recvall(sck, length)
    sck.send(struct.pack('!I', 1))

def recv_one_message(sck):
    lengthbuf = recvall(sck, 4)
    if lengthbuf!=None:
        sck.send(lengthbuf)
    else:
        return
    got_it=recvall(sck, 4)
    while struct.unpack('!I', got_it)[0] !=1:
        empty_socket(sck)
        lengthbuf = recvall(sck, 4)
        sck.send(lengthbuf)
        got_it=sck.recv(4)
    length, = struct.unpack('!I', lengthbuf)
    message=recvall(sck, length)
    sck.send(message)
    got_it=recvall(sck, 4)
    while struct.unpack('!I', got_it)[0] !=1:
        # TODO: erase empty_socket?
        empty_socket(sck)
        message=recvall(sck, length)
        sck.send(message)
        got_it=sck.recv(4)
    return message

def recvall(sockrec, count):
    buf = b''
    while count:
        newbuf = sockrec.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def empty_socket(sock):
    """remove the data present on the socket"""
    # delete this function?
    #sock.recv(16000)
    pass

def send_to_host(what):
    #global online, host, port, socksend
    global gamevars
    if gamevars.online==True:
        try:
            #client(host, port, pickle.dumps(what))
            send_one_message(gamevars.socksend, pickle.dumps(what))
            #return
            #print('') #this is only to make it stop between sends, not one long send
        except ConnectionResetError:
            gamevars.online=False
            print("ERROR: Connection was lost. Please reconnect.")
            remove_online_sprites()

def sethost():
    #global host, port
    global gamevars
    gamevars.host = socket.gethostname() # Get local machine name
    gamevars.port = 12345                # Reserve a port for your service.
    ip=0
    while ip==0:
        try:
            file=open("multiplayer_info.txt", 'r')
            gamevars.host=file.read()
            ip=1
            print("Connecting to "+gamevars.host)
        except NameError:
            print('ERROR: "multiplayer_info.txt" file not found.')
            ip=input("Enter the IP address of the host,\n"
                  "or leave blank to use your own IP address. ")
            if ip!="":
                gamevars.host=ip
        except FileNotFoundError:
            print('ERROR: "multiplayer_info.txt" file not found.')
            ip=input("Enter the IP address of the host,\n"
                  "or leave blank to use your own IP address. ")
            if ip!="":
                gamevars.host=ip

def go_online():
    try:
        #TODO: get rid of the global list main_players?
        # There is only one main player, others are online players
        # (2nd player?)
        global gamevars
        #socksend=gamevars.socksend
        #sockrec=gamevars.sockrec
        #port=gamevars.port
        #host=gamevars.host
        #parent=gamevars.server_parent
        #current_location=gamevars.current_location
        #user=gamevars.user
        gamevars.online=True
        gamevars.socksend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gamevars.sockrec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sethost()
        gamevars.socksend.connect((gamevars.host, gamevars.port))
        print(recv_one_message(gamevars.socksend).decode('utf-8'))
        send_one_message(gamevars.socksend, "send".encode('utf-8'))
        gamevars.server_parent=recv_one_message(gamevars.socksend).decode('utf-8')
        gamevars.user.mysprite.serverparent=gamevars.server_parent
        if type(gamevars.current_location) != int:
            for troop in gamevars.user.myarmy:
                #print("working")
                troop.serverparent=gamevars.server_parent
            for guy in gamevars.current_location.npc:
                guy.serverparent=gamevars.server_parent
        gamevars.sockrec.connect((gamevars.host, gamevars.port))
        print(recv_one_message(gamevars.sockrec).decode('utf-8'))
        send_one_message(gamevars.sockrec,"recv".encode('utf-8'))
        if type(gamevars.current_location) == int:
            send_one_message(gamevars.sockrec,pickle.dumps((gamevars.server_parent, 'none')))
        else:
            send_one_message(gamevars.sockrec,pickle.dumps((gamevars.server_parent, gamevars.current_location)))
        hostthread=checkinghostThread()
        hostthread.start()
    except ConnectionRefusedError:
        print("ERROR: Connection Refused")
        gamevars.online=False
        remove_online_sprites()
    except ConnectionResetError:
        gamevars.online=False
        print("ERROR: Connection was reset. Please reconnect.")
        remove_online_sprites()    

def translate(message):
    global gamevars
    #current_location=gamevars.current_location 
    #host=gamevars.host
    #port=gamevars.port
    #serverparent=gamevars.server_parent
    clientlist=gamevars.clientlist
    if type(message)==str:
        print(message)
        #^^^^delete?
        
    if message[0]=="map":
        print('got map')
        print(message[1][0].name)
        gamevars.game_map=message[1]
        starthere='none'
        for space in gamevars.game_map:
            for guy in space.npc:
                guy.set_image()
            for planet in space.planets:
                if starthere=='none':
                    starthere=planet
                planet.set_image()
                for guy in planet.npc:
                    guy.set_image()
                for things in planet.environment:
                    for thing in things[1]:
                        thing.set_image()
        
        if starthere.name=='none':
            starthere=gamevars.game_map[0]
            #gamevars.current_location=gamevars.game_map[0]
        #else:
        #    gamevars.current_location=starthere
        if starthere.space_type=='none':
            
            load_planet(starthere)

        else:
            load_space(starthere)
            
        #gamevars.current_location=starthere
        
    if message[0]=="new_client":
        print("got new client")
        fromaddr=message[1]
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsock.connect((gamevars.host, gamevars.port))
        print(recv_one_message(clientsock).decode('utf-8'))
        send_one_message(clientsock, pickle.dumps([fromaddr, gamevars.server_parent]))
        clientlist.append(clientsock)
        listen_to_client=checkingclientThread(clientsock, fromaddr)
        listen_to_client.start()
                
    if message[0]=='delete_player':
        remove_player_sprites(message[1])
        # OLD CODE:
#         if gamevars.current_location.space_type=='none':  # this means planet
#             for guy in gamevars.current_location.online_players:
#                 if guy.serverparent==message[1]:
#                     gamevars.current_location.online_players.remove(guy)
#             for guy in gamevars.current_location.online_troops:
#                 if guy.serverparent==message[1]:
#                     gamevars.current_location.online_troops.remove(guy)
#                     
#             # This is to delete him on all spaces, 
#             # so an old sprite isn't waiting in space
# 
#             for guy in gamevars.current_location.parent.online_players:
#                 if guy.serverparent==message[1]:
#                     gamevars.current_location.parent.online_players.remove(guy)
#             for guy in gamevars.current_location.parent.online_troops:
#                 if guy.serverparent==message[1]:
#                     gamevars.current_location.parent.online_troops.remove(guy)
#                     
#         # TODO: location error might be in here:
#         else:  # this means space
#             for guy in gamevars.current_location.online_players:
#                 if guy.serverparent==message[1]:
#                     gamevars.current_location.online_players.remove(guy)
#             for guy in gamevars.current_location.online_troops:
#                 if guy.serverparent==message[1]:
#                     gamevars.current_location.online_troops.remove(guy)
#             for loc in gamevars.current_location.planets:
#                 for guy in loc.online_players:
#                     if guy.serverparent==message[1]:
#                         gamevars.current_location.online_players.remove(guy)
#                 for guy in loc.online_troops:
#                     if guy.serverparent==message[1]:
#                         gamevars.current_location.online_troops.remove(guy)
    
    if message[0]=="get_all_sprites":
        #TODO: all npcs and environment are stored by the host, others just get info
        reply_to=message[1]
        for space in gamevars.game_map:
            for guy in space.npc:
                send_to_host(["just_one",reply_to,['spawnstatue',guy,guy.x-space.gamex,guy.y-space.gamey, space.name]])
            for planet in space.planets:
                for guy in planet.npc:
                    send_to_host(["just_one",reply_to,['spawnstatue',guy,guy.x-planet.gamex,guy.y-planet.gamey, planet.name]])
        for guy in gamevars.user.myarmy:
            send_to_host(["just_one",reply_to,['spawnsoldier',guy,guy.x-gamevars.current_location.gamex,guy.y-gamevars.current_location.gamey, gamevars.current_location.name]])
        for guy in gamevars.main_players:
            send_to_host(["just_one",reply_to,['spawnplayer',guy,guy.x-gamevars.current_location.gamex,guy.y-gamevars.current_location.gamey, gamevars.current_location.name]])
            print(reply_to)
        print("sent everything")
        
    if message[0] == 'spawnsoldier':
        if message[1].character == "tyranid":
            if message[1].age=='adult':
                change_character(message[1], 'tyranid/adult')
            else:
                change_character(message[1], 'tyranid/kid')
        elif message[1].character=="human":
            if message[1].age=='adult':
                change_character(message[1], 'human/adult')
            else:
                change_character(message[1], 'human/troop')

        for space in gamevars.game_map:
            if space.name == message[4]:
                message[1].x=message[2]+space.gamex
                message[1].y=message[3]+space.gamey
                message[1].set_rect()
                space.online_troops.add(message[1])
                return
            else:
                for planet in space.planets:
                    if planet.name == message[4]:
                        message[1].x=message[2]+planet.gamex
                        message[1].y=message[3]+planet.gamey
                        message[1].set_rect()
                        planet.online_troops.add(message[1])
                        return
    elif message[0]=='spawnplayer':
        if message[1].character == "tyranid":
            change_character(message[1], 'tyranid/player')
        elif message[1].character=="human":
            change_character(message[1], 'human/player')
        for space in gamevars.game_map:
            if space.name == message[4]:
                message[1].x=message[2]+space.gamex
                message[1].y=message[3]+space.gamey
                message[1].set_rect()
                space.online_players.add(message[1])
                return
            else:
                for planet in space.planets:
                    if planet.name == message[4]:
                        message[1].x=message[2]+planet.gamex
                        message[1].y=message[3]+planet.gamey
                        message[1].set_rect()
                        planet.online_players.add(message[1])
                        return
    elif message[0]=='spawnstatue':
        message[1].set_image()
        for space in gamevars.game_map:
            if space.name == message[4]:
                message[1].x=message[2]+space.gamex
                message[1].y=message[3]+space.gamey
                message[1].set_rect()
                space.online_npcs.add(message[1])
                return
            else:
                for planet in space.planets:
                    if planet.name == message[4]:
                        message[1].x=message[2]+planet.gamex
                        message[1].y=message[3]+planet.gamey
                        message[1].set_rect()
                        planet.online_npcs.add(message[1])
                        return
    elif message[0]=='attack':
        for guy in gamevars.current_location.online_npcs:
            if guy.onlineID==message[1]:
                guy.take_damage(message[2])
        for guy in gamevars.current_location.npc:
            if guy.onlineID==message[1]:
                guy.health=0
                guy.alive=False
    elif message[0]=='killnpc':
        for guy in gamevars.current_location.online_npcs:
            if guy.onlineID==message[1]:
                guy.take_damage(10000)
        for guy in gamevars.current_location.npc:
            if guy.onlineID==message[1]:
                guy.take_damage(10000)
    elif message[0]=='deletenpc':
        for guy in gamevars.current_location.online_npcs:
            if guy.onlineID==message[1]:
                gamevars.current_location.online_npcs.remove(guy)
        for guy in gamevars.current_location.npc:
            if guy.onlineID==message[1]:
                gamevars.current_location.npc.remove(guy)
    elif message[0]=='movenpc':
        for thing in gamevars.current_location.online_npcs:
            if thing.onlineID==message[1]:
                thing.x=message[2]+gamevars.current_location.gamex
                thing.y=message[3]+gamevars.current_location.gamey
                thing.set_rect()
    elif message[0]=='moveright':
        if message[1]=='Player':
            for guy in gamevars.current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="right"
                    guy.facing="right"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
        else:
            for guy in gamevars.current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
    elif message[0]=='moveleft':
        if message[1]=='Player':
            for guy in gamevars.current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
        else:
            for guy in gamevars.current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
    elif message[0]=='movedown':
        if message[1]=='Player':
            for guy in gamevars.current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
        else:
            for guy in gamevars.current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
    elif message[0]=='moveup':
        if message[1]=='Player':
            for guy in gamevars.current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
        else:
            for guy in gamevars.current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    guy.x =message[3]+gamevars.current_location.gamex
                    guy.y=message[4]+gamevars.current_location.gamey
                    guy.set_rect()
                    

#------------------END OF ONLINE FUNCTIONS-----------------------------------------






#___________________________________________________________________________
#***************************************************************************
#------------------------------START GAME:----------------------------------
    
    
def main_game_loop():
    
    # Initialize the game engine
    pygame.init()

    
    # Set the screen size and caption
    gamesize=(1000,700)

    screen = pygame.display.set_mode(gamesize)
    pygame.display.set_caption("WarHammer 40k")
    #my_screen = pygame.FULLSCREEN
    
    # Used to manage how fast the my_screen updates
    clock = pygame.time.Clock()
    
    #TODO: change to this after gamevars gets passed to functions that need it
    #gamevars=new_game(gamesize, screen)
    global gamevars
    
    gamevars=Game_variables(gamesize, screen)
    
    
    # later this will call the main menu
    response, gamevars.fullscrn = ask_player(gamevars.my_screen, gamesize)
    
    
    #this sets the invisible boundaries to move the screen
    gamevars.set_boundaries()
    
    
    if response == 'loadgame':
        load_game(gamesize, screen)
        
    elif response == 'loadgameonline':
        load_game(gamesize, screen)
        os.startfile('whammerServer.py')
        #os.startfile('whammerServer.exe')
        go_online()
        send_one_message(gamevars.socksend,pickle.dumps(('map',gamevars.game_map)))
    #TODO: fix these response variables
    #add if response[0]==default:
    
    elif response[0]==True: #online is true
        #TODO: this will send the map to the server
        gamevars.playerkind=response[1]
        new_game(gamesize, screen)
        #TODO: should this be opened beforehand?
        # or, try to run it, if it doesn't work then try to connect
        os.startfile('whammerServer.py')
        #os.startfile('whammerServer.exe')
        go_online()
        send_one_message(gamevars.socksend,pickle.dumps(('map',gamevars.game_map)))
        
    elif response[0]==False: #online is false
        gamevars.playerkind=response[1]
        new_game(gamesize, screen)
        
    elif response[0]=='join':
        gamevars.playerkind=response[1]
        new_game(gamesize, screen, gmap='online')
        go_online()
        #send_to_host(["new_location", gamevars.current_location, gamevars.current_location])
        send_one_message(gamevars.socksend, pickle.dumps(['get_map','get_map']))
        print('\nWaiting...\n')
        #count=0
        while gamevars.current_location.name=='none':
            pass
#             count+=1
#             if count >=10000:
#                 send_one_message(gamevars.socksend, pickle.dumps(['get_map','get_map']))
#                 print('\nStill waiting...\n')
#                 count=0
        print('Done waiting.')
        
    elif response[0]=='custom':
        gamevars.playerkind=response[3]
        if response[2]==True:
            #TODO: this will send the map to the server
            new_game(gamesize, screen, gmap=response[1])
            #TODO: should this be opened beforehand?
            # or, try to run it, if it doesn't work then try to connect
            os.startfile('whammerServer.py')
            #os.startfile('whammerServer.exe')
            go_online()
            send_one_message(gamevars.socksend,pickle.dumps(('map',gamevars.game_map)))
        elif response[2]==False:
            new_game(gamesize, screen, gmap=response[1])
        
    else:
        print("error  ...")
    
    
    
    
    # DELETE:
    # this makes a text box:
    #txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='type here: ')
    
    #music:
    #t=open('Soundtrack/GreendaleIsWhereIBelong.wav')
    #print(t.getframerate())
    #pygame.mixer.init(44200)
    
    #pygame.mixer.music.load('Soundtrack/Greendale.wav')
    
    #pygame.mixer.music.load('Soundtrack/ChristmasRap.wav')
    #pygame.mixer.music.play(3)
    
    # not used yet, might be used for in game menu
    #words_box="none"
    #using_menu=False
    


    # ------------------- Main Program Loop --------------------
    
    # Loop until the user clicks the close button.
    done = False
    
    while not done:
    
    
        # --- EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        
        user_inputs()
        
        # TODO, use these functions:
        if gamevars.user.character=='tyranid':
            tyranid_inputs()
        elif gamevars.user.character=="human":
            human_inputs()
        elif gamevars.user.character=='tau':
            tau_inputs()
        elif gamevars.user.character=='eldar':
            eldar_inputs()
        elif gamevars.user.character=='dark_eldar':
            darkeldar_inputs()
        elif gamevars.user.character=='chaos':
            chaos_inputs()
     
    
        # --- EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
    
    
    
    
        # --- GAME LOGIC SHOULD GO BELOW THIS COMMENT
    
        gamevars.user.myquests.check_flaglist()
        
    
        # This checks if troops are doing damage as they run around
        # TODO: change this so it spams the attack button, which only
        # works when cooldown time has passed.
        swinging()
        
    
        # --- GAME LOGIC SHOULD GO ABOVE THIS COMMENT
    
    
    
    
        # --- DRAWING CODE SHOULD GO BELOW THIS COMMENT
    
        
        # First, clear the my_screen to grey. Don't put other drawing commands
        # above this, or they will be erased with this command.
    
    
        gamevars.my_screen.fill((175, 175, 175)) # GREY
        
        
        fill_background(gamevars.my_screen)
        
        if gamevars.current_location.space_type=='none':   #this means it is a planet
            planet_display(gamevars.my_screen)
        else:
            space_display(gamevars.my_screen)
            
        
        # This displays the user interface:
        player_view(gamevars.my_screen, gamevars.botbar)
        
        
        #pygame.display.flip() # this updates whole screen
        pygame.display.update() # this updates only parts of the screen
        
        
        # --- DRAWING CODE SHOULD GO ABOVE THIS COMMENT
    
    
    
    
    
    
        # --- Limit to (change to 60?) frames per second
    
    
        clock.tick(20)  # this is how fast the game runs. it comes with pygame
    
        gamevars.myTick=gamevars.myTick+1
        if gamevars.myTick>1000:
            gamevars.myTick=0
#______________________________
    



if __name__=="__main__":
    main_game_loop()