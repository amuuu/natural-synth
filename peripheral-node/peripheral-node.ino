/*
    This code is a fork of pubsubclient.
    Find the original code at:
    https://github.com/knolleary/pubsubclient/blob/master/examples/mqtt_esp8266/mqtt_esp8266.ino
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

////////////////////////////////////////

const char* DEVICE_NAME = "NODE-ARD-AMESTERDAM";
const char* DEVICE_SENSOR_TYPE = "Light";

const char* MQTT_SERVER = "broker.mqtt-dashboard.com";
int MQTT_PORT = 8884;
const char* MQTT_USERNAME = "";
const char* MQTT_PASSWORD = "";

const char* NETWORK_SSID = "........";
const char* NETWORK_PASSWORD = "........";

int SENDING_DELAY_MILLISEC = 300;

// don't touch these
bool DEVICE_ACTIVESELF = true;
bool DEVICE_ACTIVESELF_STR = "true";
const char* DEVICE_OLD_NAME = "-";
bool deviceNameChanged = false;
bool deviceActiveselfChanged = false;

////////////////////////////////////////


enum STATE {
  SETUP,
  SENDING,
  PAUSE
};

STATE state;
STATE prev_state;


////////////////////////////////////////

# define NUM_TOPICS (2)
const char* topics[NUM_TOPICS] = {"ns/arduino_send", "ns/arduino_change"};
const char* commands[NUM_TOPICS][2] = {{"value_share", "node_introduction"},
  {"change_active_self", "change_name"}
};



////////////////////////////////////////

WiFiClient espClient;
PubSubClient client (espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

////////////////////////////////////////


void setup()
{
  startup();
  state = SETUP;
}

void loop()
{
  // handle lost lost connection
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (deviceNameChanged || deviceActiveselfChanged)
    state = SETUP;

    
  
  if (state == SENDING)
    handleSendingState();
  else if (state == SETUP)
    handleSetupState();
  else if (state == PAUSE)
    handlePauseState();
}

void startup()
{
  // Initialize the device
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);

  // connect to the internet and the server
  setup_wifi();

  // setup MQTT stuff
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
}

void handleSetupState()
{

  // set the next state
  if (deviceNameChanged) {
    state = SENDING;
    deviceNameChanged = false;
  }
  else if (deviceActiveselfChanged)
  {
    state = PAUSE;
    deviceActiveselfChanged = false;
  }
  
  // send the node_introduction command to ns/arduino_send
  client.publish(topics[0], make_cmd__node_introduction());

  delay(SENDING_DELAY_MILLISEC); //////////////////// NOT SURE ABOUT THIS ONE YET
}

void handleSendingState()
{
  // read sensor data
  float value = 0; // change thissssss
  
  // publish value_share command
  client.publish(topics[0], make_cmd__value_share(value));
}


void handlePauseState()
{
  // do nothing here I guess???
}


////////////////////////////////////////


void setup_wifi()
{
  delay(10);

  WiFi.mode(WIFI_STA);
  WiFi.begin(NETWORK_SSID, NETWORK_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length)
{
  
  decode_cmd(castPayload(payload, length), length);

  if (topic == topics[1]) {
    digitalWrite(LED_BUILTIN, LOW);
  } else if (topic == topics[0]) {
    digitalWrite(LED_BUILTIN, HIGH);
  }

}

void reconnect()
{

  while (!client.connected()) {

    Serial.print("Attempting MQTT connection...");

    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD)) {

      Serial.println("connected");

      for (int i = 0; i < NUM_TOPICS; i++)
        client.subscribe(topics[i]);

    } else {

      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");

      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}



// https://arduinojson.org/v6/assistant/

const char* make_cmd__value_share(float value)
{

  String res;
  StaticJsonDocument<96> doc;
  doc["cmd"] = commands[0][0];
  doc["device_name"] = DEVICE_NAME;
  doc["val"] = value;
  
  serializeJson(doc, res);

  return res.c_str();
}

const char* make_cmd__node_introduction()
{

  String res;
  StaticJsonDocument<192> doc;
  
  doc["cmd"] = commands[0][1];
  doc["device_name"] = DEVICE_NAME;
  doc["sensor_type"] = DEVICE_SENSOR_TYPE;
  doc["is_active"] = DEVICE_ACTIVESELF_STR;
  doc["old_name"] = DEVICE_OLD_NAME;

  serializeJson(doc, res);
  
  return res.c_str();
}


void decode_cmd(char* payload, int plength)
{
  StaticJsonDocument<48> doc;
  
  DeserializationError error = deserializeJson(doc, payload, plength);
  
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return;
  }
  
  const char* cmd = doc["cmd"];
  const char* device_name = doc["device_name"];
  
  if (device_name != DEVICE_NAME)
    return;
  
  if (cmd == commands[1][0])
  {
    const char* activeself = doc["activeself"];
    
    if ((activeself=="true" && DEVICE_ACTIVESELF == false) || 
        (activeself=="false" && DEVICE_ACTIVESELF == true))
    {
      if(activeself=="true") DEVICE_ACTIVESELF = true;
      else if (activeself=="false") DEVICE_ACTIVESELF = false;      
      DEVICE_ACTIVESELF_STR = activeself;

      deviceActiveselfChanged = true;
    }
    
  }
  
  else if (cmd == commands[1][1])
  {
    const char* new_name = doc["new_name"];
    DEVICE_OLD_NAME = DEVICE_NAME;
    DEVICE_NAME = new_name;
    
    deviceNameChanged = true;
  }
}

char* castPayload(byte* payload, int plength)
{
  char* res = new char[plength];
  
  for (int i = 0; i < plength; i++)
  {
    res[i] = (char) payload[i];
  }
  
  return res;
}
