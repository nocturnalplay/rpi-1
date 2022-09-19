const express = require("express")
const Websocket = require("ws");
const GPIO = require('onoff').Gpio;

const LED = new GPIO(26, 'out');
const MOTOR = new GPIO(19, 'out');


function SEND(event, msg,state) {
    return JSON.stringify({ event, msg ,state});
}

const app = express();
const wss = new Websocket.Server({ noServer: true });


app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"))

wss.on("connection", (ws, req) => {
    console.log("getting started process two");
    ws.send(SEND("connected", "[*]Connection Alive",1));
    console.log(LED.readSync());
    if (LED.readSync() == 1) {
        ws.send(SEND("LED", "[*]LED current state ...🏃‍♂️",1));
    } else {
        ws.send(SEND("LED", "[*]LED current state ...🚪",0));
    }
    ws.on("message", async (msg) => {
        const message = JSON.parse(msg);
        const data = message.value
        const event = message.event;
        switch (event) {
            case "LED": {
                LED.writeSync(parseInt(data));
                MOTOR.writeSync(parseInt(data));
                if (data !== "0") {
                    ws.send(SEND("LED", "[*]LED current state ...🏃‍♂️",1));
                } else {
                    ws.send(SEND("LED", "[*]LED current state ...🚪",0));
                }
                break
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
