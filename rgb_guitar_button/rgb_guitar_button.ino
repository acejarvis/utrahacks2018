#define WHITE 255, 255, 255
#define RED 255, 0, 0
#define ORANGE 255, 165, 0
#define YELLOW 255, 255, 0
#define GREEN 0, 255, 0
#define CYAN 0, 255, 255
#define BLUE 0, 0, 255
#define MAGENTA 255, 0, 255

#define LED_DELAY_MS 1000

#define BRIGHTNESS 1.00

const int button = 2;
const int rgb_red = 9;
const int rgb_green = 10;
const int rgb_blue = 11;
const int speaker = 14;

void setup()
{
  pinMode(button, INPUT_PULLUP);
  pinMode(rgb_red, OUTPUT);
  pinMode(rgb_green, OUTPUT);
  pinMode(rgb_blue, OUTPUT);
  pinMode(speaker, OUTPUT);

  Serial.begin(9600);
  Serial.write("Begun communications");
}

void loop()
{
  setRGB(WHITE, BRIGHTNESS); 
  delay(LED_DELAY_MS);
  setRGB(RED, BRIGHTNESS);
  Serial.println("red");
  delay(LED_DELAY_MS);
  setRGB(ORANGE, BRIGHTNESS);
  delay(LED_DELAY_MS);
  setRGB(YELLOW, BRIGHTNESS);
  delay(LED_DELAY_MS);  
  setRGB(GREEN, BRIGHTNESS);
  Serial.println("green");
  delay(LED_DELAY_MS);
  setRGB(CYAN, BRIGHTNESS);
  delay(LED_DELAY_MS);
  setRGB(BLUE, BRIGHTNESS);
  Serial.println("blue");
  delay(LED_DELAY_MS);
  setRGB(MAGENTA, BRIGHTNESS);
  delay(LED_DELAY_MS);
  
  // button wired one end to the pin, other end to GND
  // HIGH when open, LOW when closed
  // therefore, DO STUFF when HIGH (guitar taken out)
  // because normally closed (guitar in stand)
//  if(digitalRead(button))
//  {
//    // make sure the guitar has been taken out fully
//    sleep(LED_DELAY_MS, BRIGHTNESS);
//    if(digitalRead(button))
//    {
//      playRiff();
//    }
//  }
}

void playRiff()
{
  Serial.write("play riff");
}

void setRGB(int red_value, int green_value, int blue_value, double brightness)
{
  analogWrite(rgb_red*brightness, red_value);
  analogWrite(rgb_green*brightness, green_value);
  analogWrite(rgb_blue*brightness, blue_value);
}


