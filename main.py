import processing.dxf.*;

PShape lander;
import hypermedia.net.UDP;
import hypermedia.net.*;
import controlP5.*;

ControlP5 cp5;
Chart yawGraph;
Chart rollGraph;
Chart pitchGraph;
Textlabel myTextlabelA;
Textlabel myTemperature;
Textlabel AccX;
Textlabel AccY;
Textlabel AccZ;
Textarea consolearea;
Println console;

UDP udp;
float[] Euler = new float[3];
float temperature = 0;
float accx = 0;
float accy = 0;
float accz = 0;
float calib = 0;
int marginfromtop = 0;

public void setup() {
  udp = new UDP(this, 6000);
  udp.listen(true);
  fullScreen(P3D);
  smooth(8);
  marginfromtop = ((height * 10) / 100);

  lander = loadShape("LanderV1.obj");
  lander.scale(1 + (height / 1000));
  cp5 = new ControlP5(this);
  cp5.enableShortcuts();
  // Creates live graph for yaw axis
  yawGraph = cp5.addChart("YAW")
    .setPosition(50, marginfromtop)
    .setSize((width * 20) / 100, (height * 10) / 100)
    .setRange(-90, 90)
    .setView(Chart.LINE)
    .setStrokeWeight(2)
    .setColorCaptionLabel(color(255,00,00))
    .setColorBackground(color(255, 255, 255));
  yawGraph.addDataSet("incoming");
  yawGraph.setData("incoming", new float[100]);
  // Creates live graph for roll axis
  rollGraph = cp5.addChart("ROLL")
    .setPosition(50, marginfromtop + ((height * 10) / 100) + 20)
    .setSize((width * 20) / 100, (height * 10) / 100)
    .setRange(-90, 90)
    .setView(Chart.LINE)
    .setStrokeWeight(2)
    .setColorCaptionLabel(color(255, 00, 00))
    .setColorBackground(color(255, 255, 255))
    .setColorActive(color(255, 0, 0));
  rollGraph.addDataSet("incoming");
  rollGraph.setData("incoming", new float[100]);
  // Creates live graph for pitch axis
  pitchGraph = cp5.addChart("PITCH")
    .setPosition(50, marginfromtop + ((height * 10) / 100) * 2 + 40)
    .setSize((width * 20) / 100, (height * 10) / 100)
    .setRange(-90, 90)
    .setView(Chart.LINE)
    .setStrokeWeight(6)
    .setColorCaptionLabel(color(255,00,00))
    .setColorBackground(color(255, 255, 255));
  pitchGraph.addDataSet("incoming");
  pitchGraph.setData("incoming", new float[100]);

  myTextlabelA = cp5.addTextlabel("label")
    .setText("OPTIMUS")
    .setPosition(10, 10)
    .setColorValue(color(255, 0, 0))
    .setFont(createFont("Lucida Console", 20))
    .setColorBackground(color(152, 190, 100))
    .setColorForeground(color(204, 193, 145));

  myTemperature = cp5.addTextlabel("Temperature")
    .setPosition(width - ((width * 25) / 100), height - (((height * 20) / 100)))
    .setColorValue(color(255, 0, 0))
    .setFont(createFont("Lucida Console", 18))
    .setColorBackground(color(152, 190, 100))
    .setColorForeground(color(204, 193, 145));

  AccX = cp5.addTextlabel("Acceleration X")
    .setPosition(width - ((width * 25) / 100), height - (((height * 20) / 100) + 20))
    .setColorValue(color(255, 0, 0))
    .setFont(createFont("Lucida Console", 18))
    .setColorBackground(color(152, 190, 100))
    .setColorForeground(color(204, 193, 145));

  AccY = cp5.addTextlabel("Acceleration Y")
    .setPosition(width - ((width * 25) / 100), height - (((height * 20) / 100) + 40))
    .setColorValue(color(255, 0, 0))
    .setFont(createFont("Lucida Console", 18))
    .setColorBackground(color(152, 190, 100))
    .setColorForeground(color(204, 193, 145));

  AccZ = cp5.addTextlabel("Acceleration Z")
    .setPosition(width - ((width * 25) / 100), height - (((height * 20) / 100) + 60))
    .setColorValue(color(255, 0, 0))
    .setFont(createFont("Lucida Console", 18))
    .setColorBackground(color(152, 190, 100))
    .setColorForeground(color(204, 193, 145));

  consolearea = cp5.addTextarea("console")
    .setPosition(50, height - 150)
    .setSize((width * 40) / 100, (height * 10) / 100)
    .setFont(createFont("Lucida Console", 12))
    .setLineHeight(14)
    .setColor(color(128))
    .setColorBackground(color(255, 100))
    .setColorForeground(color(255, 100));

  console = cp5.addConsole(consolearea);
}

void draw() {
  hint(ENABLE_DEPTH_TEST);
  pushMatrix();
  //---------------------
  background(000, 000, 000);
  rect(0, 0, 220, 40, 0, 10, 10, 0);
  fill(0);
  ambientLight(128, 128, 128);

  directionalLight(128, 128, 128, 0, 0, -1);

  translate(10*width / 21 ,2* height /5, 250);  // Adjust the second parameter to move higher or lower
  rotateX(-Euler[2] * 3.14 / 180);
  rotateZ(Euler[0] * 3.14 / 180 + calib * 3.14 / 180);
  rotateY(Euler[1] * 3.14 / 180);
  shape(lander);
  yawGraph.push("incoming", Euler[1]);
  rollGraph.push("incoming", Euler[0]);
  pitchGraph.push("incoming", Euler[2]);
  //---------------------
  popMatrix();
  hint(DISABLE_DEPTH_TEST);
}


void receive(byte[] data, String ip, int port) {
  data = subset(data, 0, data.length);
  String message = new String(data);
  String[] list = split(message, ',');

  temperature = int(list[3]);
  accx = Float.parseFloat(list[0]);
  accy = Float.parseFloat(list[1]);
  accz = Float.parseFloat(list[2]);
  myTemperature.setText("Temperature:-" + temperature);
  AccX.setText("Acceleration X:- " + int(accx * 10) + "m/s");
  AccY.setText("Acceleration Y:- " + int(accy * 10) + "m/s");
  AccZ.setText("Acceleration Z:- " + int(accz * 10) + "m/s");

  Euler[0] = Float.parseFloat(list[4]);
  Euler[1] = Float.parseFloat(list[5]);
  Euler[2] = Float.parseFloat(list[6]);

  println("From: " + ip + "  on port: " + port);
  println("Calibration: " + calib);
  println("Incoming: " + message);
}

void mousePressed() {
  calib = Euler[0];
}
