
# TODO:
#
# class walls/doors
#
# get equipment 
#
# different controls for types


# PyInstaller --onefile whammer.py


########## CODE: ##########
import os, pygame, sys, random, pickle, struct, threading, socket#, socketserver, eztext, math
from pygame.locals import *   # only import needed functions and variables?
from win32api import GetSystemMetrics  # for getting the screen resolution

class Game_variables():
    def __init__(self, playerkind, size):
        #replace global variables with self.var
        global online, online2
        online=False
        online2=True
        global background
    
        #background= pygame.image.load('sprites/Background/backgrounddetailed8.png')
        global gamew, gameh
        gamew, gameh = 0,0 # background.get_size()
    
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
        global user, main_players, parent  #replace this parent with server_parent
        
        user=0
        main_players=[]
        #online_players=pygame.sprite.Group()
        #online_ships=[]   # turn this into a pygame group?
        
        global clientlist
        clientlist=[]  # delete?
        
        parent=""
        
        global walls, screensquares, left_rect, right_rect, toprect, bottomrect, spawningoffscreen
    
        walls = [] # List to hold the walls
        
        screensquares=[]
        left_rect = pygame.Rect(0, 0, 30, size[1])
        screensquares.append(left_rect)
        right_rect = pygame.Rect(size[0]-30, 0, 30, size[1])
        screensquares.append(right_rect)
        toprect = pygame.Rect(0, 0, size[0], 30)
        screensquares.append(toprect)
        bottomrect = pygame.Rect(0, size[1]-30, size[0], 30)
        screensquares.append(bottomrect)
        
        spawningoffscreen=False
        
        global myTick, keyTime
        myTick=0
        keyTime=0
        
        global ppushed
        ppushed=0
        
        global socksend, sockrec, host, port


class Planet():
    def __init__(self, name, parent, spacex=0, spacey=0, 
        size=(12000, 12000), planet_type='none'):
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
        self.background='none'
        self.npc=pygame.sprite.Group()
        self.other_players=[]
        self.online_players=pygame.sprite.Group()
        self.online_npcs=pygame.sprite.Group()
        self.online_troops=pygame.sprite.Group()
        self.online_ships=[]
        self.planetpic=setplanetpic(planet_type) # this function will pick a random planet that matches background
        self.rect = pygame.Rect(self.planetpic.get_rect())
        self.big_pic=pygame.image.load('sprites/space/planets/giant.png')


class Wearing_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/wearing_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        
class Skills_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/skills_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        
class Troop_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/troops_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        button1=Menu_Button('button1', 'buy_troop', self.width/4, self.y)
        button1.contains=BuyTroopObj(0,0,0,0) # TODO: button contents don't need rect?
        square1=UI_square("buy troop obj", self.x, self.y)
        square1.contains=BuyTroopObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square1.contains.image=pygame.image.load('sprites/ui/troop.png')
        #print(square1.rect.size)
        square1.contains.image=pygame.transform.scale(square1.contains.image, square1.rect.size)
        self.mybuttons=[button1]
        self.mysquares=[square1]
        
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        
class Groups_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/groups_menu.png')
        self.x=0
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        button1=Menu_Button('button1', 'square_formation', self.x+self.width/4, self.y)
        button1.contains=SquareFormationObj(0,0,0,0) # TODO: button contents don't need rect?
        button2=Menu_Button('button2', 'line_formation', self.x+self.width/4, self.y+self.height/6)
        button2.contains=LineFormationObj(0,0,0,0)
        square1=UI_square("square formation obj", self.x, self.y)
        square1.contains=SquareFormationObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square1.contains.image=pygame.image.load('sprites/ui/groups.png')
        square2=UI_square("line formation obj", self.x, self.y+self.height/6)
        square2.contains=LineFormationObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square2.contains.image=pygame.image.load('sprites/ui/groups.png')
        square1.contains.image=pygame.transform.scale(square1.contains.image, square1.rect.size)
        square2.contains.image=pygame.transform.scale(square2.contains.image, square2.rect.size)
        self.mybuttons=[button1, button2]
        self.mysquares=[square1, square2]
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()
        


class Inventory_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/inventory_menu.png')
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
#         for square in range(12):
#             self.myhotkeys.append(UI_square('inventory_square',
#                                             (self.width//55)+(square)*(self.width//27.2), 
#                                             self.y+self.height//3))
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()


class Weapon_skills_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/weapon_skills_menu.png')
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()

class Small_structures_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/small_structures_menu.png')
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        self.mybuttons=[]
        self.mysquares=[]
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()

class Ship_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/ship_menu.png')
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.posratio=(self.x/width,self.y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
        button1=Menu_Button('button1', 'buy_ship', self.x+self.width/4, self.y)
        button1.contains=BuyShipObj(0,0,0,0) # TODO: button contents don't need rect?
        square1=UI_square("buy ship obj", self.x, self.y)
        square1.contains=BuyShipObj(square1.rect.x,square1.rect.y,square1.rect.size[0],square1.rect.size[1])
        square1.contains.image=pygame.image.load('sprites/ui/ship.png')
        #print(square1.rect.size)
        square1.contains.image=pygame.transform.scale(square1.contains.image, square1.rect.size)
        self.mybuttons=[button1]
        self.mysquares=[square1]
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        for button in self.mybuttons:
            button.resize()
        for square in self.mysquares:
            square.resize()

class ActionObject():
    def __init__(self, x,y,width,height):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            Twidth, Theight=gamesize
        elif fullscrn==1:
            Twidth=fullwidth
            Theight=fullheight
        self.image='none'
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.posratio=(self.x/Twidth,self.y/Theight)
        self.sizeratio=(self.width/Twidth,self.height/Theight)
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        
class BuyTroopObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global user
        if user.biomatter>=100:
            user.biomatter=user.biomatter-100
            user.myarmy.append(Character(playerkind,parent,name="minion"))
            print("Biomatter: "+str(user.biomatter))
        else:
            print("Not enough biomatter.")
            
class BuyShipObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global user
        spawn_ship(user)
    

class SquareFormationObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global user
        troop_formations_square(user.mysprite, user.myarmy)
    
class LineFormationObj(ActionObject):
    def __init__(self, x,y,width,height):
        ActionObject.__init__(self, x,y,width,height)
    def myclick(self):
        global user
        troop_formations_line(user.mysprite, user.myarmy)

#TODO: move all if statements (functions) in "my click",
# instead the function should be in whatever it "self.opens"
# the thing in self.opens should be an object, can be dragged, remembers click function 
class Menu_Button():
    def __init__(self, name, kind, x, y, opens='none'):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
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
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        if self.name=='wearing_menu':
            self.image = pygame.image.load('sprites/ui/armor.png')
        elif self.name=='skills_menu':
            self.image = pygame.image.load('sprites/ui/skills.png')
        elif self.name=='troops_menu':
            self.image = pygame.image.load('sprites/ui/troop.png')
        elif self.name=='groups_menu':
            self.image = pygame.image.load('sprites/ui/groups.png')
        elif self.name=='closeright' or self.name=='closeleft':
            self.image = pygame.image.load('sprites/ui/close.png')
        elif self.name=='inventory_menu':
            self.image = pygame.image.load('sprites/ui/backpack.png')
        elif self.name=='weapon_skills_menu':
            self.image = pygame.image.load('sprites/ui/weapon_skills.png')
        elif self.name=='buildings_menu':
            self.image = pygame.image.load('sprites/ui/buildings.png')
        elif self.name=='ship_menu':
            self.image = pygame.image.load('sprites/ui/ship.png')
        else:
            self.image='none'
        if self.image!='none':
            self.image=pygame.transform.scale(self.image, (self.width, self.height))
        
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.x=width*self.posratio[0]
        self.y=height*self.posratio[1]
        self.width=int(self.sizeratio[0]*width)
        self.height=int(self.sizeratio[1]*height)
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        if self.image!='none':
            self.image=pygame.transform.scale(self.image, (self.width, self.height))
    def myclick(self):
        global botbar
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
                    botbar.wearing.visible=False
                if self.name!='skills_menu' and self.kind=='leftmenu':
                    botbar.myskills.visible=False
                if self.name!='troops_menu' and self.kind=='leftmenu':
                    botbar.mytroops.visible=False
                if self.name!='groups_menu' and self.kind=='leftmenu':
                    botbar.mygroups.visible=False
                if self.name!='inventory_menu' and self.kind=='rightmenu':
                    botbar.inventory.visible=False
                if self.name!='weapon_skills_menu' and self.kind=='rightmenu':
                    botbar.weapon_skills.visible=False
                if self.name!='buildings_menu' and self.kind=='rightmenu':
                    botbar.buildings.visible=False
                if self.name!='ship_menu' and self.kind=='rightmenu':
                    botbar.ship.visible=False
            else:
                self.opens.visible=False
        elif self.kind=='close':
            if self.name=='closeleft':
                botbar.wearing.visible=False
                botbar.myskills.visible=False
                botbar.mytroops.visible=False
                botbar.mygroups.visible=False
            elif self.name=='closeright':
                botbar.inventory.visible=False
                botbar.weapon_skills.visible=False
                botbar.buildings.visible=False
                botbar.ship.visible=False

        # TODO: everything uses this myclick, instead of the button knowing functions:
        else:
            self.contains.myclick()
        

class UI_bar():
    def __init__(self, view_mode):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.visible=True
        self.x=0
        self.y=0
        self.myhotkeys=[]
        self.myleftbuttons=[]
        self.myrightbuttons=[]
        if view_mode=='player':
            self.image = pygame.image.load('sprites/ui/botbar.png')
            self.width=width
            self.height=height//9
            self.x=0
            self.y=height*(4/4.5)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
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
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
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
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//36
        self.height=height//36
        self.posratio=(x/width,y/height)
        self.sizeratio=(self.width/width,self.height/height)
        self.visible=True
        self.x=x
        self.y=y
        self.moving=False
        self.image='none'
        self.contains='empty'
        self.kind=kind
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
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
        global dragging
        dragging=Moving_square(self.rect, self.contains, self)

class Icon_square():
    def __init__(self, kind):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//36
        self.height=height//36
        self.visible=True
        self.quantity=1
        if kind=='pistol':
            self.image= pygame.image.load('sprites/ui/pistol.png')
            self.abilities=['hip shot','scope shot','pistol whip']
            self.image=pygame.transform.scale(self.image, (self.width, self.height))
        elif kind=='club':
            self.image= pygame.image.load('sprites/ui/club.png')
            self.image=pygame.transform.scale(self.image, (self.width, self.height))
            self.abilities=['swing','throw','block']
        else:
            self.image='none'
            self.abilities=[]
        self.kind=kind
        #self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//36
        self.height=height//36
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
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
    global dragging
    if bttn.contains=='empty':
        bttn.contains=dragging.holding
        if dragging.parent.kind=='hot_key':
            dragging.parent.contains='empty'
    elif bttn!=dragging.parent:
        bttn.contains=dragging.holding
        if dragging.parent.kind=='hot_key':
            dragging.parent.contains=bttn.contains
    dragging==False
    
    
class Space(Planet):
    def __init__(self, name, space_type):
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

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, faction):
        pygame.sprite.Sprite.__init__(self)
        self.faction=faction
        self.x=100
        self.y=100
        self.image = pygame.image.load('sprites/space/'+self.faction+'.png')
        self.contents=[]
        self.speed=0.0

            
class Main_Player():
    def __init__(self, kind, serverparent):
        self.myarmy=pygame.sprite.Group()
        self.myships=[]
        self.myarmy=[]
        self.biomatter=0
        if kind=='tyranid':
            self.mysprite=Tyranid(serverparent, "Player")
        elif kind=='human':
            self.mysprite=Human(serverparent, "Player")
        self.character=kind
        self.in_ship=False

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
        global current_location
        if self.name=="Player":
            send_to_host(["spawnplayer", self, self.x-current_location.gamex, self.y-current_location.gamey])
        else:
            send_to_host(["spawnsoldier", self, self.x-current_location.gamex, self.y-current_location.gamey])


#     def re_initiate(self):
#         pygame.sprite.Sprite.__init__(self)
        
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
        self.health=self.health-(damage*self.armor())
        print(self.name, self.health)
        if self.health <=0:
            self.alive=False
            print("{} has died!".format(self.name))
            global user
            user.myarmy.remove(self)
            #^^^^^replace with dead pic
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
        global current_location
        send_to_host(["spawnstatue", self, self.x-current_location.gamex,self.y-current_location.gamey])

    def set_image(self):
        self.image = pygame.image.load(self.load)
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
                self.image=pygame.image.load('sprites/statue/dead.png')
                print("The {} statue has been destroyed.".format(self.name))
                #for guy in npc.sprites():
                #    if guy==self:
                #        npc.remove(guy)
        return self.alive

    def heal(self,hlth):
        """This adds a given amount of health to this statue."""
        self.health=self.health+hlth


class swarm_attackThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass
        #put the swarm-attack button code in here

class swarm_eatThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass
        #put the swarm-eat button code in here

class collidingThread (threading.Thread):
    def __init__(self, guy):
        threading.Thread.__init__(self)
        self.guy=guy
    def run(self):
        pass
        #put swinging function in here 

class updatescreenThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass
        #put all screen.blit for loops in here

class warpmenuThread (threading.Thread):
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
                for spaceplace in game_map:
                    print(str(tmpcount)+spaceplace.name)
                    tmpcount+=1
                tempchoice=input("\nEnter the number of the destination.")
                load_space(game_map[tempchoice])
            elif tempchoice==2:
                print("\n\nPlanets in the area:")
                tmpcount=1
                for planetplace in game_map:
                    print(str(tmpcount)+planetplace.name)
                    tmpcount+=1
                tempchoice=input("\nEnter the number of the destination.")
                load_space(current_location.planets[tempchoice])
            else:
                print("Warp cancelled.")

def troop_formations_line(leader, guys):
    #guys=leader.myarmy
    trooplength=len(guys)
    global user
    change_character(user.mysprite, "human/charles")
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
                change_character(guy, "human/archers")
                done_troops+=1
            troopcount=0
            for guy in guys[unitlength: unitlength*2]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(120,(-350+troopcount*troopspace))
                change_character(guy, "human/hwan")
                #pygame.transform.scale(guy.image, (30, 50))
                done_troops+=1
            troopcount=0
            for guy in guys[2*unitlength: unitlength*3]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(150,(-150+troopcount*troopspace))
                change_character(guy, "human/hwan")
                done_troops+=1
            troopcount=0
            for guy in guys[3*unitlength: unitlength*4]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(120,(50+troopcount*troopspace))
                change_character(guy, "human/hwan")
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


def fill_background(my_screen):
    global gamesize, current_location
    ## This is for the background:
    if current_location.gamex>0:
        if current_location.gamey<=0:
            tempx=current_location.gamex
            while tempx<gamesize[0]:
                tempx+=gamew
            for y in range(current_location.gamey,gamesize[1],gameh):
                for x in range(tempx,-gamew,-gamew):
                    my_screen.blit(background,(x,y))
        elif current_location.gamey>0:
            tempx=current_location.gamex
            tempy=current_location.gamey
            while tempx<gamesize[0]:
                tempx+=gamew
            while tempy<gamesize[1]:
                tempy+=gameh
            for y in range(tempy,-gameh,-gameh):
                for x in range(tempx,-gamew,-gamew):
                    my_screen.blit(background,(x,y))
                    
    elif current_location.gamex<=0:
        if current_location.gamey<=0:
            for y in range(current_location.gamey,gamesize[1],gameh):
                for x in range(current_location.gamex,gamesize[0],gamew):
                    my_screen.blit(background,(x,y))
        elif current_location.gamey>0:
            tempy=current_location.gamey
            while tempy<gamesize[1]:
                tempy+=gameh
            for y in range(tempy,-gameh,-gameh):
                for x in range(current_location.gamex,gamesize[0],gamew):
                    my_screen.blit(background,(x,y))
                    
                    

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
        global user, current_location, ppushed
        global playerkind, online
        global spawningoffscreen
        global botbar, dragging
        
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
                if dragging!=False:
                    pos= pygame.mouse.get_pos()
                    for bttn in botbar.myhotkeys:
                        if bttn.rect.collidepoint(pos)==True:
                            unclicked(bttn)
                    dragging=False
    
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
                    keyTime=myTick

                    
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
                    selected_troops=[]
                    for guy in user.myarmy:
                        if guy.age=="adult" and guy.selected==True:
                            selected_troops.append(guy)
                    if selected_troops!=[]:
                        user.mysprite.controlling=False
                        user.mysprite.selected=False
                        if user.mysprite.character=='tyranid':
                            change_character(user.mysprite,"tyranid/adult")
                        elif user.mysprite.character=='human':
                            change_character(user.mysprite,"human/adult")
                        user.mysprite.myarmy.add(user.mysprite)
                        main_players.remove(user.mysprite)
                        temp_num=random.randint(0,len(selected_troops)-1)
                        newmainguy=selected_troops[temp_num]
                        #newmainguy.myarmy=user.myarmy
                        #user.myarmy=[]
                        user.mysprite=newmainguy
                        
                        main_players.append(user.mysprite)

                        user.myarmy.remove(user.mysprite)

                        user.mysprite.controlling=True
                        user.mysprite.selected=False
                        if user.character=='tyranid':
                            change_character(user.mysprite,"tyranid/player")
                        elif user.character=='human':
                            change_character(user.mysprite,"human/player")
                        jump_here()

                if event.key==K_p:
                    print("You have "+str(len(user.myarmy))+" troops.")

                if event.key==K_o:
                    print("There are "+str(len(current_location.npc.sprites()))+" enemies.")
                    
                if event.key==K_i:
                    print("Your screen location:\n"+
                          "X = "+str(-current_location.gamex)+
                          "\nY = "+str(-current_location.gamey))

                if event.key==K_u:
                    if spawningoffscreen==False:
                        spawningoffscreen=True
                        print("spawning on")
                    else:
                        spawningoffscreen=False
                        print("spawning off")
                        
                     
                     
                
                if event.key==K_BACKQUOTE:
                    user.biomatter+=1000000
                    print("YouRich BEEEITCH!!!!")
                

                if event.key==K_BACKSPACE:
                    if online==False:
                        #online2=True
                        go_online()

                if event.key==K_DELETE:
                    if online==True:
                        try:
                            #send_to_host('close_me')
                            #sock.send('close'.encode('utf-8'))
                            socksend.close()
                            sockrec.close()
                            online=False
                            remove_online_sprites()
                        except ConnectionResetError:
                            online=False
                            print("ERROR: Connection was lost. Please reconnect.")
                            remove_online_sprites()

                if event.key==K_INSERT:
                    if online==True:
                        try:
                            send_to_host('helllooooo'.encode('utf-8'))
                            #sock.send('hellooooo'.encode('utf-8'))
                        except ConnectionResetError:
                            online=False
                            print("ERROR: Connection was lost. Please reconnect.")
                            remove_online_sprites()

                if event.key==K_EQUALS:
                    if online==True:
                        try:
                            send_to_host('testing')
                            #sock.send('testing'.encode('utf-8'))
                        except ConnectionResetError:
                            online=False
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
                        #warp=warpmenuThread(current_location)
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
    global current_location
    who.mytick+=1
    if who==user.mysprite:
        if toprect.colliderect(user.mysprite.rect) and user.mysprite.direction=="up":
            antimove('up')
        if bottomrect.colliderect(user.mysprite.rect) and user.mysprite.direction=="down":
            antimove('down')
        if left_rect.colliderect(user.mysprite.rect) and user.mysprite.direction=="left":
            antimove('left')
        if right_rect.colliderect(user.mysprite.rect) and user.mysprite.direction=="right":
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
    global fullscrn, my_screen, fullwidth, fullheight, botbar
    #print(my_screen.get_surface())
    if fullscrn == 0:
        fullscrn=1
        my_screen = pygame.display.set_mode((fullwidth,fullheight),pygame.FULLSCREEN)
        
        # TODO: move this to botbar.resize
        botbar.y=fullheight*(4/4.5)
        botbar.resize_image(fullwidth, fullheight)
    elif fullscrn == 1:
        global gamesize
        fullscrn=0
        my_screen = pygame.display.set_mode(gamesize)
        # TODO: move this to botbat.resize
        botbar.y=gamesize[1]*(4/4.5)
        botbar.resize_image(gamesize[0], gamesize[1])
        

def space_display(my_screen):
        global current_location, main_players
        
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

        for ship in user.myships:
            my_screen.blit(ship.image, (ship.x, ship.y))
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
    
        #for players in main_players:
        move_me(user.mysprite)
        my_screen.blit(user.mysprite.image, (user.mysprite.x, user.mysprite.y))


def planet_display(my_screen):
        global current_location, main_players 
        if current_location.above_planet==True: #this is if you are in planet assault mode
            my_screen.blit(current_location.big_pic, (current_location.gamex, current_location.gamey))
            
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

        for ship in user.myships:
            my_screen.blit(ship.image, (ship.x, ship.y))
            
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
    
        for it in current_location.npc.sprites():
            try:
                my_screen.blit(it.image, (it.x, it.y))
            except pygame.error:
                print(it)
            #pygame.draw.rect(my_screen,WHITE,it.rect)
    
        move_me(user.mysprite)
        my_screen.blit(user.mysprite.image, (user.mysprite.x, user.mysprite.y))
        
        #pygame.draw.rect(my_screen,WHITE,user.rect)
        #pygame.draw.rect(my_screen,WHITE,toprect)
        #pygame.draw.rect(my_screen,WHITE,bottomrect)
        #pygame.draw.rect(my_screen,WHITE,left_rect)
        #pygame.draw.rect(my_screen,WHITE,right_rect)
    
    
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
    global dragging
    
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

            
            

        if dragging!=False:
            posx,posy=pygame.mouse.get_pos()
            posx-=dragging.holding.width/2
            posy-=dragging.holding.height/2
            my_screen.blit(dragging.holding.image, (posx,posy))
    

def warpmenu(current):
    if current.space_type!="none":
        try:
            tempchoice=int(input("Press 1 to warp to other solar systems.\n"
                           "Press 2 to land on a planet.\n\n"))
            if tempchoice==1:
                print("\n\nKnown solar systems:")
                tmpcount=1
                for spaceplace in game_map:
                    if spaceplace==current:
                        print(str(tmpcount)+":  "+spaceplace.name+"   <--current location")
                    else:
                        print(str(tmpcount)+":  "+spaceplace.name)
                    tmpcount+=1
                tempchoice=int(input("\nEnter the number of the destination."))
                load_space(game_map[tempchoice-1])
                return game_map[tempchoice-1]
            elif tempchoice==2:
                print("\n\nPlanets in the area:    (coordinates)")
                tmpcount=1
                for planetplace in current.planets:
                    print(str(tmpcount)+":  "+planetplace.name +"       ("
                          +str(planetplace.spacex-current_location.gamex)
                          +", "+str(planetplace.spacey-current_location.gamey)+")")
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


def ask_player(this_screen, gsize):
    """Temporary function, will be replaced by main menu function"""
    fullscrn = 0
    fullwidth = GetSystemMetrics(0)
    fullheight = GetSystemMetrics(1)
    width,height=this_screen.get_size()
    
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
    buttns=[button1, button2, button3, button4, button5, button6, button7]
    
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
                    
                    for bttn in buttns:
                        if bttn.rect.collidepoint(pos)==True:
                            do_it=bttn.myclick()
                            if do_it != None:
                                done=True
                                return (bttn.myclick(), fullscrn)
                            
                        
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
                        this_screen = pygame.display.set_mode(gsize,pygame.FULLSCREEN)
                        pic = pygame.transform.scale(pic, gsize)
                    width, height=this_screen.get_size()
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
        this_screen.blit(pic, (0,0))
        
        # This makes the buttons visible:
#        for bttn in buttns:
#            pygame.draw.rect(this_screen, (200,200,200), bttn.rect)

        pygame.display.flip()
        


def loading_game():
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
    return (game_map, first_planet)
    
    
def load_planet_space(level):
    global background, gamew, gameh, current_location
    send_to_host(["new_location", level, current_location])
    background= pygame.image.load('sprites/space/background'+str(level.parent.space_type)+'.png')
    level.background=background
    gamew, gameh = background.get_size()
    #print(level.big_pic.get_size())
    level.gamex=-1032
    level.gamey=-1032
    level.above_planet=True
        
        
def load_space(level):
    """Takes a "Space" object and loads it."""
    global background, game_map, gamew, gameh, current_location
    old=current_location
    current_location=level
    send_to_host(["new_location", current_location, old])
    background= pygame.image.load('sprites/space/background'+str(level.space_type)+'.png')
    gamew, gameh = background.get_size()
    
    

def load_planet(level):
    global background, gamew, gameh, current_location
    old=current_location
    current_location=level
    send_to_host(["new_location", current_location, old])
    level.above_planet=False
    if level.planet_type=='grass':
        background= pygame.image.load('sprites/Background/backgrounddetailed1.png')
        level.background=background
        gamew, gameh = background.get_size()
    elif level.planet_type=='dying':
        background= pygame.image.load('sprites/Background/backgrounddetailed2.png')
        level.background=background
        gamew, gameh = background.get_size()
    elif level.planet_type=='dry':
        background= pygame.image.load('sprites/Background/backgrounddetailed3.png')
        level.background=background
        gamew, gameh = background.get_size()
    elif level.planet_type=='water':
        background= pygame.image.load('sprites/Background/backgrounddetailed4.png')
        level.background=background
        gamew, gameh = background.get_size()
    if level.planet_type=='dead':
        background= pygame.image.load('sprites/Background/backgrounddetailed5.png')
        level.background=background
        gamew, gameh = background.get_size()
    if level.planet_type=='scorched':
        background= pygame.image.load('sprites/Background/backgrounddetailed6.png')
        level.background=background
        gamew, gameh = background.get_size()
    if level.planet_type=='burned':
        background= pygame.image.load('sprites/Background/backgrounddetailed7.png')
        level.background=background
        gamew, gameh = background.get_size()
    if level.planet_type=='desert':
        background= pygame.image.load('sprites/Background/backgrounddetailed8.png')
        level.background=background
        gamew, gameh = background.get_size()

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
    global current_location, user
    if user.mysprite.x<100:
        difference=100-user.mysprite.x
        user.mysprite.x=100
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
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacex+= difference
    elif user.mysprite.x>600:
        difference=user.mysprite.x-600
        user.mysprite.x=600
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
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacex-= difference
    if user.mysprite.y<50:
        difference=50-user.mysprite.y
        user.mysprite.y=50
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
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacey+= difference
    elif user.mysprite.y>450:
        difference=user.mysprite.y-450
        user.mysprite.y=450
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
        if current_location.space_type!='none':
            for it in current_location.planets:
                it.spacey-= difference
        

def spawnoffscreen(direction):
    global spawningoffscreen, current_location, gamesize
    if spawningoffscreen==True:
        if direction=="up":
            if (random.randint(1,25))==1:
                newguy=Statue("Statue")
                newguy.y=-50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                current_location.npc.add(newguy)
        elif direction=="down":
            if (random.randint(1,40))==1:
                newguy=Statue("Statue")
                newguy.y=gamesize[1]+50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                current_location.npc.add(newguy)
        if direction=="left":
            if (random.randint(1,1))==1:
                newguy=Statue("Statue")
                newguy.x=-50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                current_location.npc.add(newguy)
        elif direction=="right":
            if (random.randint(1,50))==1:
                newguy=Statue("Statue")
                newguy.x=gamesize[0]+50
                newguy.rect=pygame.Rect(newguy.image.get_rect())
                newguy.rect.move_ip(newguy.x,newguy.y)
                current_location.npc.add(newguy)
        try:
            send_to_host(["movenpc", newguy.onlineID, newguy.x-current_location.gamex,newguy.y-current_location.gamey])
        except UnboundLocalError:
            pass

def antimove(direction):
    global current_location
    spawnoffscreen(direction)
    if direction=="up":
        current_location.gamey+=5
        user.mysprite.y += 5
        user.mysprite.rect=user.mysprite.rect.move(0,5)
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
    top=user.mysprite.rect.top
    bottom=user.mysprite.rect.bottom
    left=user.mysprite.rect.left
    right=user.mysprite.rect.right
    if (left<position[0]
        and position[0]<right
        and top<position[1]
        and position[1]<bottom):
        for guy in user.myarmy:
            guy.selected=False
        return True
    go_here=False
    for thing in current_location.npc:
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
        for thing in user.myarmy:
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
    for guy in user.myarmy:
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
    global current_location, user
    #for playyer in main_players:
    for guy in user.myarmy:
        if guy.attacking==True:
            for thing in current_location.npc:
                if thing.alive==True:
                    if guy.rect.colliderect(thing.rect):
                        testing_reasons=thing.take_damage(25)
                        #if testing_reasons==False:
                        #   guy.attacking=False
            for thing in current_location.online_npcs:
                if thing.alive==True:
                    if guy.rect.colliderect(thing.rect):
                        testing_reasons=thing.take_damage(25)
                        #if testing_reasons==False:
                        #   guy.attacking=False
        if guy.eating==True:
            eat(guy)

def fight(who):
    global current_location
    #peeps=pygame.sprite.spritecollideany(who, main_player, False)
    peeps=[]
    for guy in current_location.npc:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for guy in current_location.online_npcs:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for peep in peeps:
        peep.take_damage(25)
        send_to_host(['attack', peep.onlineID, 25])


def eat(who):
    global current_location, user
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
        

def end_game():
    global done, online
    """This stops the game loop and quits pygame."""
    try:
        if online==True:
            send_to_host('close_me')
            socksend.close()
            sockrec.close()
        online=False
        done = True
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
        global online, socksend, sockrec#, current_location
##        for guy in npc:
##            send_to_host(['spawnstatue',guy,guy.x-current_location.gamex,guy.y-current_location.gamey])
##        for dude in main_player:
##            for guy in dude.myarmy:
##                send_to_host(['spawnsoldier',guy,guy.x-current_location.gamex,guy.y-current_location.gamey])
##        for guy in main_player:
##            send_to_host(['spawnplayer',guy,guy.x-current_location.gamex,guy.y-current_location.gamey])
        #send_to_host('get_all_sprites')
        #sock.send('get_all_sprites'.encode('utf-8'))
        while online==True:
            try:
                message=recv_one_message(sockrec)
                #message=sockrec.recv(16000)
                #print(message)
                message=pickle.loads(message)
                translate(message)
            except ConnectionResetError:
                print("ERROR: lost connection")
                online=False
                remove_online_sprites()
            except ConnectionAbortedError:
                online=False
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
        global online, current_location#, socksend
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
                global clientlist
                clientlist.remove(self.sock)
                self.sock.close()
                self.running=False
                
def remove_player_sprites(plyr):
    global current_location
    for guy in current_location.online_players:
        if guy.serverparent==plyr:
            current_location.online_players.remove(guy)
    for guy in current_location.online_troops:
        if guy.serverparent==plyr:
            current_location.online_troops.remove(guy)
    if current_location.space_type=='none':  # this means planet
        # This is to delete him on all spaces, 
        # so an old sprite isn't waiting in space
        for guy in current_location.parent.online_players:
            if guy.serverparent==plyr:
                current_location.parent.online_players.remove(guy)
        for guy in current_location.parent.online_troops:
            if guy.serverparent==plyr:
                current_location.parent.online_troops.remove(guy)
                
    # TODO: location error might be in here:
    else:  # this means space
        for loc in current_location.planets:
            for guy in loc.online_players:
                if guy.serverparent==plyr:
                    current_location.online_players.remove(guy)
            for guy in loc.online_troops:
                if guy.serverparent==plyr:
                    current_location.online_troops.remove(guy)

def remove_online_sprites():
    global current_location #online_npcs, online_players, online_troops
    current_location.online_npcs.empty()
    current_location.online_players.empty()
    current_location.online_troops.empty()

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
    global online, host, port, socksend
    if online==True:
        try:
            #client(host, port, pickle.dumps(what))
            send_one_message(socksend, pickle.dumps(what))
            #return
            #print('') #this is only to make it stop between sends, not one long send
        except ConnectionResetError:
            online=False
            print("ERROR: Connection was lost. Please reconnect.")
            remove_online_sprites()

def sethost():
    global host, port
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    ip=0
    while ip==0:
        try:
            file=open("multiplayer_info.txt", 'r')
            host=file.read()
            ip=1
            print("Connecting to "+host)
        except NameError:
            print('ERROR: "multiplayer_info.txt" file not found.')
            ip=input("Enter the IP address of the host,\n"
                  "or leave blank to use your own IP address. ")
            if ip!="":
                host=ip
        except FileNotFoundError:
            print('ERROR: "multiplayer_info.txt" file not found.')
            ip=input("Enter the IP address of the host,\n"
                  "or leave blank to use your own IP address. ")
            if ip!="":
                host=ip

def go_online():
    try:
        #TODO: get rid of the global list main_players?
        # There is only one main player, others are online players
        # (2nd player?)
        global socksend, sockrec, port, host, online, parent, current_location
        global npc, main_players, user
        online=True
        socksend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockrec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sethost()
        socksend.connect((host, port))
        print(recv_one_message(socksend).decode('utf-8'))
        send_one_message(socksend, "send".encode('utf-8'))
        parent=recv_one_message(socksend).decode('utf-8')
        user.mysprite.serverparent=parent
        for troop in user.myarmy:
            #print("working")
            troop.serverparent=parent
        for guy in current_location.npc:
            guy.serverparent=parent
        sockrec.connect((host, port))
        print(recv_one_message(sockrec).decode('utf-8'))
        send_one_message(sockrec,"recv".encode('utf-8'))
        send_one_message(sockrec,pickle.dumps((parent, current_location)))
        hostthread=checkinghostThread()
        hostthread.start()
    except ConnectionRefusedError:
        print("ERROR: Connection Refused")
        online=False
        remove_online_sprites()
    except ConnectionResetError:
        online=False
        print("ERROR: Connection was reset. Please reconnect.")
        remove_online_sprites()    

def translate(message):
    global current_location, host, port, parent, clientlist
    if type(message)==str:
        print(message)
        #^^^^delete?
    if message[0]=="new_client":
        print("got new client")
        fromaddr=message[1]
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsock.connect((host, port))
        print(recv_one_message(clientsock).decode('utf-8'))
        send_one_message(clientsock, pickle.dumps([fromaddr, parent]))
        clientlist.append(clientsock)
        listen_to_client=checkingclientThread(clientsock, fromaddr)
        listen_to_client.start()
                
    if message[0]=='delete_player':
        print('delete')
        if current_location.space_type=='none':  # this means planet
            for guy in current_location.online_players:
                if guy.serverparent==message[1]:
                    current_location.online_players.remove(guy)
            for guy in current_location.online_troops:
                if guy.serverparent==message[1]:
                    current_location.online_troops.remove(guy)
                    
            # This is to delete him on all spaces, 
            # so an old sprite isn't waiting in space
            for guy in current_location.parent.online_players:
                if guy.serverparent==message[1]:
                    current_location.parent.online_players.remove(guy)
            for guy in current_location.parent.online_troops:
                if guy.serverparent==message[1]:
                    current_location.parent.online_troops.remove(guy)
                    
        # TODO: location error might be in here:
        else:  # this means space
            for guy in current_location.online_players:
                if guy.serverparent==message[1]:
                    current_location.online_players.remove(guy)
            for guy in current_location.online_troops:
                if guy.serverparent==message[1]:
                    current_location.online_troops.remove(guy)
            for loc in current_location.planets:
                for guy in loc.online_players:
                    if guy.serverparent==message[1]:
                        current_location.online_players.remove(guy)
                for guy in loc.online_troops:
                    if guy.serverparent==message[1]:
                        current_location.online_troops.remove(guy)
    
    if message[0]=="get_all_sprites":
        reply_to=message[1]
        for guy in current_location.npc:
            send_to_host(["just_one",reply_to,['spawnstatue',guy,guy.x-current_location.gamex,guy.y-current_location.gamey]])
        for guy in user.myarmy:
            send_to_host(["just_one",reply_to,['spawnsoldier',guy,guy.x-current_location.gamex,guy.y-current_location.gamey]])
        for guy in main_players:
            send_to_host(["just_one",reply_to,['spawnplayer',guy,guy.x-current_location.gamex,guy.y-current_location.gamey]])
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
        message[1].x=message[2]+current_location.gamex
        message[1].y=message[3]+current_location.gamey
        message[1].set_rect()
        
        current_location.online_troops.add(message[1])
    elif message[0]=='spawnplayer':
        if message[1].character == "tyranid":
            change_character(message[1], 'tyranid/player')
        elif message[1].character=="human":
            change_character(message[1], 'human/player')
        message[1].x=message[2]+current_location.gamex
        message[1].y=message[3]+current_location.gamey
        message[1].set_rect()
        current_location.online_players.add(message[1])
    elif message[0]=='attack':
        for guy in current_location.online_npcs:
            if guy.onlineID==message[1]:
                guy.take_damage(message[2])
        for guy in current_location.npc:
            if guy.onlineID==message[1]:
                guy.health=0
                guy.alive=False
    elif message[0]=='killnpc':
        for guy in current_location.online_npcs:
            if guy.onlineID==message[1]:
                guy.take_damage(10000)
        for guy in current_location.npc:
            if guy.onlineID==message[1]:
                guy.take_damage(10000)
    elif message[0]=='deletenpc':
        for guy in current_location.online_npcs:
            if guy.onlineID==message[1]:
                current_location.online_npcs.remove(guy)
        for guy in current_location.npc:
            if guy.onlineID==message[1]:
                current_location.npc.remove(guy)
    elif message[0]=='spawnstatue':
        message[1].set_image()
        message[1].x=message[2]+current_location.gamex
        message[1].y=message[3]+current_location.gamey
        message[1].set_rect()
        current_location.online_npcs.add(message[1])
    elif message[0]=='movenpc':
        for thing in current_location.online_npcs:
            if thing.onlineID==message[1]:
                thing.x=message[2]+current_location.gamex
                thing.y=message[3]+current_location.gamey
                thing.set_rect()
    elif message[0]=='moveright':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="right"
                    guy.facing="right"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
    elif message[0]=='moveleft':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
    elif message[0]=='movedown':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
    elif message[0]=='moveup':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    

#------------------END OF ONLINE FUNCTIONS-----------------------------------------






#___________________________________________________________________________
#***************************************************************************
#------------------------------START GAME:----------------------------------
    
    
def main_game_loop():
    
    # Initialize the game engine
    pygame.init()


    # After "gamevars" is passed to functions,
    # delete global variables.
    global online, online2
    global background, game_map
    global gamew, gameh
    #global npc, online_npcs, online_troops
    global user, main_players, clientlist, parent  #replace this parent with server_parent
    global walls, screensquares, left_rect, right_rect, toprect, bottomrect, spawningoffscreen
    global myTick, keyTime
    global ppushed
    global socksend, sockrec, host, port
    global current_location
    global gamesize, playerkind, main_players
    global fullwidth, fullheight
    global my_screen, fullscrn
    global dragging
    
    dragging=False
        

    
    
    # Get the screen resolution for fullscreen
    
    fullwidth = GetSystemMetrics(0)
    fullheight = GetSystemMetrics(1)
    
    
    
    # Set the screen size and caption
    gamesize=(1000,700)
    
    #my_screen=screen
    fullscrn=0
    my_screen = pygame.display.set_mode(gamesize)
    pygame.display.set_caption("WarHammer 40k")
    #my_screen = pygame.FULLSCREEN
    
    
    # later this will call the main menu
    playerkind, fullscrn=ask_player(my_screen, gamesize)
    
    
    # Used to manage how fast the my_screen updates
    clock = pygame.time.Clock()
    
    # Global variables and lists:
    # Object containing all variables:
    gamevars= Game_variables(playerkind, gamesize)    # (Later this object will be passed around)
    
    # this loads the saved or default maps of space objects
    game_map, current_location=loading_game()
    
    #should the loading go here? 
    load_planet(current_location)  # it's in the loading game function right now
    
    
    # this creates the user, must be after current_location is created.
    user=Main_Player(playerkind, parent)
    #user=MainCharacter( playerkind, parent, name="Player")
    main_players.append(user.mysprite)
    
    
    global botbar
    
    #uiunitx, uiunity = gamesize[0]//36, (gamesize[1]*4)//8.5
    
    botbar=UI_bar('player')
    
    botbar.myhotkeys[0].contains=Icon_square('pistol')
    botbar.myhotkeys[1].contains=Icon_square('club')
    
    
    # move this to a tyranid specific function:
    user.biomatter=400
    print("biomatter:"+str(user.biomatter))
    
    
    
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
        if user.character=='tyranid':
            tyranid_inputs()
        elif user.character=="human":
            human_inputs()
        elif user.character=='tau':
            tau_inputs()
        elif user.character=='eldar':
            eldar_inputs()
        elif user.character=='dark_eldar':
            darkeldar_inputs()
        elif user.character=='chaos':
            chaos_inputs()
     
    
    
        # --- EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
    
    
    
    
    
    
    
        # --- GAME LOGIC SHOULD GO BELOW THIS COMMENT
    
        
    
    
        # This checks if troops are doing damage as they run around
        # TODO: change this so it spams the attack button, which only
        # works when cooldown time has passed.
        swinging()
        
    
    
            
        
    
        # --- GAME LOGIC SHOULD GO ABOVE THIS COMMENT
    
    
    
    
    
    
        # --- DRAWING CODE SHOULD GO BELOW THIS COMMENT
    
    
        
        # First, clear the my_screen to grey. Don't put other drawing commands
        # above this, or they will be erased with this command.
    
    
        my_screen.fill((175, 175, 175)) # GREY
        
        fill_background(my_screen)
    
        if current_location.space_type=='none':   #this means it is a planet
            planet_display(my_screen)
        else:
            space_display(my_screen)
            
        
        # This displays the user interface:
        player_view(my_screen, botbar)
        
        
        pygame.display.flip() # this updates whole screen
        #pygame.display.update() # this updates only parts of the screen
        
    
        
        # --- DRAWING CODE SHOULD GO ABOVE THIS COMMENT
    
    
    
        # --- Limit to (change to 60?) frames per second
    
    
        clock.tick(20)  # this is how fast the game runs. it comes with pygame
    
        myTick=myTick+1
        if myTick>1000:
            myTick=0
    
    
    
    
#______________________________
    

    


if __name__=="__main__":
    main_game_loop()

