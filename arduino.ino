const int pinBuzzer = 7;
const int pinLED = 8;

char dato;

void setup() {
  Serial.begin(9600);
  pinMode(pinBuzzer, OUTPUT);
  pinMode(pinLED, OUTPUT);

  noTone(pinBuzzer);
  digitalWrite(pinLED, LOW);
}

void loop() {
  if (Serial.available()) {
    dato = Serial.read();

    if (dato == '0') {
      // 0 = CUCHILLO
      digitalWrite(pinLED, HIGH);

      tone(pinBuzzer, 300);   
      delay(30);              
      noTone(pinBuzzer);

    } else if (dato == '1') {
      // 1 = NO CUCHILLO
      digitalWrite(pinLED, LOW);
      noTone(pinBuzzer);
    }
  }
}
