#include "FastLED.h"
 
// How many leds in your strip?
#define NUM_LEDS 4
 
// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 2
#define CLOCK_PIN 3
 
#define COLOR_ORDER RGB
 
// Adalight sends a "Magic Word" (defined in /etc/boblight.conf) before sending the pixel data
uint8_t prefix[] = {'A', 'd', 'a'}, hi, lo, chk, i;
 
// Baudrate, higher rate allows faster refresh rate and more LEDs (defined in /etc/boblight.conf)
#define serialRate 115200
 
// Define the array of leds
CRGB leds[NUM_LEDS];
 
void setup() {

       FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RBG>(leds, NUM_LEDS);
     
        // initial RGB flash
        LEDS.showColor(CRGB(5, 0, 0));
        delay(500);
        LEDS.showColor(CRGB(0, 5, 0));
        delay(500);
        LEDS.showColor(CRGB(0, 0, 5));
        delay(500);
        LEDS.showColor(CRGB(0, 0, 0));
       
        Serial.begin(serialRate); 
}
 
void loop() {
  //LEDS.showColor(CRGB(5, 0, 0));
  memset(leds, 0, NUM_LEDS * sizeof(struct CRGB));
  // read the transmission data and set LED values
  //while(Serial.available());
  
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    uint8_t r, g, b;    
    while(!Serial.available());
    r = Serial.read();
    while(!Serial.available());
    g = Serial.read();
    while(!Serial.available());
    b = Serial.read();
    leds[i].r = r;
    leds[i].g = g;
    leds[i].b = b;
  }
  //LEDS.showColor(CRGB(0, 0, 200));
  //delay(500);
  // shows new values
  FastLED.show();
}
