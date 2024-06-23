from p5 import *
import socket
import threading

# Global variables
lander = None
yaw_graph = None
roll_graph = None
pitch_graph = None
temperature = 0
accx = 0
accy = 0
accz = 0
calib = 0
Euler = [0, 0, 0]
marginfromtop = 0

# UDP
UDP_IP = "0.0.0.0"
UDP_PORT = 6000

def setup():
    global lander, yaw_graph, roll_graph, pitch_graph, marginfromtop
    size(800, 600, P3D)
    marginfromtop = ((height * 10) / 100)
    
    # Load 3D model (this will depend on the format; here we use a placeholder)
    lander = load_shape("LanderV1.obj")  # Replace with actual method to load 3D model
    
    # Setup graphs and text labels
    setup_graphs()
    setup_text_labels()
    
    # Setup UDP
    threading.Thread(target=udp_listener).start()

def setup_graphs():
    global yaw_graph, roll_graph, pitch_graph
    yaw_graph = create_graph("YAW", 50, marginfromtop)
    roll_graph = create_graph("ROLL", 50, marginfromtop + ((height * 10) / 100) + 20)
    pitch_graph = create_graph("PITCH", 50, marginfromtop + ((height * 10) / 100) * 2 + 40)

def create_graph(label, x, y):
    graph = {}  # Placeholder for graph creation
    # Add necessary setup for your graph
    return graph

def setup_text_labels():
    global my_text_label_a, my_temperature, acc_x, acc_y, acc_z, console_area
    my_text_label_a = create_text_label("OPTIMUS", 10, 10, 20)
    my_temperature = create_text_label("Temperature", width - ((width * 25) / 100), height - (((height * 20) / 100)), 18)
    acc_x = create_text_label("Acceleration X", width - ((width * 25) / 100), height - (((height * 20) / 100) + 20), 18)
    acc_y = create_text_label("Acceleration Y", width - ((width * 25) / 100), height - (((height * 20) / 100) + 40), 18)
    acc_z = create_text_label("Acceleration Z", width - ((width * 25) / 100), height - (((height * 20) / 100) + 60), 18)
    console_area = create_text_label("", 50, height - 150, 12)

def create_text_label(text, x, y, font_size):
    label = {}  # Placeholder for text label creation
    # Add necessary setup for your text label
    return label

def draw():
    hint(ENABLE_DEPTH_TEST)
    push_matrix()
    background(0)
    fill(0)
    ambient_light(128, 128, 128)
    directional_light(128, 128, 128, 0, 0, -1)
    translate(10 * width / 21, 2 * height / 5, 250)
    rotate_x(-Euler[2] * PI / 180)
    rotate_z(Euler[0] * PI / 180 + calib * PI / 180)
    rotate_y(Euler[1] * PI / 180)
    shape(lander)
    yaw_graph["data"].append(Euler[1])
    roll_graph["data"].append(Euler[0])
    pitch_graph["data"].append(Euler[2])
    pop_matrix()
    hint(DISABLE_DEPTH_TEST)

def udp_listener():
    global temperature, accx, accy, accz, Euler
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode("utf-8")
        list_data = message.split(',')
        
        temperature = int(list_data[3])
        accx = float(list_data[0])
        accy = float(list_data[1])
        accz = float(list_data[2])
        
        my_temperature["text"] = f"Temperature: {temperature}"
        acc
