#include <RCSwitch.h>
RCSwitch mySwitch = RCSwitch();

void setup() {
  Serial.begin(9600);
  mySwitch.enableTransmit(10);
}

void loop() {

 int x_data = analogRead(A0);
 int y_data = analogRead(A1);
 int value_X = x_data;
 int value_Y = y_data;
 int value ;
 if((x_data>400 && y_data>600 )||(x_data>400 && y_data<400)){
   value = map(value_Y, 0, 1024, 0, 180);
}
else if((x_data<400 && y_data>400 )||(x_data>600 && y_data>400)){
   value = map(value_X , 0, 1024, 200, 380);
}


  mySwitch.send(value, 30);

       
Serial.print("x_data:");
 Serial.print(x_data);
 Serial.print("\t");
 Serial.print("y_data:");
 Serial.print(y_data);
 Serial.println("\t");
  Serial.println(value);


    
}
