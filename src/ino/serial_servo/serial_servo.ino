#include <Servo.h>
#include <Wire.h>

#define LEFT 3
#define RIGHT 5
#define I2C_ADDR 0x73

Servo left;
Servo right;

void setup() {
  left.attach(LEFT);
  right.attach(RIGHT);
  left.write(90);
  right.write(90);
  Wire.begin(I2C_ADDR);
}

void loop() {
  
  if (Wire.available()) {
    
    char first;
    String pos_str;
    first = Wire.read();
    while (Wire.available() > 0) {
      pos_str += (char) Wire.read();
    }
    int pos = pos_str.toInt();
    
    switch (first) {
      case 'l':
        left.write(pos);
        break;
      case 'r':
        right.write(pos);
        break;
    }
    
  }
  
}

