/*
 * Firmware AOI PCB System
 * Placa: NextLabTech A1 (ATmega328PB)
 * Motor: Servo GoBilda (Continuous Rotation)
 * Senzor: HC-SR04 Ultrasonic
 */

#include <Servo.h>

// --- PINOUT ---
const int PIN_TRIG = 6;
const int PIN_ECHO = 7;
const int PIN_SERVO = 9;

Servo conveyorServo;

// --- CONFIGURARE VITEZĂ (Calibrare Servo Continuu) ---
// 1500 = STOP
// <1500 = Sens Invers
// >1500 = Sens Normal
const int SPEED_STOP = 1500;
const int SPEED_RUN  = 1600; // Ajustează 1600-1900 pentru viteza dorită

// --- VARIABILE SISTEM ---
bool isRunning = false;
bool obstacleDetected = false;
long lastSensorTime = 0;

void setup() {
  Serial.begin(9600);
  
  conveyorServo.attach(PIN_SERVO);
  conveyorServo.writeMicroseconds(SPEED_STOP);
  
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  
  Serial.println("SYSTEM_READY");
}

void loop() {
  // 1. Ascultăm comenzi de la Python (PC)
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'S') { // START
      isRunning = true;
      obstacleDetected = false;
      // Mic impuls să plece de pe loc dacă e blocat
      conveyorServo.writeMicroseconds(SPEED_RUN); 
    } 
    else if (cmd == 'O') { // STOP
      isRunning = false;
      conveyorServo.writeMicroseconds(SPEED_STOP);
    }
  }

  // 2. Verificăm Senzorul (Non-blocking, la 100ms)
  if (millis() - lastSensorTime > 100) {
    checkSensor();
    lastSensorTime = millis();
  }

  // 3. Control Motor
  if (isRunning && !obstacleDetected) {
    conveyorServo.writeMicroseconds(SPEED_RUN);
  } else {
    conveyorServo.writeMicroseconds(SPEED_STOP);
  }
}

void checkSensor() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  
  long duration = pulseIn(PIN_ECHO, HIGH, 5000); // Timeout mic
  int distance = duration * 0.034 / 2;

  if (duration == 0) return; // Eroare citire

  // Logică Oprire la PCB (< 6 cm)
  if (distance > 0 && distance < 6) {
    if (!obstacleDetected) {
      obstacleDetected = true;
      Serial.println("OBSTACOL"); // Anunțăm Python-ul
    }
  } else {
    // Dacă obstacolul a dispărut (ex: am luat piesa manual)
    if (obstacleDetected && distance > 10) { 
       obstacleDetected = false;
    }
  }
}