
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
from pygame.locals import *
from win32api import GetSystemMetrics  # for getting the screen resolution
#from pygame.examples.__movie_test import screen

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
        

        
        # global lists:
    
        #global npc, online_npcs, online_troops
        #npc=pygame.sprite.Group()
        #online_npcs=pygame.sprite.Group()
        
        #online_troops=pygame.sprite.Group()
        
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
        
        #on_edge=False
        
        spawningoffscreen=False
        
        global myTick, keyTime
        myTick=0
        keyTime=0
        
        global ppushed, pppushed
        ppushed=0
        pppushed=0
        
        global newwguy, socksend, sockrec, host, port

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
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.x=0
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        
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
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.x=0
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        
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
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.x=0
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        
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
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.x=0
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        


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
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
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
        self.width=width//5
        self.height=height//2
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))


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
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))

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
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))

class Unknown_menu():
    def __init__(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.image = pygame.image.load('sprites/ui/unknown_menu.png')
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))
        self.visible=False
    def resize(self):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//5
        self.height=height//2
        self.x=width*(4/5)
        self.y=height*(1/4)
        self.image=pygame.transform.scale(self.image, (self.width, self.height))

class Button():
    def __init__(self, name, kind, x, y, opens='none'):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//38
        self.height=height//38
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
        elif self.name=='unknown_menu':
            self.image = pygame.image.load('sprites/ui/unknown.png')
        else:
            self.image='none'
        if self.image!='none':
            self.image=pygame.transform.scale(self.image, (self.width, self.height))
        
    def resize(self, x, y):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//38
        self.height=height//38
        self.x=x
        self.y=y
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
        if self.image!='none':
            self.image=pygame.transform.scale(self.image, (self.width, self.height))
    def myclick(self):
        global botbar
        if self.kind=='leftmenu':
            if type(self.opens)!=str:
                if self.opens.visible==False:
                    self.opens.visible=True
                    if self.name=='wearing_menu':
                        botbar.myskills.visible=False
                        botbar.mytroops.visible=False
                        botbar.mygroups.visible=False
                    if self.name=='skills_menu':
                        botbar.wearing.visible=False
                        botbar.mytroops.visible=False
                        botbar.mygroups.visible=False
                    if self.name=='troops_menu':
                        botbar.myskills.visible=False
                        botbar.wearing.visible=False
                        botbar.mygroups.visible=False
                    if self.name=='groups_menu':
                        botbar.myskills.visible=False
                        botbar.mytroops.visible=False
                        botbar.wearing.visible=False
                else:
                    self.opens.visible=False
        if self.kind=='rightmenu':
            if type(self.opens)!=str:
                if self.opens.visible==False:
                    self.opens.visible=True
                    if self.name=='inventory_menu':
                        botbar.weapon_skills.visible=False
                        botbar.buildings.visible=False
                        botbar.unknown.visible=False
                    if self.name=='weapon_skills_menu':
                        botbar.inventory.visible=False
                        botbar.buildings.visible=False
                        botbar.unknown.visible=False
                    if self.name=='buildings_menu':
                        botbar.weapon_skills.visible=False
                        botbar.inventory.visible=False
                        botbar.unknown.visible=False
                    if self.name=='unknown_menu':
                        botbar.weapon_skills.visible=False
                        botbar.buildings.visible=False
                        botbar.inventory.visible=False
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
                botbar.unknown.visible=False

            
        

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
            self.y=gamesize[1]*(4/4.5)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
            # Build side menus:
            self.wearing=Wearing_menu()
            self.myskills=Skills_menu()
            self.mytroops=Troop_menu()
            self.mygroups=Groups_menu()
            self.inventory=Inventory_menu()
            self.weapon_skills=Weapon_skills_menu()
            self.buildings=Small_structures_menu()
            self.unknown=Unknown_menu()
            
            
            
            for square in range(12):
                self.myhotkeys.append(UI_square('hot_key',
                                                (self.width//55)+(square)*(self.width//27.2), 
                                                self.y+self.height//3))
            

            
            # Left menu buttons:
            self.myleftbuttons.append(Button('wearing_menu', 'leftmenu',
                                            (self.width//55)+( 0 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.wearing))
            self.myleftbuttons.append(Button('skills_menu', 'leftmenu',
                                            (self.width//55)+( 1 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.myskills))
            self.myleftbuttons.append(Button('troops_menu', 'leftmenu',
                                            (self.width//55)+( 2 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.mytroops))
            self.myleftbuttons.append(Button('groups_menu', 'leftmenu',
                                            (self.width//55)+( 3 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.mygroups))
            self.myleftbuttons.append(Button('closeleft', 'close',
                                            (self.width//55)+( 4 )*(self.width//26.8), 
                                            (height*5.7)//6.4))
            
            # Right menu buttons:
            self.myrightbuttons.append(Button('inventory_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 0 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.inventory))
            self.myrightbuttons.append(Button('weapon_skills_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 1 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.weapon_skills))
            self.myrightbuttons.append(Button('buildings_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 2 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.buildings))
            self.myrightbuttons.append(Button('unknown_menu', 'rightmenu',
                                            ((self.width*6.3)//8)+( 3 )*(self.width//26.8), 
                                            (height*5.7)//6.4,
                                            self.unknown))
            self.myrightbuttons.append(Button('closeright', 'close',
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
        self.unknown.resize()
        
        count=0
        for square in self.myhotkeys:
            square.resize((self.width//55)+(count)*(self.width//27.2), 
                                                self.y+self.height//3)
            count+=1
            
        count=0
        for bttn in self.myleftbuttons:
            bttn.resize((self.width//55)+( count )*(self.width//26.8), 
                                            (height*5.7)//6.4)
            count+=1
            
        
        count=0
        for bttn in self.myrightbuttons:
            bttn.resize(((self.width*6.3)//8)+( count )*(self.width//26.8), 
                                            (height*5.7)//6.4)
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
        self.visible=True
        self.x=x
        self.y=y
        self.moving=False
        self.image='none'
        self.contains='empty'
        self.kind=kind
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def resize(self, x, y):
        global gamesize, fullscrn, fullwidth, fullheight
        if fullscrn==0:
            width, height=gamesize
        elif fullscrn==1:
            width=fullwidth
            height=fullheight
        self.width=width//36
        self.height=height//36
        self.x=x
        self.y=y
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
        
class Moving_square():
    def __init__(self, rect, holding, parent):
        self.parent=parent
        self.holding=holding
        self.rect=pygame.Rect(rect)

    
def unclicked(bttn):
    global dragging
    if bttn.contains=='empty':
        bttn.contains=dragging.holding
        dragging.parent.contains='empty'
    elif bttn!=dragging.parent:
        dragging.parent.contains=bttn.contains
        bttn.contains=dragging.holding 
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

            
class MainPlayer():
    def __init__(self, kind, serverparent, name="none"):
        self.myarmy=pygame.sprite.Group()
        self.myships=[]
        self.myarmy.biomatter=0
        self.mysprite=Player('tyranid',parent,name="Player")
        self.character=kind

# rename Player into character
class Player(pygame.sprite.Sprite):
    """Each minion can receive commands from the user and give commands to other minions.
    All minions can level up, earn xp, and be killed.
    For now the variable user is also a minion with the name player.
    Later, add inventory for each minion.
    """
    def __init__(self, kind, serverparent, name="none"):
        """When instance is created set the name and default stats.
        Make a function for default names if no name is entered.
        """
        pygame.sprite.Sprite.__init__(self)
        
        # remove these when MainPlayer is working:
        #self.myarmy=[]
        self.myarmy=pygame.sprite.Group()
        self.myships=[]
        self.myarmy.biomatter=0
        self.character=kind
        #
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
            elif kind=="spacemarine":
                change_character(self, 'spacemarine/player')
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
            elif kind=="spacemarine":
                change_character(self, 'spacemarine/troop')
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
        while self.xp>=100:
            self.level=self.level+1
            self.xp=self.xp-100

            
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

#class Group:
#    """This makes a list for minions or enemies.
#    For now this is only used for myarmy and npc.
##    Player is the only minion not added to a list of this class.
#    """
#    def __init__(self, name):
#        """Sets the name and creates a blank list."""
#        pygame.sprite.Group.__init__(self)
#        self.name=name
#        self.members=[]
#
#    def new_member(self, itsname):
#        """Adds a minion to the list. Not yet in use."""
#        self.members.append(Player(itsname))
#    
#    def get_members(self):
#        """Returns a list of members as objects."""
#        return self.members
#
#    def set_members(self, newarmy):
#        """This is in case another function edits the list and sets it. Not yet in use."""
#        self.members=newarmy


def troop_formations_line(leader, guys):
    #guys=leader.myarmy.sprites()
    trooplength=len(guys)
    global user
    change_character(user, "spacemarine/charles")
    try:
        unitlength=trooplength//4
        if unitlength>=0:
            troopspace=300/unitlength
            troopcount=0
            done_troops=0
            for guy in guys[0: unitlength]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(-60,(-150+troopcount*troopspace))
                change_character(guy, "spacemarine/archers")
                done_troops+=1
            troopcount=0
            for guy in guys[unitlength: unitlength*2]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(120,(-350+troopcount*troopspace))
                change_character(guy, "spacemarine/hwan")
                #pygame.transform.scale(guy.image, (30, 50))
                done_troops+=1
            troopcount=0
            for guy in guys[2*unitlength: unitlength*3]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(150,(-150+troopcount*troopspace))
                change_character(guy, "spacemarine/hwan")
                done_troops+=1
            troopcount=0
            for guy in guys[3*unitlength: unitlength*4]:
                troopcount+=1
                guy.following=leader
                guy.direction="formation"
                guy.anchor=(120,(50+troopcount*troopspace))
                change_character(guy, "spacemarine/hwan")
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
    #guys=leader.myarmy.sprites()
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
                    
                    

def planet_inputs():
        global user, current_location, ppushed, pppushed
        global playerkind, online,newwguy
        global spawningoffscreen
        global botbar, dragging
    # can have different functions for different classes
    
        # events for txtbx
    
    #this tells you the index number of the keys being pressed
    #    thekeys=pygame.key.get_pressed()
    #    for indexed in thekeys:
    #        if indexed==True:
    #            print(thekeys.index(indexed))
    
        pushed_keys=pygame.key.get_pressed()
    
        if pushed_keys[119] == True:  # "w" key
            user.direction="up"
        elif pushed_keys[115] == True:  # "s" key
            user.direction="down"
        elif pushed_keys[97] == True:  # "a" key
            user.direction="left"
        elif pushed_keys[100] == True:  # "d" key
            user.direction="right"
        else:
            user.direction="none"
    
        if len(main_players)>1:
            if pushed_keys[117] == True:  # "u" key
                newwguy.direction="up"
            elif pushed_keys[106] == True:  # "j" key
                newwguy.direction="down"
            elif pushed_keys[104] == True:  # "h" key
                newwguy.direction="left"
            elif pushed_keys[107] == True:  # "k" key
                newwguy.direction="right"
            else:
                newwguy.direction="none"
            
    
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
    
        if len(main_players)>1:
            if pushed_keys[112] == True:  # "p" key
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "up"
            elif pushed_keys[59] == True:  # ";" key
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "down"
            elif pushed_keys[108] == True:  # "l" key
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "left"
            elif pushed_keys[39] == True:  # " ' " key
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "right"
            else:
                for thing in newwguy.myarmy:
                    if (thing.direction!="follow"
                        and thing.direction!="here"):
                        #and thing.selected==True
                        thing.direction = "none"
                        
        if pushed_keys[113] == True:     #  "q" button
            if ppushed==0:
                if user.myarmy.biomatter>=100:
                    user.myarmy.biomatter=user.myarmy.biomatter-100
                    user.myarmy.add(Player(playerkind,parent,name="minion"))
                    print("Biomatter: "+str(user.myarmy.biomatter))
                    ppushed+=1
                else:
                    print("Not enough biomatter.")
                    ppushed=100
                
            elif ppushed<3:
                ppushed+=1
            elif ppushed!=100:
                ppushed=0
        else:
            ppushed=0
    
        if pushed_keys[105] == True:    # "i" key
            if len(main_players)>1:
                if pppushed==0:
                    if newwguy.myarmy.biomatter>=100:
                        newwguy.myarmy.biomatter=newwguy.myarmy.biomatter-100
                        newwguy.myarmy.add(Player(newwguy.character,parent,name="minion"))
                        print("Biomatter: "+str(newwguy.myarmy.biomatter))
                        pppushed+=1
                    else:
                        print("Not enough biomatter.")
                        pppushed=100
                    
                elif pppushed<3:
                    pppushed+=1
                elif pppushed!=100:
                    pppushed=0
        else:
            pppushed=0
                            
        events = pygame.event.get()
    
        for event in events:  # User did something
    
            
            
            if event.type == pygame.QUIT: # User clicked close
                end_game()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button)==1:      #  Left mouse click
                    pos = pygame.mouse.get_pos()
                    
                    ## check if cursor is on button ##
                    found=False
                    for bttn in botbar.myleftbuttons:
                        if bttn.rect.collidepoint(pos)==True:
                            bttn.myclick()
                            found=True
                    for bttn in botbar.myrightbuttons:
                        if bttn.rect.collidepoint(pos)==True:
                            bttn.myclick()
                            found=True
                    for bttn in botbar.myhotkeys:
                        if bttn.rect.collidepoint(pos)==True and type(bttn.contains)!=str:
                            bttn.myclick()
                            found=True 
                            
                    # TODO, replace clicked on function, use collide instead
                    if found==False and clicked_on(pos)==False:  
                        for kid in user.myarmy.sprites():
                            if kid.selected==True:
                                kid.attacking=False
                                kid.eating=False
                                kid.go_here=pos
                                kid.direction="here"
                                
                if event.button==3:       #  Right mouse click
                    for kid in user.myarmy.sprites():
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
#                 if (mykeys[K_a]):
#                     user.direction = LEFT
#                     keyTime=myTick
#                 if (mykeys[K_d]):
#                     user.direction = RIGHT
#                     keyTime=myTick
#                 if (mykeys[K_w]):
#                     user.direction = UP
#                     keyTime=myTick
#                 if (mykeys[K_s]):
#                     user.crouch = True
#                     user.direction = DOWN
#                     keyTime=myTick

#                 if (mykeys[K_LEFT]):
#                     for thing in myarmy:
#                         if thing.selected==True:
#                             thing.direction = LEFT
#                     keyTime=myTick
#                 if (mykeys[K_RIGHT]):
#                     for thing in myarmy:
#                         if thing.selected==True:
#                             thing.direction = RIGHT
#                     keyTime=myTick
#                 if (mykeys[K_UP]):
#                     for thing in myarmy:
#                         if thing.selected==True:
#                             thing.direction = UP
#                     keyTime=myTick
#                 if (mykeys[K_DOWN]):
#                     for thing in myarmy:
#                         if thing.selected==True:
#                             thing.direction = DOWN
#                     keyTime=myTick

                    
                if event.key == K_BACKSLASH:
                    togfullscreen()

                if event.key == K_f:
                    for guy in user.myarmy.sprites():
                        guy.direction="follow"
                        guy.following=user
                        guy.attacking=False
                        guy.eating=False

                if event.key == K_r:
                    for guy in user.myarmy.sprites():
                        guy.direction="none"
                        guy.attacking=False
                        guy.eating=False

                if event.key == K_z:
                    current_location.npc.add(Statue("Statue"))
                    
                if event.key == K_ESCAPE:
                    end_game()

                if event.key == K_e:
                    eat(user)
                    for guy in user.myarmy:
                        if guy.selected==True:
                            eat(guy)
                            
                if event.key == K_SPACE:
                    fight(user)
                    #user.jump = True  # or call a jump function

                if event.key == K_RSHIFT or event.key == K_LSHIFT:
                    for guy in user.myarmy:
                        if guy.selected==True:
                            fight(guy)

                if event.key==K_c:
                    any_kids=[]
                    eat_it=[]
                    for each in user.myarmy.sprites():
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
                    for each in user.myarmy.sprites():
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

                if event.key==K_TAB:
                    selected_troops=[]
                    for guy in user.myarmy.sprites():
                        if guy.age=="adult" and guy.selected==True:
                            selected_troops.append(guy)
                    if selected_troops!=[]:
                        user.controlling=False
                        user.selected=False
                        if user.character=='tyranid':
                            change_character(user,"tyranid/adult")
                        elif user.character=='spacemarine':
                            change_character(user,"spacemarine/adult")
                        user.myarmy.add(user)
                        main_players.remove(user)
                        temp_num=random.randint(0,len(selected_troops)-1)
                        newmainguy=selected_troops[temp_num]
                        newmainguy.myarmy=user.myarmy
                        user.myarmy=[]
                        user=newmainguy
                        
                        main_players.append(user)

                        user.myarmy.remove(user)

                        user.controlling=True
                        user.selected=False
                        if user.character=='tyranid':
                            change_character(user,"tyranid/player")
                        elif user.character=='spacemarine':
                            change_character(user,"spacemarine/player")
                        jump_here()

                if event.key==K_LEFTBRACKET:
                    newwguy=Player('tyranid',parent,name="Player")
                    main_players.add(newwguy)
                    newwguy.myarmy.biomatter=100

                if event.key==K_RIGHTBRACKET:
                    newwguy=Player('spacemarine',parent,name="Player")
                    main_players.add(newwguy)
                    newwguy.myarmy.biomatter=100

                if event.key==K_b:
                    fight(newwguy)

                if event.key==K_v:
                    for guy in newwguy.myarmy:
                        if guy.selected==True:
                            fight(guy)

                if event.key==K_y:
                    eat(newwguy)
                    for guy in newwguy.myarmy:
                        eat(guy)

                if event.key==K_g:
                    for guy in newwguy.myarmy.sprites():
                        guy.direction="follow"
                        guy.following=newwguy
                        guy.attacking=False
                        guy.eating=False

                if event.key == K_t:
                    for guy in newwguy.myarmy.sprites():
                        guy.direction="none"
                        guy.attacking=False
                        guy.eating=False

                if event.key==K_n:
                    any_kids=[]
                    eat_it=[]
                    for each in newwguy.myarmy.sprites():
                        if each.age!="adult":
                            any_kids.append(each)
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
                        for each in newwguy.myarmy:
                            if each.age=="adult":
                                if eat_it!=[]:
                                    each.attacking=False
                                    each.eating=True
                                    each.go_here=eat_it[0].rect.center
                                    each.direction="here"
                                    del eat_it[0]

                if event.key==K_m:
                    any_adults=[]
                    kill_it=[]
                    for each in newwguy.myarmy.sprites():
                        if each.age=="adult":
                            any_adults.append(each)
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
                        for each in newwguy.myarmy:
                            if each.age!="adult":
                                if kill_it!=[]:
                                    each.attacking=True
                                    each.eating=False
                                    each.go_here=kill_it[0].rect.center
                                    each.direction="here"
                                    del kill_it[0]

                if event.key==K_9:
                    print("You have "+str(len(user.myarmy.sprites()))+" troops.")

                if event.key==K_8:
                    print("There are "+str(len(current_location.npc.sprites()))+" enemies.")
                    
                if event.key==K_0:
                    print("Your screen location:\n"+
                          "X = "+str(-current_location.gamex)+
                          "\nY = "+str(-current_location.gamey))

                if event.key==K_6:
                    if spawningoffscreen==False:
                        spawningoffscreen=True
                        print("spawning on")
                    else:
                        spawningoffscreen=False
                        print("spawning off")
                        
                     
                     
                
                if event.key==K_BACKQUOTE:
                    user.myarmy.biomatter+=1000000
                    print("YouRich BEEEITCH!!!!")
                
                if event.key==K_4:
                    troop_formations_line(user, user.myarmy.sprites())
                       
                if event.key==K_5:
                    troop_formations_square(user, user.myarmy.sprites())

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

                    
                if event.key== K_1:
                    spawn_ship(user)
                
                if event.key==K_2:
                    load_space(current_location.parent)
                    current_location=current_location.parent

                #if event.key==K_3:
                    # this is for landing on planets
                    # if overlapping a planet: land
                    # TODO: planets location loads in space, before i can land
                    
                    
                if event.key == K_RETURN:
                    if current_location.space_type!="none":
                        #warp=warpmenuThread(current_location)
                        #warp.start()
                        current_location=warpmenu(current_location)
                    
                    
                    
                #if (mykeys[K_`]):
                    #ask_player()  # this is what gets the input from the player

                #if (mykeys[K_b]):
                    #words_box=eztext.Input(maxlength=45, color=(255,0,0), prompt='type here: ')
                        #boxx(30,50)
                    #using_menu=True
                    #words_box.typing()

            
                

#         elif event.type == KEYUP:     # if they release a button but are still holding another one down
#             mykeys=pygame.key.get_pressed() 
#             if ((mykeys[K_a])
#                  or(mykeys[K_d])
#                  or(mykeys[K_w])
#                  or(mykeys[K_s]))==False:
#                 user.direction = "none"
#                 user.jump = False
#                 user.crouch = False
#             if ((mykeys[K_LEFT])
#                  or(mykeys[K_RIGHT])
#                  or(mykeys[K_UP])
#                  or(mykeys[K_DOWN]))==False:
#                 for guy in myarmy:
#                     if (guy.selected==True
#                         and guy.direction!="here"):
#                         guy.direction="none"
                
    
        

    #if e is pressed:
        #action=True
    #else:
        #action=False

    #if p is pressed:  #planning mode  (for commanding and building)
        #who=ask who, map or grid?
        #command(who)
    
    
    
def move_me(who):
    global current_location
    who.mytick+=1
    if who==user:
        if toprect.colliderect(user.rect) and user.direction=="up":
            antimove('up')
        if bottomrect.colliderect(user.rect) and user.direction=="down":
            antimove('down')
        if left_rect.colliderect(user.rect) and user.direction=="left":
            antimove('left')
        if right_rect.colliderect(user.rect) and user.direction=="right":
            antimove('right')
    if who.direction == 'right':
        send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
        who.facing="right"
        who.x += 5
        who.rect=who.rect.move(5,0)
        if who.mytick<=2:
            who.image=who.walking_rightA
        elif who.mytick<=4:
            who.image=who.walking_rightB
        elif who.mytick<=6:
            who.image=who.walking_rightC
        else:
            who.mytick=0
    elif who.direction == 'down':
        send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
        #this is for the 3d setting:
        if who.character!="tyranid":
            who.facing='down'
            if who.mytick<=3:
                who.image=who.walking_downA
            elif who.mytick<=6:
                who.image=who.walking_downB
            else:
                who.mytick=0
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
        if who.mytick<=2:
            who.image=who.walking_leftA
        elif who.mytick<=4:
            who.image=who.walking_leftB
        elif who.mytick<=6:
            who.image=who.walking_leftC
        else:
            who.mytick=0
    elif who.direction == 'up':
        send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
        #this is for the 3d setting:
        if who.character!="tyranid":
            who.facing='up'
            if who.mytick<=3:
                who.image=who.walking_upA
            elif who.mytick<=6:
                who.image=who.walking_upB
            else:
                who.mytick=0
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
            if who.mytick<=2:
                who.image=who.walking_rightA
            elif who.mytick<=4:
                who.image=who.walking_rightB
            elif who.mytick<=6:
                who.image=who.walking_rightC
            else:
                who.mytick=0
        elif who.x>who.following.x+30:
            send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="left"
            who.x -= 5
            who.rect=who.rect.move(-5,0)
            if who.mytick<=2:
                who.image=who.walking_leftA
            elif who.mytick<=4:
                who.image=who.walking_leftB
            elif who.mytick<=6:
                who.image=who.walking_leftC
            else:
                who.mytick=0
        elif who.y<who.following.y-30:
            send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y += 5
            who.rect=who.rect.move(0,5)
            if who.character!='tyranid':
                who.facing="down"
                if who.mytick<=3:
                    who.image=who.walking_downA
                elif who.mytick<=6:
                    who.image=who.walking_downB
                else:
                    who.mytick=0
        elif who.y>who.following.y+30:
            send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y -= 5
            who.rect=who.rect.move(0,-5)
            if who.character!='tyranid':
                who.facing="up"
                if who.mytick<=3:
                    who.image=who.walking_upA
                elif who.mytick<=6:
                    who.image=who.walking_upB
                else:
                    who.mytick=0
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
            if who.mytick<=2:
                who.image=who.walking_rightA
            elif who.mytick<=4:
                who.image=who.walking_rightB
            elif who.mytick<=6:
                who.image=who.walking_rightC
            else:
                who.mytick=0
        elif who.x>who.go_here[0]+5-(who.rect.height/2):
            send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="left"
            who.x -= 5
            who.rect=who.rect.move(-5,0)
            if who.mytick<=2:
                who.image=who.walking_leftA
            elif who.mytick<=4:
                who.image=who.walking_leftB
            elif who.mytick<=6:
                who.image=who.walking_leftC
            else:
                who.mytick=0
        elif who.y<who.go_here[1]-5-(who.rect.height/2):
            send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y += 5
            who.rect=who.rect.move(0,5)
            if who.character!='tyranid':
                who.facing="down"
                if who.mytick<=3:
                    who.image=who.walking_downA
                elif who.mytick<=6:
                    who.image=who.walking_downB
                else:
                    who.mytick=0
        elif who.y>who.go_here[1]+5-(who.rect.height/2):
            send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y -= 5
            who.rect=who.rect.move(0,-5)
            if who.character!='tyranid':
                who.facing="up"
                if who.mytick<=3:
                    who.image=who.walking_upA
                elif who.mytick<=6:
                    who.image=who.walking_upB
                else:
                    who.mytick=0
        else:
            who.direction="none"
    elif who.direction=="follow":
        if who.x<who.following.x-30:
            send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="right"
            who.x += 5
            who.rect=who.rect.move(5,0)
            if who.mytick<=2:
                who.image=who.walking_rightA
            elif who.mytick<=4:
                who.image=who.walking_rightB
            elif who.mytick<=6:
                who.image=who.walking_rightC
            else:
                who.mytick=0
        elif who.x>who.following.x+30:
            send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="left"
            who.x -= 5
            who.rect=who.rect.move(-5,0)
            if who.mytick<=2:
                who.image=who.walking_leftA
            elif who.mytick<=4:
                who.image=who.walking_leftB
            elif who.mytick<=6:
                who.image=who.walking_leftC
            else:
                who.mytick=0
        elif who.y<who.following.y-30:
            send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y += 5
            who.rect=who.rect.move(0,5)
            if who.character!='tyranid':
                who.facing="down"
                if who.mytick<=3:
                    who.image=who.walking_downA
                elif who.mytick<=6:
                    who.image=who.walking_downB
                else:
                    who.mytick=0
        elif who.y>who.following.y+30:
            send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y -= 5
            who.rect=who.rect.move(0,-5)
            if who.character!='tyranid':
                who.facing="up"
                if who.mytick<=3:
                    who.image=who.walking_upA
                elif who.mytick<=6:
                    who.image=who.walking_upB
                else:
                    who.mytick=0
        else:
            if who.facing=="right":
                who.image=who.standing_right
            elif who.facing=="left":
                who.image=who.standing_left
            elif who.facing=="down":
                who.image=who.standing_down
            elif who.facing=="up":
                who.image=who.standing_up
                
                
    elif who.direction=="formation":
        if who.x<who.following.x-5+who.anchor[0]:
            send_to_host(["moveright",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="right"
            who.x += 5
            who.rect=who.rect.move(5,0)
            if who.mytick<=2:
                who.image=who.walking_rightA
            elif who.mytick<=4:
                who.image=who.walking_rightB
            elif who.mytick<=6:
                who.image=who.walking_rightC
            else:
                who.mytick=0
        elif who.x>who.following.x+5+who.anchor[0]:
            send_to_host(["moveleft",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.facing="left"
            who.x -= 5
            who.rect=who.rect.move(-5,0)
            if who.mytick<=2:
                who.image=who.walking_leftA
            elif who.mytick<=4:
                who.image=who.walking_leftB
            elif who.mytick<=6:
                who.image=who.walking_leftC
            else:
                who.mytick=0
        elif who.y<who.following.y-5+who.anchor[1]:
            send_to_host(["movedown",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y += 5
            who.rect=who.rect.move(0,5)
            if who.character!='tyranid':
                who.facing="down"
                if who.mytick<=3:
                    who.image=who.walking_downA
                elif who.mytick<=6:
                    who.image=who.walking_downB
                else:
                    who.mytick=0
        elif who.y>who.following.y+5+who.anchor[1]:
            send_to_host(["moveup",who.name,who.onlineID, who.x-current_location.gamex, who.y-current_location.gamey])
            who.y -= 5
            who.rect=who.rect.move(0,-5)
            if who.character!='tyranid':
                who.facing="up"
                if who.mytick<=3:
                    who.image=who.walking_upA
                elif who.mytick<=6:
                    who.image=who.walking_upB
                else:
                    who.mytick=0
        else:
            if who.facing=="right":
                who.image=who.standing_right
            elif who.facing=="left":
                who.image=who.standing_left
            elif who.facing=="down":
                who.image=who.standing_down
            elif who.facing=="up":
                who.image=who.standing_up
    
    
    
def space_inputs():
        global user, current_location, ppushed,pppushed
        global playerkind, online,newwguy, socksend
            # can have different functions for different classes
    
        # events for txtbx
    
    #this tells you the index number of the keys being pressed
#         thekeys=pygame.key.get_pressed()
#         for indexed in thekeys:
#             if indexed==True:
#                 print(thekeys.index(indexed))
    
        pushed_keys=pygame.key.get_pressed()
    
        if pushed_keys[119] == True:
            user.direction="up"
        elif pushed_keys[115] == True:
            user.direction="down"
        elif pushed_keys[97] == True:
            user.direction="left"
        elif pushed_keys[100] == True:
            user.direction="right"
        else:
            user.direction="none"
    
        if len(main_players)>1:
            if pushed_keys[117] == True:
                newwguy.direction="up"
            elif pushed_keys[106] == True:
                newwguy.direction="down"
            elif pushed_keys[104] == True:
                newwguy.direction="left"
            elif pushed_keys[107] == True:
                newwguy.direction="right"
            else:
                newwguy.direction="none"
            
    
        if pushed_keys[273] == True:
            for thing in user.myarmy:
                if thing.selected==True:
                    thing.direction = "up"
        elif pushed_keys[274] == True:
            for thing in user.myarmy:
                if thing.selected==True:
                    thing.direction = "down"
        elif pushed_keys[276] == True:
            for thing in user.myarmy:
                if thing.selected==True:
                    thing.direction = "left"
        elif pushed_keys[275] == True:
            for thing in user.myarmy:
                if thing.selected==True:
                    thing.direction = "right"
        else:
            for thing in user.myarmy:
                if (thing.selected==True
                    and thing.direction!="here"
                    and thing.direction!="follow"):
                    thing.direction = "none"
    
        if len(main_players)>1:
            if pushed_keys[112] == True:
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "up"
            elif pushed_keys[59] == True:
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "down"
            elif pushed_keys[108] == True:
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "left"
            elif pushed_keys[39] == True:
                for thing in newwguy.myarmy:
                    #if thing.selected==True:
                        thing.direction = "right"
            else:
                for thing in newwguy.myarmy:
                    if (thing.direction!="follow"
                        and thing.direction!="here"):
                        #and thing.selected==True
                        thing.direction = "none"
                        
        if pushed_keys[113] == True:
            if ppushed==0:
                if user.myarmy.biomatter>=100:
                    user.myarmy.biomatter=user.myarmy.biomatter-100
                    user.myarmy.add(Player(playerkind,parent,name="minion"))
                    print("Biomatter: "+str(user.myarmy.biomatter))
                    ppushed+=1
                else:
                    print("Not enough biomatter.")
                    ppushed=100
                
            elif ppushed<3:
                ppushed+=1
            elif ppushed!=100:
                ppushed=0
        else:
            ppushed=0
    
        if pushed_keys[105] == True:
            if len(main_players)>1:
                if pppushed==0:
                    if newwguy.myarmy.biomatter>=100:
                        newwguy.myarmy.biomatter=newwguy.myarmy.biomatter-100
                        newwguy.myarmy.add(Player(newwguy.character,parent,name="minion"))
                        print("Biomatter: "+str(newwguy.myarmy.biomatter))
                        pppushed+=1
                    else:
                        print("Not enough biomatter.")
                        pppushed=100
                    
                elif pppushed<3:
                    pppushed+=1
                elif pppushed!=100:
                    pppushed=0
        else:
            pppushed=0
                            
        events = pygame.event.get()
    
        for event in events:  # User did something
            if event.type == pygame.QUIT: # User clicked close
                end_game()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button)==1:
                    #print(pygame.mouse.get_pos())
                    if clicked_on(pygame.mouse.get_pos())==False:
                        for kid in user.myarmy.sprites():
                            if kid.selected==True:
                                kid.attacking=False
                                kid.eating=False
                                kid.go_here=pygame.mouse.get_pos()
                                kid.direction="here"
                if event.button==3:
                    for kid in user.myarmy.sprites():
                        kid.selected=True
                    
            elif event.type == KEYDOWN:


                if (event.key==K_a or
                    event.key==K_d or
                    event.key==K_s or
                    event.key==K_w or
                    event.key==K_UP or
                    event.key==K_DOWN or
                    event.key==K_LEFT or
                    event.key==K_RIGHT):
                    keyTime=myTick

                if event.key==K_BACKSLASH:
                    
                    togfullscreen()


                if event.key == K_f:
                    for guy in user.myarmy.sprites():
                        guy.direction="follow"
                        guy.following=user
                        guy.attacking=False
                        guy.eating=False

                if event.key == K_r:
                    for guy in user.myarmy.sprites():
                        guy.direction="none"
                        guy.attacking=False
                        guy.eating=False

                if event.key == K_z:
                    current_location.npc.add(Statue("Statue"))
                    
                if event.key == K_ESCAPE:
                    end_game()

                if event.key == K_e:
                    eat(user)
                    for guy in user.myarmy:
                        if guy.selected==True:
                            eat(guy)
                            
                if event.key == K_SPACE:
                    fight(user)
                    #user.jump = True  # or call a jump function

                if event.key == K_RSHIFT or event.key == K_LSHIFT:
                    for guy in user.myarmy:
                        if guy.selected==True:
                            fight(guy)

                if event.key==K_c:
                    any_kids=[]
                    eat_it=[]
                    for each in user.myarmy.sprites():
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
                    for each in user.myarmy.sprites():
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

                if event.key==K_TAB:
                    selected_troops=[]
                    for guy in user.myarmy.sprites():
                        if guy.age=="adult" and guy.selected==True:
                            selected_troops.append(guy)
                    if selected_troops!=[]:
                        user.controlling=False
                        change_character(user,"tyranid/adult")
                        user.myarmy.add(user)
                        main_players.empty()
                        temp_num=random.randint(0,len(selected_troops)-1)
                        user=selected_troops[temp_num]
                        
                        main_players.add(user)

                        user.myarmy.remove(user)

                        user.controlling=True
                        user.selected=False
                        change_character(user,"tyranid/player")
                        jump_here()

                if event.key==K_LEFTBRACKET:
                    newwguy=Player( 'tyranid',parent,name="Player")
                    main_players.add(newwguy)
                    newwguy.myarmy.biomatter=100

                if event.key==K_RIGHTBRACKET:
                    newwguy=Player( 'spacemarine',parent,name="Player")
                    main_players.add(newwguy)
                    newwguy.myarmy.biomatter=100

                if event.key==K_b:
                    fight(newwguy)

                if event.key==K_v:
                    for guy in newwguy.myarmy:
                        if guy.selected==True:
                            fight(guy)

                if event.key==K_y:
                    eat(newwguy)
                    for guy in newwguy.myarmy:
                        eat(guy)

                if event.key==K_g:
                    for guy in newwguy.myarmy.sprites():
                        guy.direction="follow"
                        guy.following=newwguy
                        guy.attacking=False
                        guy.eating=False

                if event.key == K_t:
                    for guy in newwguy.myarmy.sprites():
                        guy.direction="none"
                        guy.attacking=False
                        guy.eating=False

                if event.key==K_n:
                    any_kids=[]
                    eat_it=[]
                    for each in newwguy.myarmy.sprites():
                        if each.age!="adult":
                            any_kids.append(each)
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
                        for each in newwguy.myarmy:
                            if each.age=="adult":
                                if eat_it!=[]:
                                    each.attacking=False
                                    each.eating=True
                                    each.go_here=eat_it[0].rect.center
                                    each.direction="here"
                                    del eat_it[0]

                if event.key==K_m:
                    any_adults=[]
                    kill_it=[]
                    for each in newwguy.myarmy.sprites():
                        if each.age=="adult":
                            any_adults.append(each)
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
                        for each in newwguy.myarmy:
                            if each.age!="adult":
                                if kill_it!=[]:
                                    each.attacking=True
                                    each.eating=False
                                    each.go_here=kill_it[0].rect.center
                                    each.direction="here"
                                    del kill_it[0]

                if event.key==K_9:
                    print("You have "+str(len(user.myarmy.sprites()))+" troops.")

                if event.key==K_8:
                    print("There are "+str(len(npc.sprites()))+" enemies.")
                    
                if event.key==K_0:
                    print("Your screen location:\n"+
                          "X = "+str(-current_location.gamex)+
                          "\nY = "+str(-current_location.gamey))

                if event.key==K_6:
                    if spawningoffscreen==False:
                        spawningoffscreen=True
                        print("spawning on")
                    else:
                        spawningoffscreen=False
                        print("spawning off")

                if event.key==K_BACKSPACE:
                    if online==False:
                        online2=True
                        socksend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sockrec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        host = socket.gethostname() # Get local machine name
                        port = 12345                # Reserve a port for your service.
                        go_online()

                if event.key==K_DELETE:
                    if online==True:
                        try:
                            send_to_host('close_me')
                            #sock.send('close'.encode('utf-8'))
                            #socksend.close()
                            #sockrec.close()
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

                    
                if event.key== K_1:
                    spawn_ship(user)
                
                if event.key==K_2:
                    #if user.myships!=[]:
                    for planets in current_location.planets:
                        if planets.rect.colliderect(user.rect):
                            load_planet(planets)
                            current_location=planets

                if event.key==K_3:
                    # this is for "planet assault" mode
                    # TODO this loads the giant planet, 
                    # and a new space matching planets gamex and gamey
                    for planets in current_location.planets:
                        if planets.rect.colliderect(user.rect):
                            load_planet_space(planets)
                            current_location=planets
                    
                    
                    
                if event.key == K_RETURN:
                    if current_location.space_type!="none":
                        #warp=warpmenuThread(current_location)
                        #warp.start()
                        current_location=warpmenu(current_location)
                    
                        
def togfullscreen():
    global fullscrn, my_screen, fullwidth, fullheight, botbar
    #print(my_screen.get_surface())
    if fullscrn == 0:
        fullscrn=1
        my_screen = pygame.display.set_mode((fullwidth,fullheight),pygame.FULLSCREEN)
        
        # TODO: move this to botbat.resize
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
    
        
        for playerss in main_players:
            for ship in playerss.myships:
                my_screen.blit(ship.image, (ship.x, ship.y))
            for guy in playerss.myarmy.sprites():
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
    
        for players in main_players:
            move_me(players)
            my_screen.blit(players.image, (players.x, players.y))


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
        
            
            for playerss in main_players:
                for ship in playerss.myships:
                    my_screen.blit(ship.image, (ship.x, ship.y))
                for guy in playerss.myarmy.sprites():
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
        
            for players in main_players:
                move_me(players)
                my_screen.blit(players.image, (players.x, players.y))
    
        else:    # this is if you are on the planet
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
        
            
            for playerss in main_players:
                for ship in playerss.myships:
                    my_screen.blit(ship.image, (ship.x, ship.y))
                for guy in playerss.myarmy.sprites():
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
        
            for players in main_players:
                move_me(players)
                my_screen.blit(players.image, (players.x, players.y))
        
    
    
    #    my_screen.blit(background, (current_location.gamex, current_location.gamey))
    
        #pygame.draw.rect(my_screen,WHITE,user.rect)
        #pygame.draw.rect(my_screen,WHITE,toprect)
        #pygame.draw.rect(my_screen,WHITE,bottomrect)
        #pygame.draw.rect(my_screen,WHITE,left_rect)
        #pygame.draw.rect(my_screen,WHITE,right_rect)
    
    
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
    
        # --- update the my_screen 
            # blit txtbx on the sceen
     
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
        if botbar.wearing.visible==True:
            my_screen.blit(botbar.wearing.image, (botbar.wearing.x, botbar.wearing.y))
        if botbar.myskills.visible==True:
            my_screen.blit(botbar.myskills.image, (botbar.myskills.x, botbar.inventory.y))
        if botbar.mytroops.visible==True:
            my_screen.blit(botbar.mytroops.image, (botbar.mytroops.x, botbar.inventory.y))
        if botbar.mygroups.visible==True:
            my_screen.blit(botbar.mygroups.image, (botbar.mygroups.x, botbar.inventory.y))
        if botbar.inventory.visible==True:
            my_screen.blit(botbar.inventory.image, (botbar.inventory.x, botbar.inventory.y))
        if botbar.weapon_skills.visible==True:
            my_screen.blit(botbar.weapon_skills.image, (botbar.weapon_skills.x, botbar.inventory.y))
        if botbar.buildings.visible==True:
            my_screen.blit(botbar.buildings.image, (botbar.buildings.x, botbar.inventory.y))
        if botbar.unknown.visible==True:
            my_screen.blit(botbar.unknown.image, (botbar.unknown.x, botbar.inventory.y))
            
        if dragging!=False:
            my_screen.blit(dragging.holding.image, pygame.mouse.get_pos())
    

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


def ask_player():
    """Temporary function, will be replaced by main menu function"""
    # This will later be a menu in the game my_screen:
    try:
        tempchoice=int(input("Choose your player type.\n1 Tyranid\n2 Space Marine\n\n"))
    except ValueError:
        print("\n\nERROR: Not an option.")
        print("Please enter the number of your choice.")
        return ask_player()
    if tempchoice==1:
        return "tyranid"
    elif tempchoice==2:
        return "spacemarine"
    else:
        print("\n\nERROR: Not an option.")
        print("Please enter the number of your choice.")
        return ask_player()

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
    send_to_host(["new_location", level, current_location])
    background= pygame.image.load('sprites/space/background'+str(level.space_type)+'.png')
    gamew, gameh = background.get_size()
    
    

def load_planet(level):
    global background, gamew, gameh, current_location
    send_to_host(["new_location", level, current_location])
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
    try:
        if me.character=='spacemarine':
            load='sprites/'+who
            me.standing_left = pygame.image.load(load+'/left.png')
            me.standing_right= pygame.image.load(load+'/right.png')
            me.walking_leftA= pygame.image.load(load+'/left_runningA.png')
            me.walking_leftB= pygame.image.load(load+'/left_runningB.png')
            me.walking_leftC= pygame.image.load(load+'/left_runningC.png')
            me.walking_rightA= pygame.image.load(load+'/right_runningA.png')
            me.walking_rightB= pygame.image.load(load+'/right_runningB.png')
            me.walking_rightC= pygame.image.load(load+'/right_runningC.png')
            me.lookup_left= pygame.image.load(load+'/left_lookup.png')
            me.lookup_right= pygame.image.load(load+'/right_lookup.png')
            me.lookdown_left= pygame.image.load(load+'/left_lookdown.png')
            me.lookdown_right= pygame.image.load(load+'/right_lookdown.png')
            # add these functions:
            #me.jump_leftA=pygame.image.load(load+'/jump_leftA.png')
            #me.jump_leftB=pygame.image.load(load+'/jump_leftB.png')   # troy is the only one with 3 jump animations
            #me.jump_rightA=pygame.image.load(load+'/jump_rightA.png') # everybody else only has 1
            #me.jump_rightB=pygame.image.load(load+'/jump_rightB.png')
            # separate this next part somehow, too many pictures being loaded for each character
            # maybe have a function addpic(who, pic)?
            # That would work well for characters with different numbers of pics
            # like troy and his 3 jumping pictures
            me.standing_up=pygame.image.load(load+'/standing_up.png')
            me.standing_down=pygame.image.load(load+'/standing_down.png')
            me.walking_upA=pygame.image.load(load+'/walking_upA.png')
            me.walking_upB=pygame.image.load(load+'/walking_upB.png')
            me.walking_downA=pygame.image.load(load+'/walking_downA.png')
            me.walking_downB=pygame.image.load(load+'/walking_downB.png')
            me.image = me.standing_left
            me.rect = pygame.Rect(me.image.get_rect())
            me.rect.move_ip(me.x, me.y)
        elif me.character=="tyranid":
            load='sprites/'+who
            me.standing_left = pygame.image.load(load+'/left.png')
            me.standing_right= pygame.image.load(load+'/right.png')
            me.walking_leftA= pygame.image.load(load+'/left_runningA.png')
            me.walking_leftB= pygame.image.load(load+'/left_runningB.png')
            me.walking_leftC= pygame.image.load(load+'/left_runningC.png')
            me.walking_rightA= pygame.image.load(load+'/right_runningA.png')
            me.walking_rightB= pygame.image.load(load+'/right_runningB.png')
            me.walking_rightC= pygame.image.load(load+'/right_runningC.png')
            me.lookup_left= pygame.image.load(load+'/left_lookup.png')
            me.lookup_right= pygame.image.load(load+'/right_lookup.png')
            me.lookdown_left= pygame.image.load(load+'/left_lookdown.png')
            me.lookdown_right= pygame.image.load(load+'/right_lookdown.png')
            # add these functions:
            #me.jump_leftA=pygame.image.load(load+'/jump_leftA.png')
            #me.jump_leftB=pygame.image.load(load+'/jump_leftB.png')   # troy is the only one with 3 jump animations
            #me.jump_rightA=pygame.image.load(load+'/jump_rightA.png') # everybody else only has 1
            #me.jump_rightB=pygame.image.load(load+'/jump_rightB.png')
            # separate this next part somehow, too many pictures being loaded for each character
            # maybe have a function addpic(who, pic)?
            # That would work well for characters with different numbers of pics
            # like troy and his 3 jumping pictures
            me.standing_up=pygame.image.load(load+'/standing_up.png')
            me.standing_down=pygame.image.load(load+'/standing_down.png')
            me.image = me.standing_left
            me.rect = pygame.Rect(me.image.get_rect())
            me.rect.move_ip(me.x, me.y)
    except pygame.error:
        print("Sorry, I can't do that.")

def jump_here():
    """If the player "jumps" to a spot offscreen,
    move everything else in the opposite direction
    to create the illusion of moving the screen to follow the player.
    """
    global current_location, user
    if user.x<100:
        difference=100-user.x
        user.x=100
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        current_location.gamex+= difference
        for guy in user.myarmy.sprites():
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
    elif user.x>600:
        difference=user.x-600
        user.x=600
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        current_location.gamex-= difference
        for guy in user.myarmy.sprites():
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
    if user.y<50:
        difference=50-user.y
        user.y=50
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        current_location.gamey+= difference
        for guy in user.myarmy.sprites():
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
    elif user.y>450:
        difference=user.y-450
        user.y=450
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        current_location.gamey-= difference
        for guy in user.myarmy.sprites():
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
        for players in main_players:
            players.y += 5
            players.rect=user.rect.move(0,5)
            for guy in players.myarmy.sprites():
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
        for players in main_players:
            players.y -= 5
            players.rect=players.rect.move(0,-5)
            for guy in players.myarmy.sprites():
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
        for players in main_players:
            players.x -= 5
            players.rect=players.rect.move(-5,0)
            for guy in players.myarmy.sprites():
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
        for players in main_players:
            players.x += 5
            players.rect=players.rect.move(5,0)
            for guy in players.myarmy.sprites():
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
    top=user.rect.top
    bottom=user.rect.bottom
    left=user.rect.left
    right=user.rect.right
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
    for guy in user.myarmy.sprites():
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
    global current_location
    for playyer in main_players:
        for guy in playyer.myarmy.sprites():
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
    global current_location
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
                who.myarmy.biomatter = who.myarmy.biomatter+100
                print("Biomatter: "+str(who.myarmy.biomatter))
            else:
                if who.age=="adult":
                    mydad=who.groups()[0]
                    mydad.biomatter = mydad.biomatter+100
                    print("Biomatter: "+str(mydad.biomatter))
                else:
                    who.age=who.age+1
            
            del peep
        #else:
        #   print("You can't eat something that's not dead yet.")


# def spawn_npcs(number, kind):
#     """This spawns a given number of
#     characters and returns them in a list.
#     """
#     spawning=[]
#     for i in range(number):
#         #replace with pygame group function
#         spawning.append(Player(kind))
#     return spawning
        

def end_game():
    global done, online
    """This stops the game loop and quits pygame."""
    if online==True:
        send_to_host('close_me')
        socksend.close()
        sockrec.close()
    online=False
    done = True
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
                
def remove_player_sprites(plyr):
    global current_location
    for guy in current_location.online_players:
        if guy.serverparent==plyr:
            current_location.online_players.remove(guy)
    for guy in current_location.online_troops:
        if guy.serverparent==plyr:
            current_location.online_troops.remove(guy)

def remove_online_sprites():
    global current_location #online_npcs, online_players, online_troops
    current_location.online_npcs.empty()
    current_location.online_players.empty()
    current_location.online_troops.empty()

#def client(ip, port, message):
#    #delete?
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
#        sck.connect((ip, port))
#        sck.sendall(bytes(message, 'ascii'))
#        response = str(sock.recv(1024), 'ascii')
#        print("Received: {}".format(response))

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
    #print(length)
    sck.send(data)
    message=recvall(sck, length)
    while message!=data:
        empty_socket(sck)
        #print(message)
        #print(data)
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
    #print(length)
    message=recvall(sck, length)
    sck.send(message)
    got_it=recvall(sck, 4)
    while struct.unpack('!I', got_it)[0] !=1:
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
    #sock.recv(16000)
    pass

def send_to_host(what):
    global online, host, port
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
        global socksend, sockrec, port, host, online, parent, current_location
        global npc, main_players
        socksend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockrec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sethost()
        socksend.connect((host, port))
        print(recv_one_message(socksend).decode('utf-8'))
        send_one_message(socksend, "send".encode('utf-8'))
        parent=recv_one_message(socksend).decode('utf-8')
        for guy in main_players:
            guy.serverparent=parent
            for troop in guy.myarmy:
                print("working")
                troop.serverparent=parent
        for guy in current_location.npc:
            guy.serverparent=parent
        sockrec.connect((host, port))
        print(recv_one_message(sockrec).decode('utf-8'))
        send_one_message(sockrec,"recv".encode('utf-8'))
        send_one_message(sockrec,pickle.dumps((parent, current_location)))
        #print(sock.recv(16000).decode("utf-8"))
        #sock.send("connected".encode("utf-8"))
        #send_all_sprites()
        #sock.send(get_all_sprites)
        online=True
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

def check_host():
    """delete, not being used"""
    global socksend, sockrec, port, host
    try:
        send_to_host("get")
        #sock.send("get".encode("utf-8"))
        #print(sock.recv(16000).decode("utf-8"))
        #eventlist=translate(sock.recv(8000).decode("utf-8"))
        return True
    except ConnectionRefusedError:
        print("Connection Refused")
        return False

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
##        for guy in npc:
##            send_to_host(["just_one",fromaddr,['spawnstatue',guy,guy.x-gamex,guy.y-current_location.gamey]])
##        for dude in main_player:
##            for guy in dude.myarmy:
##                send_to_host(["just_one",fromaddr,['spawnsoldier',guy,guy.x-gamex,guy.y-current_location.gamey]])
##        for guy in main_player:
##            send_to_host(["just_one",fromaddr,['spawnplayer',guy,guy.x-gamex,guy.y-current_location.gamey]])
##            print("hello")
                
    if message[0]=='delete_player':
        if current_location.space_type=='none':  # this means planet
            for guy in current_location.online_players:
                if guy.serverparent==message[1]:
                    current_location.online_players.remove(guy)
            for guy in current_location.online_troops:
                if guy.serverparent==message[1]:
                    current_location.online_troops.remove(guy)
            for guy in current_location.parent.online_players:
                if guy.serverparent==message[1]:
                    current_location.parent.online_players.remove(guy)
            for guy in current_location.parent.online_troops:
                if guy.serverparent==message[1]:
                    current_location.parent.online_troops.remove(guy)
        else:  # this means space
            for guy in current_location.online_players:
                if guy.serverparent==message[1]:
                    current_location.online_players.remove(guy)
            for guy in current_location.online_troops:
                if guy.serverparent==message[1]:
                    current_location.online_troops.remove(guy)
            for location in current_location.planets:
                for guy in location.online_players:
                    if guy.serverparent==message[1]:
                        current_location.online_players.remove(guy)
                for guy in location.online_troops:
                    if guy.serverparent==message[1]:
                        current_location.online_troops.remove(guy)
    
    if message[0]=="get_all_sprites":
        reply_to=message[1]
        print(reply_to)
        for guy in current_location.npc:
            #send_to_host("just_one".encode("utf-8"))
            #send_one_message(sockrec, pickle.dumps(reply_to))
            #send_to_host(['spawnstatue',guy,guy.x-gamex,guy.y-current_location.gamey])
            send_to_host(["just_one",reply_to,['spawnstatue',guy,guy.x-current_location.gamex,guy.y-current_location.gamey]])
        for dude in main_players:
            for guy in dude.myarmy:
                #send_to_host("just_one".encode("utf-8"))
                #send_one_message(sockrec, pickle.dumps(reply_to))
                send_to_host(["just_one",reply_to,['spawnsoldier',guy,guy.x-current_location.gamex,guy.y-current_location.gamey]])
        for guy in main_players:
            #send_to_host("just_one".encode("utf-8"))
            #send_one_message(sockrec, pickle.dumps(reply_to))
            #send_to_host(['spawnplayer',guy,guy.x-current_location.gamex,guy.y-current_location.gamey])
            send_to_host(["just_one",reply_to,['spawnplayer',guy,guy.x-current_location.gamex,guy.y-current_location.gamey]])
        print("sent everything")
        
    if message[0] == 'spawnsoldier':
        if message[1].character == "tyranid":
            if message[1].age=='adult':
                change_character(message[1], 'tyranid/adult')
                #message[1].
            else:
                change_character(message[1], 'tyranid/kid')
        elif message[1].character=="spacemarine":
            if message[1].age=='adult':
                change_character(message[1], 'spacemarine/adult')
            else:
                change_character(message[1], 'spacemarine/troop')
        message[1].x=message[2]+current_location.gamex
        message[1].y=message[3]+current_location.gamey
        message[1].set_rect()
        #message[1].rect.move_ip(message[1].x,message[1].y)
        
        current_location.online_troops.add(message[1])
    elif message[0]=='spawnplayer':
        if message[1].character == "tyranid":
            change_character(message[1], 'tyranid/player')
        elif message[1].character=="spacemarine":
            change_character(message[1], 'spacemarine/player')
        message[1].x=message[2]+current_location.gamex
        message[1].y=message[3]+current_location.gamey
        message[1].set_rect()
        #message[1].rect.move_ip(message[1].x,message[1].y)
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
        #message[1].rect.move_ip((message[1].x,message[1].y))
        current_location.online_npcs.add(message[1])
    elif message[0]=='movenpc':
        for thing in current_location.online_npcs:
            if thing.onlineID==message[1]:
                thing.x=message[2]+current_location.gamex
                thing.y=message[3]+current_location.gamey
                thing.set_rect()
                #thing.rect.move_ip(thing.x,thing.y)
    elif message[0]=='moveright':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="right"
                    guy.facing="right"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
    elif message[0]=='moveleft':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
    elif message[0]=='movedown':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
    elif message[0]=='moveup':
        if message[1]=='Player':
            for guy in current_location.online_players:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in current_location.online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    #guy.move_me()
                    guy.x =message[3]+current_location.gamex
                    guy.y=message[4]+current_location.gamey
                    #guy.rect.move_ip(guy.x,guy.y)
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
    global ppushed, pppushed
    global newwguy, socksend, sockrec, host, port
    global current_location
    global gamesize, playerkind, main_players
    global fullwidth, fullheight
    global my_screen, fullscrn
    global dragging
    
    dragging=False
        
    # later this will call the main menu
    playerkind=ask_player()
    
    
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
    user=Player( playerkind, parent, name="Player")
    #user=MainPlayer( playerkind, parent, name="Player")
    main_players.append(user)
    
    
    global botbar
    
    #uiunitx, uiunity = gamesize[0]//36, (gamesize[1]*4)//8.5
    
    botbar=UI_bar('player')
    
    botbar.myhotkeys[0].contains=Icon_square('pistol')
    botbar.myhotkeys[1].contains=Icon_square('club')
    
    
    # this makes a text box:
    #txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='type here: ')
    
    
    #temporary:
    #[[
    
    #t=open('Soundtrack/GreendaleIsWhereIBelong.wav')
    #print(t.getframerate())
    #pygame.mixer.init(44200)
    
    #pygame.mixer.music.load('Soundtrack/Greendale.wav')
    
    #pygame.mixer.music.load('Soundtrack/ChristmasRap.wav')
    #pygame.mixer.music.play(3)
    
    
    # move this to a tyranid specific function:
    user.myarmy.biomatter=400
    print("biomatter:"+str(user.myarmy.biomatter))
    
    
    # not used yet, might be used for in game menu
    #words_box="none"
    #using_menu=False
    
    #]]
    
    

    # ------------------- Main Program Loop --------------------
    
    # Loop until the user clicks the close button.
    done = False
    
    while not done:
    
        # --- EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        # TODO: turn into get controls function?

        if current_location.space_type=="none":
            planet_inputs()
        else:
            space_inputs()
        
    
    
        # --- EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
    
    
    
    
    
    
    
        # --- GAME LOGIC SHOULD GO BELOW THIS COMMENT
    
        
    
    
    
        
    
    
            
        
    
        # --- GAME LOGIC SHOULD GO ABOVE THIS COMMENT
    
    
    
    
    
    
        # --- DRAWING CODE SHOULD GO BELOW THIS COMMENT
    
    
        
        # First, clear the my_screen to grey. Don't put other drawing commands
        # above this, or they will be erased with this command.
    
    
        my_screen.fill((175, 175, 175)) # GREY
    
        fill_background(my_screen)
    
        #if online==True:
        #    if online2==True:
        #        check_host()
        #        online2=False
    
        #print(current_location.gamey)
    
        # This checks if troops are doing damage as they run around
        swinging()
    
        if current_location.space_type=='none':   #this means it is a planet
            planet_display(my_screen)
        else:
            space_display(my_screen)
            
        
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
    
    #def main():
    #    """This spawns the player, npcs, 
    #    and runs the main loop for the game.
    #    """
    #    
    #    #mostly use functions
    #    
    #    #move new guys into this function
    #    #load_level(1, player_type)
    #    
    #    # make main player 
    #    player_kind = "not necro" #input("")
    #    main_player = Player(player_kind)
    #    
    #    #start with some npcs
    #    npc_list = spawn_npcs(10, "necro")
    #    
    #   _____MAIN LOOP_____
    #    running=True
    #    while running==True:
    #        #inputs
    #        
    #        #logic
    #        
    #        #display
    #        
    #        #clock tick
    #        
    #        #for now just shut down
    #        running = quit_game()
    #        
    #    #for now when done:
    #    print("goodbye")
    


if __name__=="__main__":
    main_game_loop()

