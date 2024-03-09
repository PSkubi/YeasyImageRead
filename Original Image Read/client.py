import socket
import time
import time
import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

HEADER = 64                                                     # the first message the client sends to the server will be the length of the message
PORT = 5050                                                     # port that we are going to use
#SERVER = '192.168.1.29'
SERVER = socket.gethostbyname(socket.gethostname())             # get the ip address of the server
ADDR = (SERVER, PORT)                                           # tuple of the server and port
FORMAT = 'utf-8'                                                # format of the message
DISCONNECT_MESSAGE = "!DISCONNECT"                              # message to disconnect

client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # create a socket object
client.connect(ADDR)                                            # connect to the server

def send_string(msg):
    message = msg.encode(FORMAT)                                # encode the message
    msg_info = str(len(message))+'_str'                          # get the info of the message    
    send_info = msg_info.encode(FORMAT)                # encode the length of the message
    send_info += b' ' * (HEADER - len(send_info))           # add spaces to the length of the message to make it 64 bytes
    client.send(send_info)                                    # send the length of the message                             
    client.send(message)                                        # send the message
def send_bytes(msg):
    msg_info = str(len(msg))+'_byt'                          # get the info of the message   
    #print(f'Sent message info: {msg_info}') 
    send_info = msg_info.encode(FORMAT)                # encode the length of the message
    send_info += b' ' * (HEADER - len(send_info))           # add spaces to the length of the message to make it 64 bytes
    client.send(send_info)                                    # send the length of the message                             
    client.send(msg)                                        # send the message
########################### File Management ############################
# Start with identifying the directory and folders within it
folder =os.path.dirname(os.path.realpath(__file__))
flist = [0,0]
flist[0] = [x[0] for x in os.walk(folder)]
flist[1] = [x[1] for x in os.walk(folder)][0]
flist[0].pop(0)

# create a list of chamber names 
c_list = []
for i in range(20):
    c_list.append('Chamber '+str(i+1))
c_flist = [os.listdir(flist[0][0]), os.listdir(flist[0][1]), os.listdir(flist[0][2])]

chamber_sizes = [len(c_flist[0]), len(c_flist[1]), len(c_flist[2])]

# Which types of images are supported:
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# create sub list of image files (no wrong file types)

fnames = [0,0,0] # List storing the names of image files
fnames[0] = [f for f in c_flist[0] if f.lower().endswith(img_types)]

fnames[1] = [f for f in c_flist[1] if f.lower().endswith(img_types)]

fnames[2] = [f for f in c_flist[2] if f.lower().endswith(img_types)]

# If there are no suitable images, throw a popup
if chamber_sizes[0] == 0:
    sg.popup('No files from Chamber 1!')
    raise SystemExit()
if chamber_sizes[1] == 0:
    sg.popup('No files from Chamber 2!')
    raise SystemExit()
if chamber_sizes[2] == 0:
    sg.popup('No files from Chamber 3!')
    raise SystemExit()

################################## Image reading ######################################

# Define a function which opens an image file using Python Imaging Library
def get_img_data(f, maxsize=(1600, 1000), first=False):
    """Generate image data using PIL"""
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

def image_to_bytes(image_path):
    with Image.open(image_path) as image_file:
        #image_file = image_file.resize((500,500))
        image_bytes = io.BytesIO()
        image_file.save(image_bytes, format='PNG')
    return image_bytes.getvalue()
##################################  Start reading data ######################################

# active chamber index
active_chamber = 0

i = 1
while True:
    time.sleep(0.5)
    if i >= chamber_sizes[active_chamber]:
        i -= chamber_sizes[active_chamber]
    filename = os.path.join(flist[0][active_chamber], fnames[active_chamber][i])
    byte_im = image_to_bytes(filename)
    #send_string(f'Image size of {i}: {len(byte_im)}')
    send_bytes(byte_im)
    print(f'Image number {i} of size {len(byte_im)} sent to the server!')
    i+=1