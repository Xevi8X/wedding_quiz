#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

uint32_t code = 0;
const byte button_A = 0b0001;
const byte button_B = 0b0010;
const byte button_C = 0b0100;
const byte button_D = 0b1000;

#define CRC8_POLYNOMIAL 0x07

uint8_t calculate_crc8(uint16_t value) {
    uint8_t crc = 0x00;  // Initialize CRC
    for (int i = 15; i >= 0; i--) {  // Process each bit of the 16-bit value
        crc ^= ((value >> i) & 0x01) ? 0x80 : 0x00;  // Shift bit into CRC register
        
        // Check if the left-most bit is set
        if (crc & 0x80) {
            crc = (crc << 1) ^ CRC8_POLYNOMIAL;  // Shift and apply polynomial
        } else {
            crc <<= 1;  // Just shift if no polynomial division needed
        }
    }
    return crc;
}

void set_code(String command)
{
  uint16_t id = 1000 * (command[0] - '0')
    + 100 * (command[1] - '0')
    + 10 * (command[2] - '0')
    + 1 * (command[3] - '0');
  Serial.print("Remote ID: ");
  Serial.println(id);

  uint8_t button = 0;
  switch(command[5])
  {
    case 'A':
      button = button_A;
    break;
    case 'B':
      button = button_B;
    break;
    case 'C':
      button = button_C;
    break;
    case 'D':
      button = button_D;
    break;
  }
  Serial.print("Button: ");
  Serial.println(command[5]);

  uint16_t remote_id = id << 8 | button;
  uint32_t crc = calculate_crc8(remote_id);
  code = crc << 16 | remote_id;
}

void setup() {
  Serial.println("EV1527 Transmitter Starting...");

  mySwitch.enableTransmit(10);
  mySwitch.setRepeatTransmit(1);

  /* Format for protocol definitions:
  * {pulselength, Sync bit, "0" bit, "1" bit, invertedSignal}
  * 
  * pulselength: pulse length in microseconds, e.g. 350
  * Sync bit: {1, 31} means 1 high pulse and 31 low pulses
  *     (perceived as a 31*pulselength long pulse, total length of sync bit is
  *     32*pulselength microseconds), i.e:
  *      _
  *     | |_______________________________ (don't count the vertical bars)
  * "0" bit: waveform for a data bit of value "0", {1, 3} means 1 high pulse
  *     and 3 low pulses, total length (1+3)*pulselength, i.e:
  *      _
  *     | |___
  * "1" bit: waveform for a data bit of value "1", e.g. {3,1}:
  *      ___
  *     |   |_
  *
  * These are combined to form Tri-State bits when sending or receiving codes.
  */
  RCSwitch::Protocol p = { 75, {  7, 217 }, {  7,  19 }, {  19,  5 }, false };
  mySwitch.setProtocol(p);

  set_code("0000,A");
}

void loop() {
  mySwitch.send(code, 24);
  if(Serial.available() > 0)
  {
    set_code(Serial.readString());
  }
  else
  {
    delay(100);
  }
}
