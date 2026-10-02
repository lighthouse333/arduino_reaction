// Arduino 端：接收电脑命令，亮灯后测量用户按下按钮需要的时间。
// 通信约定：电脑发送 START 加换行，Arduino 返回 TIME:毫秒数 加换行。
const int ledPin = 8;     // LED 控制引脚，外接 LED 需要合适的限流电阻。
const int buttonPin = 2;  // 按钮接在此引脚与 GND 之间。

// setup() 在上电或复位后执行一次，负责初始化硬件。
void setup() {
  pinMode(ledPin, OUTPUT);
  // 内部上拉：按钮未按下时为 HIGH，按下接地后为 LOW。
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);  // 波特率必须与电脑端一致。
  // 读取 A0 作为伪随机数种子；A0 悬空时读数的波动可使等待时间有所变化。
  randomSeed(analogRead(A0));
}

// loop() 会被反复调用，这里等待电脑发来测试指令。
void loop() {
  if (Serial.available()) {
    // 读取一条命令，不包含末尾的换行符。
    String command = Serial.readStringUntil('\n');
    if (command == "START") {
      delay(1000);  // 固定准备时间，单位是毫秒。
      // 上限不包含在内，因此随机等待 1000～4999 毫秒。
      int waitTime = random(1000, 5000);
      delay(waitTime);

      digitalWrite(ledPin, HIGH);
      // millis() 返回程序启动后的毫秒数，先记下亮灯时刻。
      unsigned long startTime = millis();
      // 持续等待按钮按下。此处没有超时，也没有检测提前按下的情况。
      // 如果用户一直按住按钮，灯亮后就会立即结束，得到接近 0 的成绩。
      while (digitalRead(buttonPin) == HIGH) {
      }

      unsigned long reaction = millis() - startTime;
      digitalWrite(ledPin, LOW);
      Serial.print("TIME:");
      // println() 会追加换行，电脑端 readline() 就能读取完整的一行。
      Serial.println(reaction);
    }
  }
}
