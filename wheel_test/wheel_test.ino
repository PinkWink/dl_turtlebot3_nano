/*
 * Simaple Dynamixel Test
 * by PinkWink
 * http://pinkwink.kr/
 */

#include <DynamixelWorkbench.h>

#define BAUDRATE            57600
#define BAUDRATE_TO_DXL     1000000
#define LEFT_ID             1
#define RIGHT_ID            2
 
DynamixelWorkbench dxl_wb;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(BAUDRATE);

    dxl_wb.begin("", BAUDRATE_TO_DXL);
    dxl_wb.ping(LEFT_ID);
    dxl_wb.ping(RIGHT_ID);

    dxl_wb.wheelMode(LEFT_ID);
    dxl_wb.wheelMode(RIGHT_ID);
}

void loop() {
    if(Serial.available()){
        String inString = Serial.readStringUntil('\n');
        int sepPosition = inString.indexOf(",");
        int length_inString = inString.length();

        String forward_cmd = inString.substring(0, sepPosition);
        String rotational_cmd = inString.substring(sepPosition+1, length_inString);

        int left_wheel_speed = forward_cmd.toInt() - rotational_cmd.toInt()*0.5;
        int right_wheel_speed = forward_cmd.toInt() + rotational_cmd.toInt()*0.5;

        //Serial.println("-- start");
        //Serial.println(left_wheel_speed);
        //Serial.println(right_wheel_speed);

        // put your main code here, to run repeatedly:
        dxl_wb.goalVelocity(LEFT_ID, left_wheel_speed);
        dxl_wb.goalVelocity(RIGHT_ID, right_wheel_speed);
    }
    
}
