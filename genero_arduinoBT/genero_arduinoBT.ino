#include "BluetoothSerial.h"
#include "esp_bt_device.h"
/* Check if Bluetooth configurations are enabled in the SDK */
/* If not, then you have to recompile the SDK */
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;

const int potPin = 34;

void printDeviceAddress() { 
  const uint8_t* point = esp_bt_dev_get_address();
  for (int i = 0; i < 6; i++) {
    char str[3];
    sprintf(str, "%02X", (int)point[i]);
    Serial.print(str);
 
    if (i < 5){
      Serial.print(":");
    }
  }
}

void setup() {
  pinMode(potPin, INPUT);
  Serial.begin(115200);
  
  SerialBT.begin("esp32_genero");
  Serial.println("Bluetooth Started! Ready to pair...");

  Serial.println("The device started, now you can pair it with bluetooth!");
  Serial.println("Device Name: esp32_genero");
  Serial.print("BT MAC: ");
  printDeviceAddress();
  Serial.println();
}

int signalRate = 0;

void loop() {
    signalRate = 0;
    signalRate += analogRead(potPin);
    SerialBT.println(signalRate);
    delay(20);
}
