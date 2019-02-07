
# TODO:
#
# class player
#     variables:
#     type
#     items
#     level 
# class npc
# class other players (later)
# class walls/doors
#
# control army
#
# control guy
#
# get equipment 
#
# stats and levels 
#
# different player types
#
# different controls for types





# PyInstaller --onefile whammer.py
########## CODE: ##########
import math, os, pygame, sys, random, pickle, struct, threading, socket, socketserver#, eztext
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    """Each minion can receive commands from the user and give commands to other minions.
    All minions can level up, earn xp, and be killed.
    For now the variable user is also a minion with the name player.
    Later, add inventory for each minion.
    """
    
    def __init__(self, kind, name="none"):
        """When instance is created set the name and default stats.
        Make a function for default names if no name is entered.
        """
        pygame.sprite.Sprite.__init__(self)
        self.onlineID=id(self)
        self.myarmy=pygame.sprite.Group()
        self.myarmy.biomatter=0
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
        self.character=kind
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
        global gamex, gamey
        if self.name=="Player":
            send_to_host(["spawnplayer", self, self.x-gamex, self.y-gamey])
        else:
            send_to_host(["spawnsoldier", self, self.x-gamex, self.y-gamey])


    def re_initiate(self):
        pygame.sprite.Sprite.__init__(self)
        
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
        
    def take_damage(self, damage):
        """Removes health from this minion."""
        self.health=self.health-(damage*self.armor())
        print(self.name, self.health)
        if self.health <=0:
            self.alive=False
            print("{} has died!".format(self.name))
            user.myarmy.remove(guy)
            #^^^^^replace with dead pic
        return self.alive

    def add_to_inventory(self,add, number=1):
        """This adds items to the inventory"""
        self.inventory.append([add, number])

    def equip(self, item, where):
        """This is equips an item to one part of the body, by using a dictionary"""
        for i in self.inventory:
            if i == item:
                try:
                    self.armor=item
                    change_character(self,self.character)
                    self.equipped[where]=item
                    if where=='body':
                        change_character(self,self.character)
                except pygame.error:
                    print("Sorry, I don't know what that is.")
                    

    def unequip(self, where):
        """This sets the given part of the minion to blank"""
        if where in self.equipped.keys():
            self.equipped[where]=""

    def receive_order(self, orders):
        """ This makes a list of tasks recieved,
        does the first task,
        then deletes it from the list.
        This is not yet in use, but will be needed when tasks take time to complete
        """
        print("work in progress...")
        self.tasks.append(orders)
        while self.tasks != {}:
            do_orders(self.tasks[0])
            del self.tasks[0]
            

    def do_orders(self, order):
        """This takes an order and converts it into a task."""
    
        if type(order)==list: # if the order is a list, read the first element to find the order
            
            if order[0] == "attack": # if the order is attack then the rest of the list is who to attack.
                for i in order[1]:
                    for it in npc.sprites(): # checks potential enemies first. replace with findwhat.
                        if it.name==i:
                            attack(it, self)
                    for it in user.myarmy.sprites(): # also checks myarmy for matching name. replace with findguy.
                        if it.name==i:
                            attack(it, self)

            elif order[0] == "kill":
                for i in order[1]:
                    for it in npc.sprites(): # checks potential enemies first. replace with findwhat.
                        if it.name==i:
                            attacktilldead(it, self)
                    for it in user.myarmy.sprites(): # also checks myarmy for matching name. replace with findguy.
                        if it.name==i:
                            attacktilldead(it, self)

            elif order[0]=="repair": # works just like attack. this also works to heal minions.
                for i in order[1]:
                    for it in user.myarmy.sprites(): # first checks myarmy for matching name. replace with findguy.
                        if it.name==i:
                            repair(it, self)
                    for it in npc.sprites():    # checks potential enemies next. replace with findwhat.
                        if it.name==i:
                            repair(it, self)
                    
            elif order[0]=="tell":  # this splits what's left of "order" into a list of who and what 
                self.give_orders(order[1],order[2])  # passes the order list to the give_order function

            elif order[0]=="craft": # this splits what's left of "order" into a list of what to craft
                if type(order[1])==list:
                    for i in order[1]:
                        self.inventory.append(i) # for now build just adds a string to the self.inventory list
                else:
                    self.inventory.append(order[1])

            elif order[0]=="equip":
                self.equip(order[1], order[2])

            elif order[0]=="unequip":
                self.unequip(order[1])


        elif order=="name": # this just says their name. good for getting a list of myarmy.
            if self.alive==True:
                print("Hello, my name is {}.".format(self.name))
            else:
                print("{} is dead.".format(self.name))
                
        elif order=="stats": # this prints all existing stats for this minion.
            print("\nMy name is {}".format(self.name))
            print("My health is {}".format(self.health))
            print("My level is {}".format(self.level))
            print("My xp is {}".format(self.xp))
            print("I have {} in my inventory.".format(self.inventory))
            print("Equipped: {}".format(self.equipped))


        #comming soon:
        #if order == "craft": 
        #if order == "build":
        #if order == "wait":


    def give_orders(self, who, what):
        """This takes a list of minions and a list of tasks and passes each task to each minion."""
        for guy in who:
            for it in user.myarmy.sprites(): #replace with findguy function
                if it.name==guy:
                    for stuff in what:
                        it.do_orders(stuff)

    def move_me(self):
        global gamex, gamey
        self.mytick+=1
        if self==user:
            if toprect.colliderect(user.rect) and user.direction=="up":
                antimove('up')
            if bottomrect.colliderect(user.rect) and user.direction=="down":
                antimove('down')
            if left_rect.colliderect(user.rect) and user.direction=="left":
                antimove('left')
            if right_rect.colliderect(user.rect) and user.direction=="right":
                antimove('right')
        if self.direction == 'right':
            send_to_host(["moveright",self.name,self.onlineID, self.x-gamex, self.y-gamey])
            self.facing="right"
            self.x += 5
            self.rect=self.rect.move(5,0)
            if self.mytick<=2:
                self.image=self.walking_rightA
            elif self.mytick<=4:
                self.image=self.walking_rightB
            elif self.mytick<=6:
                self.image=self.walking_rightC
            else:
                self.mytick=0
        elif self.direction == 'down':
            send_to_host(["movedown",self.name,self.onlineID, self.x-gamex, self.y-gamey])
            #this is for the 3d setting:
            if self.character!="tyranid":
                self.facing='down'
                if self.mytick<=3:
                    self.image=self.walking_downA
                elif self.mytick<=6:
                    self.image=self.walking_downB
                else:
                    self.mytick=0
            self.y += 5
            self.rect=self.rect.move(0,5)
            #this is for the 2d setting:
            #if user.facing == 'left':
            #    user.image=user.lookdown_left
            #if user.facing == 'right':
            #    user.image=user.lookdown_right
        elif self.direction == 'left':
            send_to_host(["moveleft",self.name,self.onlineID, self.x-gamex, self.y-gamey])
            self.facing="left"
            self.x -= 5
            self.rect=self.rect.move(-5,0)
            if self.mytick<=2:
                self.image=self.walking_leftA
            elif self.mytick<=4:
                self.image=self.walking_leftB
            elif self.mytick<=6:
                self.image=self.walking_leftC
            else:
                self.mytick=0
        elif self.direction == 'up':
            send_to_host(["moveup",self.name,self.onlineID, self.x-gamex, self.y-gamey])
            #this is for the 3d setting:
            if self.character!="tyranid":
                self.facing='up'
                if self.mytick<=3:
                    self.image=self.walking_upA
                elif self.mytick<=6:
                    self.image=self.walking_upB
                else:
                    self.mytick=0
            self.y -= 5
            self.rect=self.rect.move(0,-5)
            #this is for the 2d setting:
            #if user.facing == 'left':
            #    user.image=user.lookup_left
            #if user.facing == 'right':
            #    user.image=user.lookup_right
        elif self.direction=="none":
            #if user.jump==True
            if self.facing=="right":
                self.image=self.standing_right
            elif self.facing=="left":
                self.image=self.standing_left
            elif self.facing=="down":
                self.image=self.standing_down
            elif self.facing=="up":
                self.image=self.standing_up
        elif self.direction=="follow":
            if self.x<self.following.x-30:
                send_to_host(["moveright",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.facing="right"
                self.x += 5
                self.rect=self.rect.move(5,0)
                if self.mytick<=2:
                    self.image=self.walking_rightA
                elif self.mytick<=4:
                    self.image=self.walking_rightB
                elif self.mytick<=6:
                    self.image=self.walking_rightC
                else:
                    self.mytick=0
            elif self.x>self.following.x+30:
                send_to_host(["moveleft",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.facing="left"
                self.x -= 5
                self.rect=self.rect.move(-5,0)
                if self.mytick<=2:
                    self.image=self.walking_leftA
                elif self.mytick<=4:
                    self.image=self.walking_leftB
                elif self.mytick<=6:
                    self.image=self.walking_leftC
                else:
                    self.mytick=0
            elif self.y<self.following.y-30:
                send_to_host(["movedown",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.y += 5
                self.rect=self.rect.move(0,5)
                if self.character!='tyranid':
                    self.facing="down"
                    if self.mytick<=3:
                        self.image=self.walking_downA
                    elif self.mytick<=6:
                        self.image=self.walking_downB
                    else:
                        self.mytick=0
            elif self.y>self.following.y+30:
                send_to_host(["moveup",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.y -= 5
                self.rect=self.rect.move(0,-5)
                if self.character!='tyranid':
                    self.facing="up"
                    if self.mytick<=3:
                        self.image=self.walking_upA
                    elif self.mytick<=6:
                        self.image=self.walking_upB
                    else:
                        self.mytick=0
            else:
                if self.facing=="right":
                    self.image=self.standing_right
                elif self.facing=="left":
                    self.image=self.standing_left
                elif self.facing=="down":
                    self.image=self.standing_down
                elif self.facing=="up":
                    self.image=self.standing_up
        elif self.direction=="here":
            if self.x<self.go_here[0]-5-(self.rect.height/2):
                send_to_host(["moveright",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.x += 5
                self.rect=self.rect.move(5,0)
                self.facing="right"
                if self.mytick<=2:
                    self.image=self.walking_rightA
                elif self.mytick<=4:
                    self.image=self.walking_rightB
                elif self.mytick<=6:
                    self.image=self.walking_rightC
                else:
                    self.mytick=0
            elif self.x>self.go_here[0]+5-(self.rect.height/2):
                send_to_host(["moveleft",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.facing="left"
                self.x -= 5
                self.rect=self.rect.move(-5,0)
                if self.mytick<=2:
                    self.image=self.walking_leftA
                elif self.mytick<=4:
                    self.image=self.walking_leftB
                elif self.mytick<=6:
                    self.image=self.walking_leftC
                else:
                    self.mytick=0
            elif self.y<self.go_here[1]-5-(self.rect.height/2):
                send_to_host(["movedown",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.y += 5
                self.rect=self.rect.move(0,5)
                if self.character!='tyranid':
                    self.facing="down"
                    if self.mytick<=3:
                        self.image=self.walking_downA
                    elif self.mytick<=6:
                        self.image=self.walking_downB
                    else:
                        self.mytick=0
            elif self.y>self.go_here[1]+5-(self.rect.height/2):
                send_to_host(["moveup",self.name,self.onlineID, self.x-gamex, self.y-gamey])
                self.y -= 5
                self.rect=self.rect.move(0,-5)
                if self.character!='tyranid':
                    self.facing="up"
                    if self.mytick<=3:
                        self.image=self.walking_upA
                    elif self.mytick<=6:
                        self.image=self.walking_upB
                    else:
                        self.mytick=0
            else:
                self.direction="none"
                    
        



    
        

class Statue(pygame.sprite.Sprite):
    """A statue cannot attack, but can be destroyed."""
    
    def __init__(self, name):
        """When created, set name and default stats."""
        pygame.sprite.Sprite.__init__(self)
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
        global gamex, gamey
        send_to_host(["spawnstatue", self, self.x-gamex,self.y-gamey])

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

class checkinghostThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global online, socksend, sockrec, gamex, gamey
        for guy in npc:
            send_to_host(['spawnstatue',guy,guy.x-gamex,guy.y-gamey])
        for dude in main_player:
            for guy in dude.myarmy:
                send_to_host(['spawnsoldier',guy,guy.x-gamex,guy.y-gamey])
        for guy in main_player:
            send_to_host(['spawnplayer',guy,guy.x-gamex,guy.y-gamey])
        send_to_host('get_all_sprites')
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
                print(message)
            except OverflowError:
                print("Too much data")



                
       

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

def remove_online_sprites():
    global online_npcs, online_players, online_troops
    online_npcs.empty()
    online_players.empty()
    online_troops.empty()

def client(ip, port, message):
    #delete?
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
        sck.connect((ip, port))
        sck.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

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
    sck.send(lengthbuf)
    got_it=recvall(sck, 4)
    while struct.unpack('!I', got_it)[0] ==0:
        empty_socket(sck)
        lengthbuf = recvall(sck, 4)
        sck.send(lengthbuf)
        got_it=sck.recv(4)
    length, = struct.unpack('!I', lengthbuf)
    #print(length)
    message=recvall(sck, length)
    reply=sck.send(message)
    got_it=recvall(sck, 4)
    while struct.unpack('!I', got_it)[0] ==0:
        empty_socket(sck)
        message=recvall(sck, length)
        reply=sck.send(message)
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
    global host
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
        global socksend, sockrec, port, host, online
        sethost()
        socksend.connect((host, port))
        print(recv_one_message(socksend).decode('utf-8'))
        send_one_message(socksend, "send".encode('utf-8'))
        parent=recv_one_message(socksend).decode('utf-8')
        sockrec.connect((host, port))
        print(recv_one_message(sockrec).decode('utf-8'))
        send_one_message(sockrec,"recv".encode('utf-8'))
        send_one_message(sockrec,parent.encode('utf-8'))
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

def send_all_sprites():
    pass
    #delete?

def check_host():
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
    global npc, gamex, gamey
    if type(message)==str:
        print(message)
        #^^^^delete?
    if message[0]=="get_all_sprites":
        reply_to=message[1]
        print(reply_to)
        for guy in npc:
            #send_to_host("just_one".encode("utf-8"))
            #send_one_message(sockrec, pickle.dumps(reply_to))
            #send_to_host(['spawnstatue',guy,guy.x-gamex,guy.y-gamey])
            send_to_host(["just_one",reply_to,['spawnstatue',guy,guy.x-gamex,guy.y-gamey]])
        for dude in main_player:
            for guy in dude.myarmy:
                #send_to_host("just_one".encode("utf-8"))
                #send_one_message(sockrec, pickle.dumps(reply_to))
                send_to_host(["just_one",reply_to,['spawnsoldier',guy,guy.x-gamex,guy.y-gamey]])
        for guy in main_player:
            #send_to_host("just_one".encode("utf-8"))
            #send_one_message(sockrec, pickle.dumps(reply_to))
            #send_to_host(['spawnplayer',guy,guy.x-gamex,guy.y-gamey])
            send_to_host(["just_one",reply_to,['spawnplayer',guy,guy.x-gamex,guy.y-gamey]])

        print("sent everything")
    elif message[0] == 'spawnsoldier':
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
        message[1].x=message[2]+gamex
        message[1].y=message[3]+gamey
        message[1].set_rect()
        #message[1].rect.move_ip(message[1].x,message[1].y)
        
        online_troops.add(message[1])
    elif message[0]=='spawnplayer':
        if message[1].character == "tyranid":
            change_character(message[1], 'tyranid/player')
        elif message[1].character=="spacemarine":
            change_character(message[1], 'spacemarine/player')
        message[1].x=message[2]+gamex
        message[1].y=message[3]+gamey
        message[1].set_rect()
        #message[1].rect.move_ip(message[1].x,message[1].y)
        online_players.add(message[1])
    elif message[0]=='attack':
        for guy in online_npcs:
            if guy.onlineID==message[1]:
                guy.take_damage(message[3])
        for guy in npc:
            if guy.onlineID==message[1]:
                guy.health=0
                guy.alive=False
    elif message[0]=='killnpc':
        for guy in online_npcs:
            if guy.onlineID==message[1]:
                guy.take_damage(10000)
        for guy in npc:
            if guy.onlineID==message[1]:
                guy.take_damage(10000)
    elif message[0]=='deletenpc':
        for guy in online_npcs:
            if guy.onlineID==message[1]:
                online_npcs.remove(guy)
        for guy in npc:
            if guy.onlineID==message[1]:
                npc.remove(guy)
    elif message[0]=='spawnstatue':
        message[1].set_image()
        message[1].x=message[2]+gamex
        message[1].y=message[3]+gamey
        message[1].set_rect()
        #message[1].rect.move_ip((message[1].x,message[1].y))
        online_npcs.add(message[1])
    elif message[0]=='movenpc':
        for thing in online_npcs:
            if thing.onlineID==message[1]:
                thing.x=message[2]+gamex
                thing.y=message[3]+gamey
                thing.set_rect()
                #thing.rect.move_ip(thing.x,thing.y)
    elif message[0]=='moveright':
        if message[1]=='Player':
            for guy in online_players:
                if guy.onlineID==message[2]:
                    guy.direction="right"
                    guy.facing="right"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
    elif message[0]=='moveleft':
        if message[1]=='Player':
            for guy in online_players:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="left"
                    guy.facing="left"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
    elif message[0]=='movedown':
        if message[1]=='Player':
            for guy in online_players:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="down"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
    elif message[0]=='moveup':
        if message[1]=='Player':
            for guy in online_players:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        else:
            for guy in online_troops:
                if guy.onlineID==message[2]:
                    guy.direction="up"
                    #guy.move_me()
                    guy.x =message[3]+gamex
                    guy.y=message[4]+gamey
                    guy.set_rect()
                    #guy.rect.move_ip(guy.x,guy.y)
        
            
        
            
         #   newguy=words    #needs a proper id or name, then move searches for guy
         #also send group? npc, main_player, guy.myarmy
            

def loading_game():
    tempchoice=int(input("Choose your player type.\n1 Tyranid\n2 Space Marine\n\n"))
    if tempchoice==1:
        return "tyranid"
    elif tempchoice==2:
        return "spacemarine"
#    else:
 #       print("Please enter the number of your choice.")
  #      return loading_game()

def change_character(me, who):
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
    global gamex
    global gamey
    if user.x<100:
        difference=100-user.x
        user.x=100
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        gamex+= difference
        for guy in user.myarmy.sprites():
            guy.x += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]+difference,guy.go_here[1])
        for thing in npc.sprites():
            thing.x += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in online_troops:
            guy.x += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]+difference,guy.go_here[1])
        for thing in online_npcs:
            thing.x += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
    elif user.x>600:
        difference=user.x-600
        user.x=600
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        gamex-= difference
        for guy in user.myarmy.sprites():
            guy.x -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]-difference,guy.go_here[1])
        for thing in npc.sprites():
            thing.x -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in online_troops:
            guy.x -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0]-difference,guy.go_here[1])
        for thing in online_npcs:
            thing.x -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
    if user.y<50:
        difference=50-user.y
        user.y=50
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        gamey+= difference
        for guy in user.myarmy.sprites():
            guy.y += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]+difference)
        for thing in npc.sprites():
            thing.y += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in online_troops:
            guy.y += difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]+difference)
        for thing in online_npcs:
            thing.y += difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
    elif user.y>450:
        difference=user.y-450
        user.y=450
        user.rect=pygame.Rect(user.image.get_rect())
        user.rect.move_ip(user.x,user.y)
        gamey-= difference
        for guy in user.myarmy.sprites():
            guy.y -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]-difference)
        for thing in npc.sprites():
            thing.y -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        for guy in online_troops:
            guy.y -= difference
            guy.rect=pygame.Rect(guy.image.get_rect())
            guy.rect.move_ip(guy.x,guy.y)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]-difference)
        for thing in online_npcs:
            thing.y -= difference
            thing.rect=pygame.Rect(thing.image.get_rect())
            thing.rect.move_ip(thing.x,thing.y)
        

def spawnoffscreen(direction):
    if direction=="up":
        if (random.randint(1,25))==1:
            newguy=Statue("Statue")
            newguy.y=-50
            newguy.rect=pygame.Rect(newguy.image.get_rect())
            newguy.rect.move_ip(newguy.x,newguy.y)
            npc.add(newguy)
    elif direction=="down":
        if (random.randint(1,40))==1:
            newguy=Statue("Statue")
            newguy.y=550
            newguy.rect=pygame.Rect(newguy.image.get_rect())
            newguy.rect.move_ip(newguy.x,newguy.y)
            npc.add(newguy)
    if direction=="left":
        if (random.randint(1,1))==1:
            newguy=Statue("Statue")
            newguy.x=-50
            newguy.rect=pygame.Rect(newguy.image.get_rect())
            newguy.rect.move_ip(newguy.x,newguy.y)
            npc.add(newguy)
    elif direction=="right":
        if (random.randint(1,50))==1:
            newguy=Statue("Statue")
            newguy.x=750
            newguy.rect=pygame.Rect(newguy.image.get_rect())
            newguy.rect.move_ip(newguy.x,newguy.y)
            npc.add(newguy)
    try:
        global gamex, gamey
        send_to_host(["movenpc", newguy.onlineID, newguy.x-gamex,newguy.y-gamey])
    except UnboundLocalError:
        pass

def antimove(direction):
    global gamex
    global gamey
    spawnoffscreen(direction)
    if direction=="up":
        gamey+=5
        for players in main_player:
            players.y += 5
            players.rect=user.rect.move(0,5)
            for guy in players.myarmy.sprites():
                guy.y += 5
                guy.rect=guy.rect.move(0,5)
                if guy.go_here!="none":
                    guy.go_here=(guy.go_here[0],guy.go_here[1]+5)
        for thing in npc.sprites():
            thing.y += 5
            thing.rect=thing.rect.move(0,5)
        for players in online_players:
            players.y += 5
            players.rect=players.rect.move(0,5)
        for guy in online_troops.sprites():
            guy.y += 5
            guy.rect=guy.rect.move(0,5)
            if guy.go_here!="none":
                guy.go_here=(guy.go_here[0],guy.go_here[1]+5)
        for thing in online_npcs.sprites():
            thing.y += 5
            thing.rect=thing.rect.move(0,5)
    if direction=="down":
        gamey-=5
        for players in main_player:
            players.y -= 5
            players.rect=players.rect.move(0,-5)
            for guy in players.myarmy.sprites():
                guy.y -= 5
                guy.rect=guy.rect.move(0,-5)
                if guy.go_here!="none":
                    guy.go_here=(guy.go_here[0],guy.go_here[1]-5)
        for thing in npc.sprites():
            thing.y -= 5
            thing.rect=thing.rect.move(0,-5)
        for players in online_players:
            players.y -= 5
            players.rect=players.rect.move(0,-5)
        for guy in online_troops.sprites():
            guy.y -= 5
            guy.rect=guy.rect.move(0,-5)
        for thing in online_npcs.sprites():
            thing.y -= 5
            thing.rect=thing.rect.move(0,-5)
    if direction=="right":
        gamex-=5
        for players in main_player:
            players.x -= 5
            players.rect=players.rect.move(-5,0)
            for guy in players.myarmy.sprites():
                guy.x -= 5
                guy.rect=guy.rect.move(-5,0)
                if guy.go_here!="none":
                    guy.go_here=(guy.go_here[0]-5,(guy.go_here[1]))
        for thing in npc.sprites():
            thing.x -= 5
            thing.rect=thing.rect.move(-5,0)
        for players in online_players:
            players.x -= 5
            players.rect=players.rect.move(-5,0)
        for guy in online_troops.sprites():
            guy.x -= 5
            guy.rect=guy.rect.move(-5,0)
        for thing in online_npcs.sprites():
            thing.x -= 5
            thing.rect=thing.rect.move(-5,0)
    if direction=="left":
        gamex+=5
        for players in main_player:
            players.x += 5
            players.rect=players.rect.move(5,0)
            for guy in players.myarmy.sprites():
                guy.x += 5
                guy.rect=guy.rect.move(5,0)
                if guy.go_here!="none":
                    guy.go_here=(guy.go_here[0]+5,(guy.go_here[1]))
        for thing in npc.sprites():
            thing.x += 5
            thing.rect=thing.rect.move(5,0)
        for players in online_players:
            players.x += 5
            players.rect=players.rect.move(5,0)
        for guy in online_troops.sprites():
            guy.x += 5
            guy.rect=guy.rect.move(5,0)
        for thing in online_npcs.sprites():
            thing.x += 5
            thing.rect=thing.rect.move(5,0)
                        

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
    for thing in npc:
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
    for playyer in main_player:
        for guy in playyer.myarmy.sprites():
            if guy.attacking==True:
                for thing in npc:
                    if thing.alive==True:
                        if guy.rect.colliderect(thing.rect):
                            testing_reasons=thing.take_damage(25)
                            #if testing_reasons==False:
                             #   guy.attacking=False
                for thing in online_npcs:
                    if thing.alive==True:
                        if guy.rect.colliderect(thing.rect):
                            testing_reasons=thing.take_damage(25)
                            #if testing_reasons==False:
                             #   guy.attacking=False
            if guy.eating==True:
                eat(guy)

def fight(who):
    #peeps=pygame.sprite.spritecollideany(who, main_player, False)
    peeps=[]
    for guy in npc:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for guy in online_npcs:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for peep in peeps:
        peep.take_damage(25)
        send_to_host(['attack', peep.onlineID, 25])


def eat(who):
    peeps=[]
    for guy in npc:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for guy in online_npcs:
        if who.rect.colliderect(guy.rect)==True:
            peeps.append(guy)
    for peep in peeps:
        if peep.health<=0:
            send_to_host(["deletenpc", peep.onlineID])
            npc.remove(peep)
            online_npcs.remove(peep)
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


def spawn_npcs(number, kind):
    """This spawns a given number of
    characters and returns them in a list.
    """
    spawning=[]
    for i in range(number):
        #replace with pygame group function
        spawning.append(Player(kind))
    return spawning
        

def end_game():
    global done, online
    """This stops the game loop and quits pygame."""
    if online==True:
        send_to_host('close')
        socksend.close()
        sockrec.close()
    online=False
    done = True
    pygame.quit()
    os._exit(1)
    sys.exit("You quit the game, not me")

#-----------------------------------------------------
#*****************************************************
#-----------------------------------------------------
#____________________START GAME:______________________


# Initialize the game engine

pygame.init()

playerkind=loading_game()

online=False
online2=True

# Define the colors
# remember: http://www.colorpicker.com

BLACK = ( 0, 0, 0)

WHITE = ( 255, 255, 255)

GREEN = ( 0, 255, 0)

RED = ( 255, 0, 0)

BLUE = ( 0, 0, 255)

GREY = ( 175, 175, 175)


# Define the directions?
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


# Set the screen size and caption

size=(700,500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("WarHammer 40k")

background= pygame.image.load('sprites/Background/backgrounddetailed8.png')
gamex=0
gamey=0
gamew, gameh = background.get_size()


# Loop until the user clicks the close button.
done = False



# Used to manage how fast the screen updates

clock = pygame.time.Clock()


# global lists:



npc=pygame.sprite.Group()
online_npcs=pygame.sprite.Group()

online_troops=pygame.sprite.Group()

# for now, user is a minion object:

user=Player(kind=playerkind, name="Player")
main_player=pygame.sprite.Group()
main_player.add(user)
online_players=pygame.sprite.Group()

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


walls = [] # List to hold the walls

screensquares=[]
left_rect = pygame.Rect(0, 0, 30, 500)
screensquares.append(left_rect)
right_rect = pygame.Rect(670, 0, 30, 500)
screensquares.append(right_rect)
toprect = pygame.Rect(0, 0, 700, 30)
screensquares.append(toprect)
bottomrect = pygame.Rect(0, 470, 700, 30)
screensquares.append(bottomrect)

on_edge=False


myTick=0
keyTime=0

ppushed=0
pppushed=0

user.myarmy.biomatter=200
print("biomatter:"+str(user.myarmy.biomatter))



words_box="none"
using_menu=False

            

#]]


# ------------------- Main Program Loop --------------------

while not done:


    
    # --- EVENT PROCESSING SHOULD GO BELOW THIS COMMENT


    # events for txtbx

#this tells you the index number of the keys being pressed
#    thekeys=pygame.key.get_pressed()
 #   for indexed in thekeys:
  #      if indexed==True:
   #         print(thekeys.index(indexed))

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

    if len(main_player)>1:
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

    if len(main_player)>1:
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
                user.myarmy.add(Player(name="minion",kind=playerkind))
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
        if len(main_player)>1:
            if pppushed==0:
                if newwguy.myarmy.biomatter>=100:
                    newwguy.myarmy.biomatter=newwguy.myarmy.biomatter-100
                    newwguy.myarmy.add(Player(name="minion",kind=newwguy.character))
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
            #mykeys=pygame.key.get_pressed()
            
            if using_menu==True:
                if event.key == K_ESCAPE:
                    #delete(words_box.delete)
                    using_menu=False

                #else:
                    #words_box.image.fill(event.key)
                    
                
            else:
                if (event.key==K_a or
                    event.key==K_d or
                    event.key==K_s or
                    event.key==K_w or
                    event.key==K_UP or
                    event.key==K_DOWN or
                    event.key==K_LEFT or
                    event.key==K_RIGHT):
                    keyTime=myTick
#                if (mykeys[K_a]):
 #                   user.direction = LEFT
  #                  keyTime=myTick
   #             if (mykeys[K_d]):
    #                user.direction = RIGHT
     #               keyTime=myTick
      #          if (mykeys[K_w]):
       #             user.direction = UP
        #            keyTime=myTick
         #       if (mykeys[K_s]):
          #          user.crouch = True
           #         user.direction = DOWN
            #        keyTime=myTick

#                if (mykeys[K_LEFT]):
 #                   for thing in myarmy:
  #                      if thing.selected==True:
   #                         thing.direction = LEFT
    #                keyTime=myTick
     #           if (mykeys[K_RIGHT]):
      #              for thing in myarmy:
       #                 if thing.selected==True:
        #                    thing.direction = RIGHT
         #           keyTime=myTick
          #      if (mykeys[K_UP]):
           #         for thing in myarmy:
            #            if thing.selected==True:
             #               thing.direction = UP
              #      keyTime=myTick
               # if (mykeys[K_DOWN]):
                #    for thing in myarmy:
                 #       if thing.selected==True:
                  #          thing.direction = DOWN
                   # keyTime=myTick

                    
                

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
                    npc.add(Statue("Statue"))
                    
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
                    for thing in online_npcs:
                        if thing.alive==False:
                            eat_it.append(thing)
                    for thing in npc:
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
                    for thing in online_npcs:
                        if thing.alive==True:
                            kill_it.append(thing)
                    for thing in npc:
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
                        main_player.empty()
                        temp_num=random.randint(0,len(selected_troops)-1)
                        user=selected_troops[temp_num]
                        
                        main_player.add(user)

                        user.myarmy.remove(user)

                        user.controlling=True
                        user.selected=False
                        change_character(user,"tyranid/player")
                        jump_here()

                if event.key==K_LEFTBRACKET:
                    newwguy=Player(kind='tyranid',name="Player")
                    main_player.add(newwguy)
                    newwguy.myarmy.biomatter=100

                if event.key==K_RIGHTBRACKET:
                    newwguy=Player(kind='spacemarine',name="Player")
                    main_player.add(newwguy)
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
                    for thing in npc:
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
                    for thing in npc:
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

                if event.key==K_0:
                    print("You have "+str(len(user.myarmy.sprites()))+" troops.")

                if event.key==K_9:
                    print("There are "+str(len(npc.sprites()))+" enemies.")
                    
                if event.key==K_8:
                    print("Your screen location:\n"+
                          "X = "+str(-gamex)+
                          "\nY = "+str(-gamey))

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
                            send_to_host('close')
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

                    
                    

                #if event.key == K_RETURN:
                    #textin() 
                #if (mykeys[K_`]):
                    #ask_player()  # this is what gets the input from the player

                #if (mykeys[K_b]):
                    #words_box=eztext.Input(maxlength=45, color=(255,0,0), prompt='type here: ')
                        #boxx(30,50)
                    #using_menu=True
                    #words_box.typing()

            
                

#        elif event.type == KEYUP:     # if they release a button but are still holding another one down
 #           mykeys=pygame.key.get_pressed() 
  #          if ((mykeys[K_a])
   #              or(mykeys[K_d])
    #             or(mykeys[K_w])
     #            or(mykeys[K_s]))==False:
      #          user.direction = "none"
       #         user.jump = False
        #        user.crouch = False
         #   if ((mykeys[K_LEFT])
          #       or(mykeys[K_RIGHT])
           #      or(mykeys[K_UP])
            #     or(mykeys[K_DOWN]))==False:
             #   for guy in myarmy:
              #      if (guy.selected==True
               #         and guy.direction!="here"):
                #        guy.direction="none"
                
    
        

    #if e is pressed:
        #action=True
    #else:
        #action=False

    #if p is pressed:  #planning mode  (for commanding and building)
        #who=ask who, map or grid?
        #command(who)





    # --- EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT







    # --- GAME LOGIC SHOULD GO BELOW THIS COMMENT

    



    


        
    

    # --- GAME LOGIC SHOULD GO ABOVE THIS COMMENT






    # --- DRAWING CODE SHOULD GO BELOW THIS COMMENT


    
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.


    screen.fill(GREY) #


    if gamex>0:
        if gamey<=0:
            tempx=gamex
            while tempx<size[0]:
                tempx+=gamew
            for y in range(gamey,size[1],gameh):
                for x in range(tempx,-gamew,-gamew):
                    screen.blit(background,(x,y))
        elif gamey>0:
            tempx=gamex
            tempy=gamey
            while tempx<size[0]:
                tempx+=gamew
            while tempy<size[1]:
                tempy+=gameh
            for y in range(tempy,-gameh,-gameh):
                for x in range(tempx,-gamew,-gamew):
                    screen.blit(background,(x,y))
                    
    elif gamex<=0:
        if gamey<=0:
            for y in range(gamey,size[1],gameh):
                for x in range(gamex,size[0],gamew):
                    screen.blit(background,(x,y))
        elif gamey>0:
            tempy=gamey
            while tempy<size[1]:
                tempy+=gameh
            for y in range(tempy,-gameh,-gameh):
                for x in range(gamex,size[0],gamew):
                    screen.blit(background,(x,y))
    

    #if online==True:
     #   if online2==True:
      #      check_host()
       #     online2=False

    #print(gamey)

    swinging()

    for it in online_troops.sprites():
        try:
            screen.blit(it.image, (it.x, it.y))
            #pygame.draw.rect(screen,WHITE,it.rect)
        except pygame.error:
            print(it)
            
    for it in online_npcs.sprites():
        try:
            screen.blit(it.image, (it.x, it.y))
            #pygame.draw.rect(screen,WHITE,it.rect)
        except pygame.error:
            print(it)

    for players in online_players:
        screen.blit(players.image, (players.x, players.y))
        #pygame.draw.rect(screen,WHITE,players.rect)

    
    for playerss in main_player:
        for guy in playerss.myarmy.sprites():
            guy.move_me()
            if guy.age!="adult":
                if guy.age>=1:
                    guy.age="adult"
                    change_character(guy, guy.character+'/adult')
            screen.blit(guy.image, (guy.x, guy.y))
            #pygame.draw.rect(screen,WHITE,guy.rect)

    for it in npc.sprites():
        try:
            screen.blit(it.image, (it.x, it.y))
        except pygame.error:
            print(it)
        #pygame.draw.rect(screen,WHITE,it.rect)

    for players in main_player:
        players.move_me()
        screen.blit(players.image, (players.x, players.y))



#    screen.blit(background, (gamex, gamey))

    #pygame.draw.rect(screen,WHITE,user.rect)
    #pygame.draw.rect(screen,WHITE,toprect)
    #pygame.draw.rect(screen,WHITE,bottomrect)
    #pygame.draw.rect(screen,WHITE,left_rect)
    #pygame.draw.rect(screen,WHITE,right_rect)


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
#        words_box.draw(screen)
#        #screen.blit(words_box.image, words_box.position) # add self.contents or self.text

#    for wall in walls:
#        pygame.draw.rect(screen, (RED), wall)

    # --- update the screen 
        # blit txtbx on the sceen
    
    
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
    main()
