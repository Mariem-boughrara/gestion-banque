from errno import EBUSY
from filecmp import cmp
from re import T
import threading
import queue
import socket

mutex = threading.Lock()

def consulter_compte(reference,in_q) :
	global mutex
	mutex.acquire()
	file1=open("/home/cyrine/Downloads/progsys/comptes.txt","r")
	line=file1.readline()
	while line:
		l=line.split(" ")
		if(int(l[0])==reference):
			in_q.put(line)
		line=file1.readline()
	file1.close()
	mutex.release()

def consulter_facture(reference) :
	global mutex
	mutex.acquire()
	file1=open("/home/cyrine/Downloads/progsys/factures.txt","r")
	line=file1.readline()
	while line:
		l=line.split(" ")
		if(int(l[0])==reference):
			print(line+"\n")
			return line
		line=file1.readline()
	file1.close()
	mutex.release()
	
	
def consulter_histo(reference) :
	global mutex
	mutex.acquire()
	file1=open("/home/cyrine/Downloads/progsys/histo.txt","r")
	line=file1.readline()
	while line:
		l=line.split(" ")
		if(int(l[0])==reference):
			mutex
			print(line+"\n")
		line=file1.readline()
	file1.close()
	mutex.release()
	
	



def debiter_compte(reference ,valeur,in_q):
	global mutex
	mutex.acquire()
	file1=open("/home/cyrine/Downloads/progsys/comptes.txt","r")
	tmp=open("/home/cyrine/Downloads/progsys/cmp.txt","w")
	file2=open("/home/cyrine/Downloads/progsys/histo.txt","a")
	file3=open("/home/cyrine/Downloads/progsys/factures.txt","a")
	ch=""
	ch1=""
	ch2=""
	line=file1.readline()
	while line:
		l=line.split(" ")
		if(int(l[0]) == reference):
			if (l[2]=="positif"):
				val=int(l[1])+valeur
				ch=ch+l[0]+" "+str(val)+" "+l[2]+" "+l[3]
				tmp.write(ch)
				ch1=ch1+"\n"+l[0]+" ajout "+str(valeur)+" succès "+l[2]
				file2.write(ch1)
				ch2=ch2+"\n"+l[0]+" 0.0"
				file3.write(ch2)
				in_q.put(1)
			else :  #etat negatif
				val2=float(valeur)*0.02
				if (int(l[1])<=valeur):
					val=int(valeur)-int(l[1])
					ch=ch+l[0]+" "+str(val)+" positif "+l[3]
					tmp.write(ch)
					ch1=ch1+"\n"+l[0]+" ajout "+str(valeur)+" succès "+" positif"
					file2.write(ch1)
					ch2=ch2+"\n"+l[0]+" "+str(val2)
					file3.write(ch2)
					in_q.put(1)
				else:
					val=int(l[1])-valeur
					ch=ch+l[0]+" "+str(val)+" négatif "+l[3]
					tmp.write(ch)
					ch1=ch1+"\n"+l[0]+" ajout "+str(valeur)+" succès "+" négatif"
					file2.write(ch1)
					ch2=ch2+"\n"+l[0]+" "+str(val2)
					file3.write(ch2)
					in_q.put(1)
		else:
			tmp.write(line)
			line=file1.readline()
	tmp.close()
	file1.close()
	file2.close()
	file3.close()
	file1=open("/home/cyrine/Downloads/progsys/comptes.txt","w")
	tmp=open("/home/cyrine/Downloads/progsys/cmp.txt","r")
	for line in tmp:
		file1.write(line)
	tmp.close()
	file1.close()
	mutex.release()
#=======================================================================================

def crediter_compte(reference,valeur,in_q):
	global mutex
	mutex.acquire()
	file1=open("/home/cyrine/Downloads/progsys/comptes.txt","r")
	tmp=open("/home/cyrine/Downloads/progsys/cmp.txt","w")
	file2=open("/home/cyrine/Downloads/progsys/histo.txt","a")
	file3=open("/home/cyrine/Downloads/progsys/factures.txt","a")
	ch=""
	ch1=""
	ch2=""
	line=file1.readline()
	while line:
		l=line.split(" ")
		if(int(l[0])==reference):
			val2=valeur*0.02
			if(l[2]=="positif"):
				if(int(valeur)<int(l[1])):
					val=int(l[1])-valeur
					ch=ch+l[0]+" "+str(val)+" "+l[2]+" "+l[3]
					tmp.write(ch)
					ch1=ch1+"\n"+l[0]+" retrait "+str(valeur)+" succès "+" positif"
					file2.write(ch1)
					ch2=ch2+"\n"+l[0]+" 0.0"
					file3.write(ch2)
					in_q.put(1)
				elif ((valeur>int(l[1])) and (valeur<int(l[1])+int(l[3]))):
					val=valeur-int(l[1])
					ch=ch+l[0]+" "+str(val)+" négatif "+l[3]
					tmp.write(ch)
					ch1=ch1+"\n"+l[0]+" retrait "+str(valeur)+" succès "+" négatif"
					file2.write(ch1)
					ch2=ch2+"\n"+l[0]+" "+str(val2)
					file3.write(ch2)
					in_q.put(1)
				else:
					print("Impossible de créditer ! \n")
					tmp.write(line)
					ch1=ch1+"\n"+l[0]+" retrait "+str(valeur)+" échec "+" positif"
					file2.write(ch1)
					in_q.put(0)
			else:#etat negatif
				val2=valeur*0.02
				if (valeur<int(l[3])-int(l[1])):
					val=valeur+int(l[1])
					ch=ch+l[0]+" "+str(val)+" "+l[2]+" "+l[3]
					tmp.write(ch)
					ch1=ch1+"\n"+l[0]+" retrait "+str(valeur)+" succès "+" négatif"
					file2.write(ch1)
					ch2=ch2+"\n"+l[0]+" "+str(val2)
					file3.write(ch2)
					in_q.put(1)
				else:
					print("Impossible de créditer ! \n")
					tmp.write(line)
					ch1=ch1+"\n"+l[0]+" retrait "+str(valeur)+" échec "+" négatif"
					file2.write(ch1)
					in_q.put(0)
		else:
			tmp.write(line)
		line=file1.readline()
	tmp.close()
	file1.close()
	file2.close()
	file3.close()
	file1=open("/home/cyrine/Downloads/progsys/comptes.txt","w")
	tmp=open("/home/cyrine/Downloads/progsys/cmp.txt","r")
	for line in tmp:
		file1.write(line)
	tmp.close()
	file1.close()
	mutex.release()



host,port=('',5565)

socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host,port))
print("Le serveur est démarré... \n")
socket.listen(5)
q=queue.Queue()
q1=queue.Queue()
while True:
	client, adresse=socket.accept()
	print(f"connexion etabli - {adresse[0]}:{adresse[0]}")
	print("En écoute... \n")
	ch = client.recv(1024).decode("utf8")
	print("choix : ",ch)
	ch1 = client.recv(1024).decode("utf8")
	print("reference : ",ch1)
	if (ch=="1"):
		t = threading.Thread(target=consulter_compte,args=(int(ch1),q))
		t.start()
		#print("size : "+str(q.qsize()))
		res = q.get()
		#print("size : "+str(q.qsize()))
		print(res)
		code = res.encode("utf8")
		client.send(code)
	elif (ch=="2") :
		val = client.recv(1024).decode("utf8")
		print("valeur : ",val)
		t = threading.Thread(target=debiter_compte,args=(int(ch1),int(val),q1))
		t.start()
		#print("size : "+str(q1.qsize()))
		res = q1.get()
		#print("size : "+str(q1.qsize()))
		#print(res)
		if (res==1):
			ch="débit avec succès"
			print(ch)
		else :
			ch="échec,Réessayer SVP"
			print(ch)
		code = ch.encode("utf8")
		client.send(code)
	elif (ch=="3") :
		val = client.recv(1024).decode("utf8")
		print("valeur : ",val)
		t = threading.Thread(target=crediter_compte,args=(int(ch1),int(val),q1))
		t.start()
		#print("size : "+str(q1.qsize()))
		res = q1.get()
		#print("size : "+str(q1.qsize()))
		#print(res)
		if (res==1):
			ch="crédit avec succès"
			print(ch)
		else :
			ch="échec,Réessayer SVP"
			print(ch)
		code = ch.encode("utf8")
		client.send(code)
client.close()
socket.close()
