#include <ESP8266WiFi.h>

#include <ESP8266HTTPClient.h>

#include <SPI.h>

#include "MFRC522.h"



#define RST_PIN  5  // RST-PIN für RC522 - RFID - SPI - Modul GPIO5 

#define SS_PIN  4  // SDA-PIN für RC522 - RFID - SPI - Modul GPIO4 

#define CARD_ID_LENGTH 8 //Lenght of card id in hexadecimal representation



const char* chipID = "0000";



const char *ssid =  "Innopolis";     

const char *pass =  "Innopolis";





MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance



void setup() {

  Serial.begin(115200);    // Initialize serial communications

  delay(250);

  Serial.println(F("Booting...."));

  

  SPI.begin();           // Init SPI bus

  mfrc522.PCD_Init();    // Init MFRC522

  

  WiFi.begin(ssid, pass);

  

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");

  }

  if (WiFi.status() == WL_CONNECTED) {

    Serial.println(F("WiFi connected"));

  }

  

  Serial.println(F("Ready!"));

  Serial.println(F("======================================================")); 

  Serial.println(F("Scan for Card and print UID:"));

}



void loop() { 

  // Look for new cards

  if ( ! mfrc522.PICC_IsNewCardPresent()) {

    delay(50);

    return;

  }

  // Select one of the cards

  if ( ! mfrc522.PICC_ReadCardSerial()) {

    delay(50);

    return;

  }

  

  HTTPClient http;
  
  http.begin("http://10.90.137.97:5000/print/");

  http.addHeader("Content-Type", "application/json"); 



  char* str = prepare_POST_str( mfrc522.uid.uidByte, mfrc522.uid.size, chipID);

  int httpCode = http.POST(str);

  free(str);   

  

  switch(httpCode){

    case HTTPC_ERROR_CONNECTION_REFUSED: break;

    case HTTPC_ERROR_SEND_HEADER_FAILED: break;

    case HTTPC_ERROR_SEND_PAYLOAD_FAILED: break;

    case HTTPC_ERROR_NOT_CONNECTED: break;

    case HTTPC_ERROR_NO_STREAM: break;

    case HTTPC_ERROR_NO_HTTP_SERVER: break;

    case HTTPC_ERROR_TOO_LESS_RAM: break;

    case HTTPC_ERROR_ENCODING: break;

    case HTTPC_ERROR_STREAM_WRITE: break;

    case HTTPC_ERROR_READ_TIMEOUT: break;

    default: break;
  }

    

  

  http.end();

  // Show some details of the PICC (that is: the tag/card)

  Serial.print(F("Card UID:"));

  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);

  Serial.println();



  if(((WiFi.status() != WL_CONNECTED))) WiFi.begin(ssid, pass);



}



// Helper routine to dump a byte array as hex values to Serial

void dump_byte_array(byte *buffer, byte bufferSize) {

  for (byte i = 0; i < bufferSize; i++) {

 

    Serial.print(buffer[i] < 0x10 ? " 0" : " ");

    Serial.print(buffer[i], HEX);

  }

}



char* prepare_POST_str(byte* cardID, byte cardIDSize, const char* chipID){

  char* str = (char*) malloc(45); //12 for ""card_id":"", 8 for cardID and, 14 for ", 'reader_id':", 4 for chipID; 

  char* k = "{\"card_id\": \"";  //auxiliary variable;

  memcpy(str, k, 13);

  char* cardIDStr = byte_to_string(cardID, cardIDSize);

  memcpy(str + 13, cardIDStr, CARD_ID_LENGTH);

  free(cardIDStr);

  char* s = "\", \"reader_id\": \""; //auxiliary variable;

  memcpy(str + 21, s, 17);

  memcpy(str + 38, chipID, 4);

  str[42] = '\"';
  str[43] = '}';
  str[44] = '\0';

  return str;

}



char* byte_to_string(byte *buffer, byte bufferSize){

  char* str = (char*)malloc(2*bufferSize);

  byte index = 0;

  

  for(byte i = 0; i < bufferSize; i++){

    byte l = buffer[i] >> 4;

    byte r = buffer[i] % 16;

    if(l <= 9) str[index] = '0' + l;

    else str[index] = 'A' + l - 10;

    index++;



    if(r <= 9) str[index] = '0' + r;

    else str[index] = 'A' + r - 10;

    index++;

  }



  str[index] = '\0';



  return str;

}


