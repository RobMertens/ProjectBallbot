import pyre

P_NODE_SELF = 'RPi'
P_NODE_GROUP = 'EAGLE'

node = pyre.Pyre(NODE_SELF)
node.start()
node.join(NODE_GROUP)

while(1):
	msg = node.recv()
	print(msg)


