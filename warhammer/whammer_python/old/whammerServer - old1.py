#!/usr/bin/python           # This is server.py file

import socket, threading, pickle, struct


class string_to_allThread (threading.Thread):
   def __init__(self, message,excpt='none'):
      threading.Thread.__init__(self)
      self.excpt=excpt
      self.message=message
   def run(self):
      for guy in clientlist:
         if guy.addr!=self.excpt.addr:
            guy.send(self.message.encode('utf-8'))

class event_to_allThread (threading.Thread):
   def __init__(self, message,excpt='none'):
      threading.Thread.__init__(self)
      self.excpt=excpt
      self.message=message
   def run(self):
      for guy in clientlist:
         if guy!=self.excpt:
            send_one_message(guy, self.message)
            #guy.send(self.message)

class newThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      global clienteventlists, clientlist, serv
      serv.listen(5)                 # Now wait for client connection.
      c, addr = serv.accept()     # Establish connection with client.
      print(c)
      print('Got connection from'+ str(addr))
      send_one_message(c, "Connected successfully".encode('utf-8'))
      #c.send("Connected successfully".encode("utf-8"))
      clientlist.append(c)
      #clienteventlists.append([c, ["connected"]])
      thread1 = for_each_clientThread(c)
      thread1.start()
      
      
class for_each_clientThread (threading.Thread):
   def __init__(self,guy):
      threading.Thread.__init__(self)
      self.guy=guy
   def run(self):
      global clienteventlists, clientlist
      #self.done=False
      #while self.done==False:
      do=recv_one_message(self.guy)
      #do=self.guy.recv(16000)
      thread2 = for_each_clientThread(self.guy)
      thread2.start()
      try:
         do=do.decode('utf-8')
         if do == 'get':
            return_events(self.guy)
         elif do == 'close':
            add_to_list('disconnected', self.guy)
            self.guy.close()                # Close the connection
            clientlist.remove(self.guy)
            print("Connection closed")
            #self.done=True
         elif do =='testing':
            print("\nclientlist:\n"+str(clientlist))
            print("\nclienteventlists:\n"+str(clienteventlists))
         elif do =="get_all_sprites":
            print("working")
         elif do !="" and do!='connected'and do!='disconnected':
               print(do)
               add_to_list(do, self.guy)
               #self.guy.send("server recieved info".encode("utf-8"))
               sending=string_to_allThread(do,excpt=self.guy)
               sending.start()
      except UnicodeDecodeError:
         #print(pickle.loads(do))
         #print(do)
         sending=event_to_allThread(do,excpt=self.guy)
         sending.start()

def send_one_message(sck, data):
    length = len(data)
    sck.sendall(struct.pack('!I', length))
    sck.sendall(data)

def recv_one_message(sck):
    lengthbuf = recvall(sck, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sck, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf            

def return_events(thisguy):
   global clienteventlists
   templist=[]
   for client in clienteventlists:
      #if client[0]==thisguy:
      #if client[0]!=thisguy:
         for thing in client[1]:
            templist.append(thing)
   thisguy.send(str(templist).encode('utf-8'))

def add_to_list(add, towho):
   global clienteventlists
   for client in clienteventlists:
      if client[0]==towho:
         client[1].append(add)

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
   


#clienteventlists=[]
clientlist=[]

host = socket.gethostname() # Get local machine name
port = 12345               # Reserve a port for your service.
serv = socket.socket()
serv.bind((host, port))        # Bind to the port

#new_guy()

while 1:
   newguy=newThread()
   newguy.start()
   newguy.join()
   #for cl in clientlist:
   #  for_each_client(cl)
