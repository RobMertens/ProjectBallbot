import pyre
import time

node = pyre.Pyre('Rob')
node.start()
node.join('EAGLE')

while(1):
	peers = node.peers()
	for p in peers:
		if(node.get_peer_name(p)=='Ibe'):
			uuid = p
			print("Ibe", uuid)
			
			node.whisper(uuid, "Hello, I'm Rob!")
	
	time.sleep(1.0)


