#include "DHT.h"

#define pin0 2
#define pin1 3
#define pin2 4
#define DHTTYPE DHT11

DHT dht0(pin0, DHTTYPE); //bed dht
DHT dht1(pin1, DHTTYPE); //front dht
DHT dht2(pin2, DHTTYPE); //back dht

void setup() {
  Serial.begin(9600);
  dht0.begin();
  dht1.begin();
  dht2.begin();  
}

void loop() {

 if (Serial.available() > 0){ //check communication status
  delay(2000);
  int temp0 = dht0.readTemperature();
  int temp1 = dht1.readTemperature();
  int temp2 = dht2.readTemperature();
  Serial.println(temp0);
  //Serial.println(temp1);
  //Serial.println(temp2);
  Serial.flush();
    
  }

}
