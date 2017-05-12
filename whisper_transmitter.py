import pyre
import time

P_NODE_SELF = 'RPi'
P_NODE_EXTERN = 'PC'
P_GROUP = 'EAGLE'

node = pyre.Pyre(P_NODE_SELF)
node.start()
node.join(P_GROUP)

while(1):
	peers = node.peers()
	for p in peers:
		if(node.get_peer_name(p)==P_NODE_EXTERN):
			uuid = p
			print(P_NODE_EXTERN, uuid)
			
			node.whisper(uuid, "ENDPOINT")
	
	time.sleep(1.0)
	
	msg = node.recv()
	while(msg[0]!='WHISPER'):		
		msg = node.recv()
	
	print(msg)
