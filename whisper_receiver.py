import pyre

P_NODE_SELF = 'RPi'
P_NODE_GROUP = 'EAGLE'

node = pyre.Pyre(P_NODE_SELF)
node.start()
node.join(P_NODE_GROUP)

while(1):
	msg = node.recv()
	print(msg[3])


