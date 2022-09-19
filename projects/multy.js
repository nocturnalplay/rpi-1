var Gpio = require('pigpio').Gpio;
console.log('Define each color from RGB Strip light.');
//For each color you need to specify on what GPIO pin is connected and that we will use in mode OUTPUT
var ledRed = new Gpio(4, {mode: Gpio.OUTPUT});
var ledGreen = new Gpio(17, {mode: Gpio.OUTPUT});
var ledBlue = new Gpio(27, {mode: Gpio.OUTPUT});
console.log('Power up the red color.');
//You can set a brightness value between 0 and 255 
//where 0 is off and 255 is maximum brightness
ledRed.pwmWrite(255);
console.log("Let's start other colors too");
ledGreen.pwmWrite(100);
ledBlue.pwmWrite(50);
//Stop the lights after 5 seconds
setTimeout(function(){
    console.log('Stop all colors after 5 seconds');
    ledRed.pwmWrite(0);
    ledGreen.pwmWrite(0);  
    ledBlue.pwmWrite(0);
}, 5000);