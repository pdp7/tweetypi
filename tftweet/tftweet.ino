// Based  on Adafruit's:  https://github.com/adafruit/TFTLCD-Library/blob/master/examples/graphicstest/graphicstest.pde

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library

#define LCD_DELAY 5000

// The control pins for the LCD can be assigned to any digital or
// analog pins...but we'll use the analog pins as this allows us to
// double up the pins with the touch screen (see the TFT paint example).
#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0

#define LCD_RESET A4 // Can alternately just connect to Arduino's reset pin

// Assign human-readable names to some common 16-bit color values:
#define	BLACK   0x0000
#define	BLUE    0x001F
#define	RED     0xF800
#define	GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

Adafruit_TFTLCD tft;

void setup(void) {
  Serial.begin(9600);
  tft.reset();
  uint16_t identifier = tft.readID();
  tft.begin(identifier);
}

void loop(void) {
  tft.setRotation(1);
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.setTextSize(3);
  tft.setTextColor(GREEN);
  while(1) {
    if(Serial.available())
    {
      String content = "";
      char character = Serial.read();
      Serial.print(character);
      if(character=='\n') {
        delay(LCD_DELAY);
        tft.fillScreen(BLACK);  
        tft.setCursor(0, 0);
        tft.setTextSize(3);  
        tft.setTextColor(GREEN);
      } 
      else {
        content.concat(character);
        tft.print(content);        
      }
    }
  }
  delay(2000);
}    

