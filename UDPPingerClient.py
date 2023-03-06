from socket import *
import time

HOST = 'localhost'
PORT = 12000
NUM_PACKETS = 10

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

rtts = []

for i in range(1, NUM_PACKETS + 1):
    message = f'Ping {i} {time.time()}'

    clientSocket.sendto(message.encode(), (HOST, PORT))

    try:
        data, address = clientSocket.recvfrom(1024)
        data = data.decode()
        sentTime = float(data.split()[2])
        rtt = (time.time() - sentTime) * 1000
        rtts.append(rtt)
        print(data, '{:.2f}'.format(rtt), 'ms')
    except timeout:
        print('Request timed out')

min_rtt = min(rtts)
max_rtt = max(rtts)
avg_rtt = sum(rtts) / len(rtts)

packet_loss = (1 - len(rtts) / NUM_PACKETS) * 100

print('min: {:.2f}'.format(min_rtt), 'ms', 'max: {:.2f}'.format(max_rtt), 'ms', 'average: {:.2f}'.format(avg_rtt), 'ms')
print('{:.2f}% packet loss'.format(packet_loss))