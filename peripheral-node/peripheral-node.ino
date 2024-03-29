/*
    This code is a fork of pubsubclient.
    Find the original code at:
    https://github.com/knolleary/pubsubclient/blob/master/examples/mqtt_esp8266/mqtt_esp8266.ino
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <NewPing.h>

////////////////////////////////////////

const char* DEVICE_NAME = "NODE-ARD-AMESTERDAM";
const char* DEVICE_SENSOR_TYPE = "Light";
bool IS_SENSORD_DIGITAL = true;

const char* MQTT_SERVER = "";
int MQTT_PORT = 8883;
const char* MQTT_USERNAME = "";
const char* MQTT_PASSWORD = "";

const char* NETWORK_SSID = "Amu";
const char* NETWORK_PASSWORD = "amuamuamu";

///////////////////////////////////////

//#define TRIGGER_PIN 11
//#define ECHO_PIN 8
//#define MAX_DISTANCE 200

//NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

#define SENSOR_PIN 0

///////////////////////////////////////

bool DEVICE_TESTMODE_ACTIVE = false;
const char* DEVICE_TESTMODE_ACTIVE_STR = "false";
float DEVICE_SEND_INTERVAL = 1;
bool DEVICE_ACTIVESELF = true;
const char* DEVICE_ACTIVESELF_STR = "true";
const char* DEVICE_OLD_NAME = "-";
bool deviceNameChanged = false;
bool deviceActiveselfChanged = false;
bool deviceMustIntroduce = false;
bool deviceTestModeActiveChanged = false;
bool deviceSendIntervalChanged = false;

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


////////////////////////////////////////

WiFiClientSecure espClient;
//WiFiClient espClient;
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

  if (deviceNameChanged || deviceActiveselfChanged || deviceMustIntroduce || deviceTestModeActiveChanged || deviceSendIntervalChanged)
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
  pinMode(BUILTIN_LED, OUTPUT);
  Serial.begin(115200);

  //espClient.setFingerprint(fingerprint);
  espClient.setInsecure();

  // connect to the internet and the server
  setup_wifi();

  // setup MQTT stuff
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
}

void handleSetupState()
{
  bool next_state_is_pause = false;

  // set the next state
  if (deviceActiveselfChanged)
  {
    if (!DEVICE_ACTIVESELF)
      next_state_is_pause = true;
    deviceActiveselfChanged = false;
  }

  if (deviceNameChanged) {
    deviceNameChanged = false;
  }

  if (deviceMustIntroduce)
    deviceMustIntroduce = false;
  if (deviceTestModeActiveChanged)
    deviceTestModeActiveChanged = false;
  if (deviceSendIntervalChanged)
    deviceSendIntervalChanged = false;

  if (next_state_is_pause)
    state = PAUSE;
  else
    state = SENDING;



  // send the node_introduction command to ns/arduino_send
  String command = make_cmd__node_introduction();
  client.publish(topics[0], command.c_str());

  Serial.println(command);
  Serial.println("Sent the introduction command...");

  delay(DEVICE_SEND_INTERVAL * 1000);
}

void handleSendingState()
{

  float value = 0; // change thissssss

  if (!DEVICE_TESTMODE_ACTIVE)
  {
    //value = sonar.ping_cm();
    value = analogRead(SENSOR_PIN);
  }
  else
  {
    value = random(1000);
  }

  // publish value_share command

  String command = make_cmd__value_share(value);
  Serial.println(command);
  client.publish(topics[0], command.c_str());

  delay(DEVICE_SEND_INTERVAL * 1000);

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
    digitalWrite(BUILTIN_LED, LOW);
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

      Serial.println("connected...");

      for (int i = 0; i < NUM_TOPICS; i++)
        client.subscribe(topics[i]);

      Serial.println("Subscribed to topics...");

    } else {

      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");

      delay(5000);
    }
  }
}



// https://arduinojson.org/v6/assistant/

String make_cmd__value_share(float value)
{

  String res;
  StaticJsonDocument<96> doc;
  doc["cmd"] = "value_share";
  doc["device_name"] = DEVICE_NAME;
  doc["val"] = value;

  serializeJson(doc, res);

  return res;
}

String make_cmd__node_introduction()
{

  String res;
  StaticJsonDocument<192> doc;

  doc["cmd"] = "node_introduction";
  doc["device_name"] = DEVICE_NAME;
  doc["sensor_type"] = DEVICE_SENSOR_TYPE;
  doc["is_active"] = DEVICE_ACTIVESELF_STR;
  doc["old_name"] = DEVICE_OLD_NAME;
  doc["send_interval"] = DEVICE_SEND_INTERVAL;
  doc["is_test_mode_active"] = DEVICE_TESTMODE_ACTIVE_STR;

  serializeJson(doc, res);

  return res;
}


void decode_cmd(char* payload, int plength)
{
  StaticJsonDocument<48> doc;

  DeserializationError error = deserializeJson(doc, payload, plength);

  if (error) {
    //Serial.print(F("deserializeJson() failed: "));
    //Serial.println(error.f_str());
    Serial.println("Emtpy/invalid input cmd...");
    return;
  }

  const char* cmd = doc["cmd"];
  const char* device_name = doc["device_name"];
  String device_name_str(device_name);
  String cmd_str(cmd);


  if (cmd_str.equals("introduction_request"))
  {
    deviceMustIntroduce = true;
    return;
  }

  if (!device_name_str.equals(DEVICE_NAME))
    return;

  if (cmd_str.equals("value_share"))
  {
    return;
  }

  Serial.println("Recieved a command for this device...");

  if (cmd_str.equals("change_active_self"))
  {
    const char* activeself = doc["activeself"];
    String activeself_str(activeself);

    if ((activeself_str.equals("true") && DEVICE_ACTIVESELF == false) ||
        (activeself_str.equals("false") && DEVICE_ACTIVESELF == true))
    {
      if (activeself_str.equals("true"))
      {
        DEVICE_ACTIVESELF = true;
        DEVICE_ACTIVESELF_STR = "true";

        Serial.println("Device got enabled in the network...");
      }

      else if (activeself_str.equals("false"))
      {
        DEVICE_ACTIVESELF = false;
        DEVICE_ACTIVESELF_STR = "false";

        Serial.println("Device got disabled in the network...");
      }

      deviceActiveselfChanged = true;
    }

    else
    {
      Serial.println("Device was already in a state that the command mentioned. So no change...");
    }

  }

  else if (cmd_str.equals("change_name"))
  {
    const char* new_name = doc["new_name"];
    DEVICE_OLD_NAME = DEVICE_NAME;
    DEVICE_NAME = new_name;

    Serial.println("Device got a name change command...");

    deviceNameChanged = true;
  }

  else if (cmd_str.equals("change_test_mode_active"))
  {
    const char* isactive = doc["isactive"];
    String isactive_str(isactive);
    if ((isactive_str.equals("true") && DEVICE_TESTMODE_ACTIVE == false) ||
        (isactive_str.equals("false") && DEVICE_TESTMODE_ACTIVE == true))
    {
      if (isactive_str.equals("true"))
      {
        DEVICE_TESTMODE_ACTIVE = true;
        DEVICE_TESTMODE_ACTIVE_STR = "true";

        Serial.println("Device test mode enabled...");
      }

      else if (isactive_str.equals("false"))
      {
        DEVICE_TESTMODE_ACTIVE = false;
        DEVICE_TESTMODE_ACTIVE_STR = "false";

        Serial.println("Device test mode disabled...");
      }

      deviceTestModeActiveChanged = true;
    }

    else
    {
      Serial.println("Device was already in a state that the command mentioned. So no change...");
    }
  }

  else if (cmd_str.equals("change_send_interval"))
  {
    const char* interval = doc["interval"];
    String interval_str(interval);
    DEVICE_SEND_INTERVAL = interval_str.toFloat();
    deviceSendIntervalChanged = true;
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
