#!/usr/bin/python           # This is server.py file

import socket, time, threading, pickle, struct, socketserver, pygame

class Main_Player():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Character():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Tyranid():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Human():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Tau():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Chaos():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Eldar():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class DarkEldar():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Ork():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Statue():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Space():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Planet():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class Buildings():
    """
   This is only here as a fix to a bug.
   When pickle unloads a message to read the first element,
   it also wants to load any object.
   """
    pass

class PlayerClient():
    def __init__(self, address):
        self.address=address
        self.from_player=0#socksend
        self.to_player=0#sockrec
        self.player_to_players=[]
        self.location = 'none'# planet/space

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """not used, delete"""
    # Or should I replace socket stuff with tcp socket stuff?
    pass

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """not used, delete"""
    def handle(self):
        """copied and not used, delete"""
        self.data = recv_one_message(self)
        cur_thread = threading.current_thread()
        response = "{}".format(cur_thread.name)
        send_one_message(self, response)
##        self.request.sendall(response)

class adding_new_client (threading.Thread):
    """This is not used, delete"""
    def __init__(self, message,excpt='none'):
        threading.Thread.__init__(self)
    def run(self):
        pass

    #TODO: change excpt to sender
class event_to_allThread (threading.Thread):
    """"""
    def __init__(self, message,excpt='none', location='none'):
        """takes a message and one list from clientlist"""
        threading.Thread.__init__(self)
        self.excpt=excpt
        self.message=message
        self.location=location
    def run(self):
        if self.location=='none':
            for guy in self.excpt.player_to_players:#range(3,len(self.excpt)):
                send_one_message(guy[1], self.message)
                #send_one_message(self.excpt[guy][1], self.message)
        else:
            global clientlocations
            for guy in self.excpt.player_to_players:#range(3,len(self.excpt)):
                if clientlocations[guy[0]].name==self.location.name:
                #if clientlocations[self.excpt[guy][0]].name==self.location.name:
                    try:
                        send_one_message(guy[1], self.message)
                    except ConnectionResetError:
                        print('Connection was forcibly closed by the remote host')
                        

class host_to_allThread (threading.Thread):
    def __init__(self, message,excpt='none'):
        threading.Thread.__init__(self)
        self.excpt=excpt
        self.message=message
    def run(self):
        for guy in clientlist:
            if guy.address!=self.excpt.address:
                send_one_message(guy.to_player, self.message)
##            guy.send(self.message)
            

class newThread (threading.Thread):
    """This thread listens to the socket for creating all new sockets.

    This thread is the first to begin, and waits for a client to
    conntect. After connecting it starts a new thread to listen while
    it finishes setting up the socket and saving it to clientlist."""
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global clienteventlists, clientlist, serv  # get rid of global variables

        # Wait for client connection
        serv.listen(5)

        # Establish connection and save address.
        # 'c' is the new socket object.
        # addr is a tuple in the form (client_IP, client_port).
        c, addr = serv.accept()

        # Start a new listening thread.
        keeplistening=newThread()
        keeplistening.daemon=False
        keeplistening.start()

        # Confirm connection.
        print('Got connection from'+ str(addr))
        send_one_message(c, "Connected successfully".encode('utf-8'))
        who=recv_one_message(c)

        # If the message is a string, decode with utf-8
        # If the message is a list, string, or object decode with pickle
        try:
            who=who.decode('utf-8')
        except UnicodeDecodeError:
            who=pickle.loads(who)

        # The client will send a string "send" if it is the
        # socket dedicated for this client to send to the server.
        # It gets added to the clientlist first.
        if who=='send':
            send_one_message(c, str(addr).encode('utf-8'))
            newclient=PlayerClient(str(addr))
            newclient.from_player=c
            clientlist.append(newclient)
            #clientlist.append([str(addr), c])
            
            #thread1 = for_each_clientThread([str(addr),c], str(addr))
            #thread1.daemon=False
            #thread1.start()

        # After "send" socket is connected, the client will connect
        # again, this time sending a string "recv". This will be the
        # socket dedicated to messages from the server to the client.
        # Right now these messages should only be the "new_client" command.
        # TODO: make sure "send_all_sprites" doesn't go through this socket.
        elif who=='recv':
            global clientlocations
            parent, location=(pickle.loads(recv_one_message(c)))
            clientlocations[parent]=location
            templist=[]
            for dude in clientlist:
                if dude.address==parent:
                    # Add sockrec(from server to client) to clientlist.
                    dude.to_player=c
                    thread1 = for_each_clientThread(dude, parent)
                    thread1.daemon=False
                    thread1.start()
                else:
                    templist.append(dude)
            for dude in templist:
                # Now send 'new_client' to the new guy for each guy already connected.
                # This needs to be after the last loop to make sure recv socket was
                # already added to the clientlist.
                send_one_message(c, pickle.dumps(['new_client', dude.address]))
                #time.sleep(0.25)
                # Send a "new_client" message to everyone else already in server.
                send_one_message(dude.to_player, pickle.dumps(['new_client', parent]))
            return 0
        
        else:
            # If setting up a socket for one client to another, the following will run.
            # This comes from translate-> new client
            # in this form:  [fromaddr, parent]
            for guy in clientlist:
                if guy.address==who[0]:
                    guy.player_to_players.append((who[1],c))
                    print("New socket added to list.")
            # Wait a moment to set up all new sockets before getting sprites.
            time.sleep(0.25)
            # Now send 'get_all_sprites' message after sockets were setup.
            #TODO: uncomment?:
#             for guy in clientlist:
#                 if guy.address != who[0]:
#                     send_one_message(guy.to_player, pickle.dumps(['get_all_sprites', who[0]]))
                
                #TODO: 
                # this sends get all sprites to only those in the same location
#                 if guy[0]==who[1] and clientlocations[who[0]].name==clientlocations[who[1]].name:
#                     send_one_message(guy[2], pickle.dumps(['get_all_sprites', who[0]]))
#                 else:
#                     pass
#                     #print(clientlocations[who[0]].name)
#                     #print(clientlocations[who[1]].name)

      
    #TODO: get rid of self.guy, move his variables into here:
class for_each_clientThread (threading.Thread):
    """This thread is for listening to the "recv" socket for
    each client. It opens the message to look for keywords, like
    get_all_sprites or close, so it can perform requred tasks."""
    
    def __init__(self,guy, parent):
        """Takes a clientlist element and the address for the client.

        guy is in the form:
        [address1,
        client_send_socket,
        client_recv_socket,
        [client2_address, client1_to_client2_socket],
        [client3_address, client1_to_client3_socket]]
        """
        threading.Thread.__init__(self)
        self.guy=guy
        self.parent=parent
        self.done = False
        
    def run(self):
        """Each message is unpacked and checked for keywords.
        If there are no keywords the message is sent to all clients,
        excluding the client who originally sent this message.
        """
        global clientlist, clientlocations, game_map   # Delete global variables.
        while self.done==False:
            do=recv_one_message(self.guy.from_player)
            try:
                # If the message is a list or a string, use pickle to unpack it.
                newdo=pickle.loads(do)

##              # DELETE, no longer used this way
##                if newdo == 'get_all_sprites':
##                    reply_to=self.guy[0]
##                    #return_events(self.guy)
##                    print(str([newdo,reply_to]))
##                    sending=event_to_allThread(pickle.dumps([newdo,reply_to]),excpt=self.guy)
##                    sending.start()
##                    sending.join()


                # This is used to send a message to only one client.
                # It will be in the format:
                # ['just_one', send_to_address, message]
                if newdo[0] == 'map':
                    game_map=newdo[1]
                    print('got map')
                    #print(clientlist)
                    
                elif newdo[0] == 'get_map':
                    send_one_message(self.guy.to_player, pickle.dumps(('map', game_map)))
                    print('sentmap')
                    #print(clientlist)
#                     for client in clientlist:
#                         print('get all sprites')
#                         if client.address != self.guy.address:
#                             
#                             send_one_message(self.guy.to_player, pickle.dumps(('get_all_sprites', client.address)))
#                             send_one_message(client.to_player, pickle.dumps(('get_all_sprites', self.guy.address)))
                            
                elif newdo[0] == 'just_one':
                    reply_to=newdo[1]
                    reply=newdo[2]
                    found=False
                    for dude in self.guy.player_to_players:#range(3,len(self.guy)):
                        if dude[0]==reply_to and clientlocations[self.guy.address].name==clientlocations[reply_to].name:
                            found=True
                            send_one_message(dude[1], pickle.dumps(reply))
                    if found==False:
                    # Because multiple threads are running at once, the
                    # last loop may have ran before the socket is ready.
                    # If the socket wasn't found, run one more time.
                        for dude in self.guy.player_to_players:#range(3,len(self.guy)):
                            if dude[0]==reply_to and clientlocations[self.guy.address].name==clientlocations[reply_to].name:
                                found=True
                                send_one_message(dude[1], pickle.dumps(reply))
                                
                elif newdo[0] == 'new_location':
                    
                    new_location=newdo[1]
                    old_location=newdo[2]
                    #print(old_location.name)
                    #print(new_location.name)
                    clientlocations[self.guy.address]=new_location
                    
                    #TODO: fix:
                    #this sends get all sprites to only players in the same location
                    for client in clientlist:####
                        if client.address!=self.guy.address and clientlocations[client.address].name==new_location.name:
                                send_one_message(client.to_player, pickle.dumps(['get_all_sprites', self.guy.address]))
                                send_one_message(self.guy.to_player, pickle.dumps(['get_all_sprites', client.address]))
                        elif client.address!=self.guy.address and clientlocations[client.address].name==old_location.name:
                            send_one_message(client.to_player, pickle.dumps(['delete_player', self.guy.address]))
                            # TODO: might cause errors:
                            # this gets the new sprites, it will be deleted when one host holds all npcs
                            #send_one_message(client.to_player, pickle.dumps(['get_all_sprites', self.guy.address]))
                            #send_one_message(self.guy.to_player, pickle.dumps(['get_all_sprites', client.address]))
#                         else:
#                             print('ohhhhhnooooo!!!!')
#                             print(clientlocations[client.address].name)
#                             print('---')
#                             print(new_location.name)
                             
                            
                            
                #elif newdo == 'close_me':
                    # This means the client pressed the button to disconnect
                    # or the game was closed. In response, close the connection and
                    # delete this client from clientlist.
#                     self.guy[1].close()
#                     self.guy[2].close()
#                     for dude in range(3,len(self.guy)):
#                         #send_one_message(self.guy[dude][1], pickle.dumps(['close_him',self.guy[0]]))
#                         self.guy[dude][1].close()
#                     # TODO: also include a loop to close any other sockets in the list
#                     clientlist.remove(self.guy)
#                     #sending=event_to_allThread("close".encode("utf-8"),excpt=self.guy)
#                     #sending.start()
#                     #sending.join()
#                     print("Connection closed")
#                     # Stop running the thread.
#                     self.done=True
                    
                elif newdo =='testing':
                    # This prints the clientlist, for testing.
                    print("\nclientlist:\n"+str(clientlist))
                    
                elif newdo !="" and do!='connected'and do!='disconnected':
                    # If the message had no keywords, send it to all other clients
                    sending=event_to_allThread(pickle.dumps(newdo),excpt=self.guy)
#                                               location=clientlocations[self.guy[0]])
                    sending.start()
                    sending.join()
                       
                       
            # If any sprite doesn't show up, print these errors and contents:
            
            except UnicodeDecodeError:
                # If the message wouldn't unpack, it has no keywords.
                # The message will be sent to all other clients.
                print('UnicodeDecodeError')
                #print(newdo)
                sending=event_to_allThread(do,excpt=self.guy, 
                                           location=clientlocations[self.guy.address])
                sending.start()
                sending.join()
                
            except AttributeError:
                # If the message wouldn't unpack, it has no keywords.
                # The message will be sent to all other clients.
                print('Pickle Unpacking Error')
                #print(newdo)
                sending=event_to_allThread(do,excpt=self.guy, 
                                           location=clientlocations[self.guy.address])
                sending.start()
                sending.join()
                
            except EOFError:
                # TESTING, might not work:
                # For some reason, there is still an EOFError.
                # This is an attempt to resend the message.
                print("lost data")
                send_one_message(self.guy.address, pickle.dumps("error"))
                try_again=for_each_clientThread(self.guy, self.parent, 
                                           location=clientlocations[self.guy[0]])
                try_again.start()
                self.done=True
                
            except TypeError:  # this means the other person disconnected
                #self.done=True
                self.guy.from_player.close()
                self.guy.to_player.close()
                for dude in self.guy.player_to_players: #range(3,len(self.guy)):
                    #send_one_message(self.guy[dude][1], pickle.dumps(['close_him',self.guy[0]]))
                    dude[1].close()
                # TODO: also include a loop to close any other sockets in the list
                clientlist.remove(self.guy)
                for cl in clientlist:
                    for guy in cl.player_to_players:
                        if type(guy)==list:
                            if guy.address==self.guy.address:
                                del guy
                #sending=event_to_allThread("close".encode("utf-8"),excpt=self.guy)
                #sending.start()
                #sending.join()
                print("Connection closed")
                # Stop running the thread.
                self.done=True
                
                  
    
#def remove_player_sprites():
    
    
def send_one_message(sck, data):
    """This takes a socket and a message, then sends the message, then
    makes sure the message properly received. If it wasn't it resends
    the message.
    """
    
    # The receive function needs to know how long the message is, so it
    # only takes the exact number of bytes needed. Otherwise there will
    # be "end of file" errors.
    # First get the length of the length of the data and send it.
    length = len(data)
    sck.send(struct.pack('!I', length))
    
    # When the message 'length' is received, it is sent back here to be checked for errors.
    send_again=recvall(sck, 4)

    # If the message received doesn't match the message sent,
    # send "0" and resend message, repeating the process until they match.
    while struct.unpack('!I', send_again)[0] != length:
        #empty_socket(sck)
        sck.send(struct.pack('!I', 0))
        sck.send(struct.pack('!I', length))
        send_again=recvall(sck, 4)
        
    # If they match, send a "1" and continue sending message.
    sck.send(struct.pack('!I', 1))

    # Now send the intended message.
    sck.send(data)

    # When received the message will be sent back again.
    # Compare to the original message. If they don't match resend.
    message=recvall(sck, length)
    while message!=data:
        sck.send(struct.pack('!I', 0))
        sck.send(data)
        message=recvall(sck, length)
        
    # When they do match, send a "1"
    sck.send(struct.pack('!I', 1))



def recv_one_message(sck):
    """This is the counterpart for "send_one_message".

    It first recieves the length (of the message) then the message,
    and sends back each message to make sure they are the same.
    """

    # First the length is received, which is known to be 4 bytes long.
    lengthbuf = recvall(sck, 4)

    # Then return the length to make sure it matches.
    if lengthbuf!=None:
        sck.send(lengthbuf)
    else:
        return 

    # If they match, the send_one_message function will return a 1,
    # (also 4 bytes long).
    got_it=recvall(sck, 4)

    # If the other side returns a 0, they do not match.
    # The other side will now resend the data again.
    while struct.unpack('!I', got_it)[0] !=1:
        lengthbuf = recvall(sck, 4)
        sck.send(lengthbuf)
        got_it=sck.recv(4)

    # If they match, continue unpacking.
    length, = struct.unpack('!I', lengthbuf)

    # Call the recvall function to collect only "length" many bytes.
    message=recvall(sck, length)
    
    # Then return the length to make sure it matches.
    reply=sck.send(message)
    
    # If they match, the send_one_message function will return a 1.
    got_it=recvall(sck, 4)
    
    # If the other side returns a 0, they do not match.
    # The other side will now resend the data again.
    while struct.unpack('!I', got_it)[0] !=1:
        message=recvall(sck, length)
        reply=sck.send(message)
        got_it=sck.recv(4)

    # When the exact message of the correct length is collected,
    # return the message without decoding it.
    return message

def recvall(sock, count):
    """Takes a socket objest and an integer "count",
    then recieves "count" many bytes from the given socket,
    then returns the bytes without decoding it.
    """
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def add_to_list(add, towho):
    """Not used yet, but could help declutter other functions."""
    pass

# DELETE, now used as a new thread instead:
##def for_each_client(guy):
##   global clienteventlists
##   done=False
##   while done==False:
##      do=(guy.recv(1024).decode('utf-8'))
##      if do == 'get':
##         return_events(guy)
##      elif do == 'close':
##         add_to_list('disconnected', guy)
##         #clienteventlists[guy]append([guy, "disconnected"])
##         guy.send("Disconnected".encode("utf-8"))
##         guy.close()                # Close the connection
##         clientlist.remove(guy)
##         print("Connection closed")
##         #s.listen(5)
##         #c2, addr = s.accept()     # Establish connection with client. 
##         #print('Got connection from'+ str(addr))
##         #c2.send("Connected successfully".encode("utf-8"))
##         #clientlist.append(c2)
##         #clienteventlists.append([c2, ['connected again']])
##         done=True
##      elif do =='testing':
##         print(clienteventlists)
##      elif do !="" and do!='connected'and do!='disconnected':
##            print(do)
##            add_to_list(do, guy)
##            #clienteventlists.append([guy, do])
##            guy.send("server recieved info".encode("utf-8"))
##            #print(clienteventlists)
##   print("done")
##
##def new_guy():
##   print("start")
##   global clienteventlists, clientlist, port, host
##   port+=1
##   s = socket.socket()
##   s.bind((host, port))        # Bind to the port
##   done=False
##   clientlist=[]
##   s.listen(5)                 # Now wait for client connection.
##   c, addr = s.accept()     # Establish connection with client. 
##   print('Got connection from'+ str(addr))
##   c.send("Connected successfully".encode("utf-8"))
##   clientlist.append(c)
##   clienteventlists.append([c, ["connected"]])
##   thread1 = threading.Thread(for_each_client(c))
##   print("and back")
##   thread2 = threading.Thread(new_guy())
##   thread1.start()
##   thread2.start()
##   #threading.start_new_thread(new_guy())
   

def start_server():
    global clientlist
    clientlist=[]    # Remove global variables.   use fake global object?
    # Clientlist will later be in this format for 3 clients:
    # [
    # [address1, socksend1, sockrecv1, [client2 address, client2 socket],[client3 address,client3 socket]],
    # [address2, socksend2, sockrecv2, [client1 address, client1 socket],[client3 address,client3 socket]],
    # [address3, socksend3, sockrecv3, [client1 address, client1 socket],[client2 address,client2 socket]]
    # ]
    # address = the address and port for socksend. Used as an id for the list.
    # socksend = the socket object that handles messages sent from client to server
    # sockrecv = the socket object that handles messages from the server to the client (mostly "new client")
    # each client socket is a unique object that handles messages from socksend to client socket (in the same list)
    
    global clientlocations
    clientlocations={}

    # Get local machine name
    global host    # Remove global variables.
    host = socket.gethostname()

    # Reserve a port for your service.
    global port    # Remove global variables.
    port = 12345

    # delete, or use tcp functions:
##    serv = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
##    server = threading.Thread(target=serv.serve_forever)
##    server.start()

    # Create the main socket object
    global serv    # Remove global variables.
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to the port.
    #(not needed with socketserver?)
    serv.bind((host, port))

    # DELETE, no longer used:
    ##new_guy()

    # Verify the program is running.
    print("Whammer Server Running\n\n")

    # Begin listening to the main socket.
    newguy=newThread()
    #newguy.daemon=False
    newguy.start()

    # DELETE, thread now calls itself instead:
##    while 1:
##        newguy=newThread()
##        newguy.start()
##        newguy.join()


if __name__ == '__main__':
    start_server()
