const express = require("express")
const Websocket = require("ws");
var g = require('onoff').Gpio; //include onoff to interact with the GPIO
var LED = new g(26, 'out');

var Gpio = require('pigpio').Gpio, //include pigpio to interact with the GPIO
  ledRed = new Gpio(4, { mode: Gpio.OUTPUT }), //use GPIO pin 4 as output for RED
  ledGreen = new Gpio(17, { mode: Gpio.OUTPUT }), //use GPIO pin 17 as output for GREEN
  ledBlue = new Gpio(27, { mode: Gpio.OUTPUT }), //use GPIO pin 27 as output for BLUE
  redRGB = 255, //set starting value of RED variable to off (0 for common cathode)
  greenRGB = 255, //set starting value of GREEN variable to off (0 for common cathode)
  blueRGB = 255; //set starting value of BLUE variable to off (0 for common cathode)

//RESET RGB LED
ledRed.digitalWrite(1); // Turn RED LED off
ledGreen.digitalWrite(1); // Turn GREEN LED off
ledBlue.digitalWrite(1); // Turn BLUE LED off

function SEND(event, msg) {
  return JSON.stringify({ event, msg });
}

const app = express();
const wss = new Websocket.Server({ noServer: true });


app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"))

wss.on("connection", (ws, req) => {
  console.log("getting started process two");
  ws.send(SEND("connected", "[*]Connection Alive"));

  ws.on("message", async (msg) => {
    const message = JSON.parse(msg);
    const data = message.value
    const event = message.event;
    switch (event) {
      case "LED": {
        LED.writeSync(parseInt(data));
        break
      }
      case "rgbLed": {
        redRGB=255-parseInt(data.red);
        greenRGB=255-parseInt(data.green);
        blueRGB=255-parseInt(data.blue);

        ledRed.pwmWrite(redRGB); //set RED LED to specified value
        ledGreen.pwmWrite(greenRGB); //set GREEN LED to specified value
        ledBlue.pwmWrite(blueRGB); //set BLUE LED to specified value
      }
    }
  })
})

const server = app.listen(9000, () => console.log('server is listening on port 9000'))

server.on('upgrade', (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, socket => {
    wss.emit('connection', socket, request);
  });
});
