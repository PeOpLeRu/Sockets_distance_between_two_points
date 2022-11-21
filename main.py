from math import sqrt
import matplotlib.pyplot as plt
import socket
import numpy as np
from skimage.measure import label, regionprops

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
        # print(len(data))
    return data

host = "84.237.21.36"
port = 5152
packet_size = 40002

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))

    beat = b"nope"

    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, packet_size)

        rows, cols = bts[:2]
        im1 = np.frombuffer(bts[2 : rows * cols + 2], dtype='uint8').reshape(rows, cols)

        plt.clf()
        plt.subplot(121)
        plt.imshow(im1)

        bin_im1 = im1
        bin_im1[bin_im1 > 0] = 1
        props = regionprops(label(bin_im1))
        
        if len(props) < 2:
            continue

        plt.subplot(122)
        plt.imshow(bin_im1)
        
        coord_0 = props[0].centroid
        coord_1 = props[1].centroid
        diff = np.abs(np.array(coord_0) - np.array(coord_1))
        print(f"sqrt = {sqrt(diff[0] ** 2 + diff[1] ** 2)}")
        distance = round(sqrt(diff[0] ** 2 + diff[1] ** 2), 1)
        print(f"distance -> {distance}")

        sock.send(f"{distance}".encode())
        print(sock.recv(20))

        plt.pause(0.2)

        # char = input("enter to continue...")

        sock.send(b"beat")
        beat = sock.recv(20)

print("Done")