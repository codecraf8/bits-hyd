            NETWORK FUNDAMENTALS and BASIC DESIGN  PATTERN
        *******************************    

The Problem:
	* Communication Between two computers
	* It's just sending/receiving bits.

Two main issues:
	* Addressing
		* Specifying a remote computer and service.

	* Data transport
		* Moving bits back and forth.	

   i. STANDARD PORTS
  ......................

* Ports for common services are preassigned 
	
		21 		FTP
		22 		SSH
		23 		Telnet
		25 		SMTP (Mail)
		80 		HTTP (Web)
		110 	POP3 (Mail)
		119 	NNTP (News)
		443 	HTTPS (web)  		

* Other port numbers may just be randomly
  assigned to programs by the operating system		

   ii. CONNECTIONS 
  .....................

* Each endpoint of a network connection is always
  represented by a host and port #

* In Python you write it out as a tuple (host,port)
	("www.python.org",80)
	("205.172.13.4",443)	  

* In almost all of the network programs you’ll
  write, you use this convention to specify a
  network address.

   iii. USING TELNET
  .....................
  
* As a debugging aid, telnet can be used to
  directly communicate with many services 

      telnet hostname portnum  

  • Example:
		shell % telnet www.python.org 80
		Trying 82.94.237.218...
		Connected to www.python.org.
		Escape character is '^]'.
		GET /index.html HTTP/1.0
		HTTP/1.1 200 OK
		Date: Mon, 31 Mar 2008 13:34:03 GMT
		Server: Apache/2.2.3 (Debian) DAV/2 SVN/1.4.2
		mod_ssl/2.2.3 OpenSSL/0.9.8c        

  iv. SOCKET
  ............

*Socket Basics
	
	• To create a socket
		import socket
		s = socket.socket(addr_family, type)

	• Address families	
		socket.AF_INET Internet protocol (IPv4)
		socket.AF_INET6 Internet protocol (IPv6)
	• Socket types
		socket.SOCK_STREAM Connection based stream (TCP)
		socket.SOCK_DGRAM Datagrams (UDP)
	• Example:	
		from socket import *
		s = socket(AF_INET,SOCK_STREAM)

   v. TCP CLIENT
 .................		
 	
 	• How to make an outgoing connection

 	*Code/script:

 		from socket import *
		s = socket(AF_INET,SOCK_STREAM)
		s.connect(("www.python.org",80)) # Connect
		s.send("GET /index.html HTTP/1.0\n\n") # Send request
		data = s.recv(10000) # Get response
		s.close()

   vi. TCP SERVER
  .................

    *code/script:
    	from socket import *
		s = socket(AF_INET,SOCK_STREAM)
		s.bind(("",9000))
		s.listen(5)
		while True:
		 	c,a = s.accept()
		 	print "Received connection from", a
		 	c.send("Hello %s\n" % a[0])
		 	c.close()

   vii. PARTIAL READS/WRITES
   ...........................

	• Be aware that for TCP, the data stream is
	  continuous---no concept of records, etc.

		# Client
		...
		s.send(data)
		s.send(moredata)
		...
		# Server
		...
		data = s.recv(maxsize) <<----
									-->	This recv() may return data
										from both of the sends
										combined or less data than
										even the first send

	• A lot depends on OS buffers, network
	  bandwidth, congestion, etc.

   viii. DATA REASSEMBLY
   .......................

   • Receivers often need to reassemble
	 messages from a series of small chunks

	• Here is a programming template for that:

	code/scripts:
	 	fragments = []               # List of chunks

		while not done:
		 	chunk = s.recv(maxsize)   # Get a chunk
		 	if not chunk:
		 		break # EOF. No more data
		 	fragments.append(chunk)

		# Reassemble the message
		message = "".join(fragments)

 
   ix. SOCKETS AS FILE
   .....................

   • Sometimes it is easier to work with sockets
	 represented as a "file" object
		    f = s.makefile()

	• This will wrap a socket with a file-like API
			f.read()
			f.readline()
			f.write()
			f.writelines()
			for line in f:
			 ...
			f.close()		

	x. UDP: DATAGRAMS
	....................

	• Data sent in discrete packets (Datagrams)
	• No concept of a "connection"
	• No reliability, no ordering of data
	• Datagrams may be lost, arrive in any order
	• Higher performance (used in games, etc.)

	    A. UDP SERVER
	    ...............

	    *code/scripts:
	    			from socket import *
					s = socket(AF_INET,SOCK_DGRAM)
					s.bind(("",10000))
					while True:
					 	data, addr = s.recvfrom(maxsize)
					 	resp = "Get off my lawn!"
					 	s.sendto(resp,addr)

	• No "connection" is established
	• It just sends and receives packets

	    B. UDP CLIENT
	    ...............

	    *code/script:

	    from socket import *
		s = socket(AF_INET,SOCK_DGRAM)

		msg = "Hello World"
		s.sendto(msg,("server.com",10000))

		data, addr = s.recvfrom(maxsize)

    xi. Sockets and Concurrency
    ..............................

		• To manage multiple clients,

		• Server must always be ready to accept
		  new connections

		• Must allow each client to operate
		  independently (each may be performing
		  different tasks on the server)

		• Will briefly outline the common solutions
    
    xii. Threaded Server
    .......................

     	• Each client is handled by a separate thread

     	script:
     		import threading
			from socket import *

			def handle_client(c):
			 ... whatever ...
			 c.close()
			 return
			s = socket(AF_INET,SOCK_STREAM)
			s.bind(("",9000))
			s.listen(5)
			while True:
			 	c,a = s.accept()
			 	t = threading.Thread(target=handle_client,args=(c,))


	xiii. Forking Server(UNIX)		 	
	..............................
	    • Each client is handled by a subprocess

	    script:
			import os
			from socket import *
			s = socket(AF_INET,SOCK_STREAM)
			s.bind(("",9000))
			s.listen(5)

			while True:
				c,a = s.accept()
				if os.fork() == 0:
				# Child process. Manage client
				...
				c.close()
				os._exit(0)
				else:
				 # Parent process. Clean up and go
				 # back to wait for more connections
				c.close()	

	xiv. Asynchronous Server
	.........................

	• Server handles all clients in an event loop

	script:
		import select
		from socket import *
		s = socket(AF_INET,SOCK_STREAM)
		...
		clients = [] # List of all active client sockets
		while True:
		 	# Look for activity on any of my sockets
		 	input,output,err = select.select(s+clients,clients, clients)
		 	
		 # Process all sockets with input
		 	for i in input:
		 		...

		 	# Process all sockets ready for output
		 	for o in output:
		 		...			 	