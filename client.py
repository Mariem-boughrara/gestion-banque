import socket
host, port=('172.18.2.207',5565)#il faut que le port resterait le meme     changer l'adresse ip de la machine
socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host,port))
while True:
	print("Client connecté")
	print("\n------------------------------------------------------------\n")
	print("\n-------             1. consulter compte             --------\n")
	print("\n-------             2. debiter                      --------\n")
	print("\n-------             3. crediter                     --------\n")
	print("\n------------------------------------------------------------\n")
		
	#saisir le choix
	print("Choix: ")
	choix=input()
	ch = choix.encode("utf8")
	socket.send(ch)

	#saisir le choix
	print("Donner la réference de votre compte ")
	ref=input()
	ch=ref.encode("utf8")
	socket.send(ch)

	#saisir la valeur à débiter ou à créditer
	if(choix=="2") :
		print("Donner la valeur à débiter : ")
		val=input()
		ch=val.encode("utf8")
		socket.send(ch)

	elif(choix=="3") :
		print("Donner la valeur à créditer : ")
		val=input()
		ch=val.encode("utf8")
		socket.send(ch)
			
	ch = socket.recv(2048).decode("utf8")
	print(ch)
	socket.close()
			
