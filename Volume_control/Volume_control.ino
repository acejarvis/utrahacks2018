
// define ports
#define pin_1 A0
#define pin_2 A1
#define pin_3 A2

// define the detect-range
#define upperLimit 75
#define lowerLimit 0

int volume;
int dist_1,dist_2,dist_3;


void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(pin_1, INPUT);
  pinMode(pin_2, INPUT);
  pinMode(pin_3, INPUT);
}
 
void loop() {
  //get distance
  dist_1 = 2.6851 *exp(0.0035*analogRead(pin_1))-10;
  dist_2 = 2.6851 *exp(0.0035*analogRead(pin_2))-10;
  dist_3 = 2.6851 *exp(0.0035*analogRead(pin_3))-10;

  //get volume converted from distance
  if(dist_1 >= lowerLimit && dist_1 <= upperLimit){ 
    volume = (dist_1- lowerLimit)*100/(upperLimit - lowerLimit); // convert distance to volume scale
    Serial.println(volume);
  }
  //range detect for the other two sensors
  else{
    if(dist_2 >= lowerLimit && dist_2 <= upperLimit){ 
      Serial.print('2'); // hand pass
    }
    else Serial.print('3'); // no hand pass
    Serial.print('0');
    if(dist_3 >= lowerLimit && dist_3 <= upperLimit){
      Serial.println('2'); // hand pass
    }
    else Serial.println('3'); // no hand pass
  }
  
  delay(10);
}
