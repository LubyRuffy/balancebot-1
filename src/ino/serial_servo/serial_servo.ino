#include <Servo.h>
#include <Wire.h>

#define LEFT 3
#define RIGHT 5
#define I2C_ADDR 0x73

Servo left;
Servo right;

volatile int lPos;
volatile int rPos;

void setup() {
  pinMode(LEFT, OUTPUT);
  pinMode(RIGHT, OUTPUT);
  left.attach(LEFT);
  right.attach(RIGHT);
  
  lPos = 90;
  rPos = 90;
  
  Wire.begin(I2C_ADDR);
  Wire.onReceive(recieveEvent);

  Serial.begin(115200);
  Serial.println("asd");
}

void loop() {
  left.write(lPos);
  right.write(rPos);
}

void recieveEvent(int bytes) {
  char first = Wire.read();
  uint8_t pos = Wire.read();
  clearBuff();
  Serial.println(first);
  Serial.println(pos);
  switch (first) {
    case 'l':
      lPos = pos;
      break;
    case 'r':
      rPos = pos;
      break;
  }
}

void clearBuff() {
  while (Wire.available() > 0) {
    Wire.read();
  }
}

