from ev3dev2.motor import MoveSteering, MediumMotor, OUTPUT_D, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import UltrasonicSensor
from time import sleep
from ev3dev2.sensor.lego import GyroSensor
import os


'''每转一个角度停止，进行一次记录'''
def create_circle_map_1():
    motor_pair = MoveSteering(OUTPUT_B,OUTPUT_D)
    medium_motor = MediumMotor(OUTPUT_C)
    ultrasonic_sensor = UltrasonicSensor()
    with open('test.txt', 'w') as f:
        i=36
        while i>0:
            medium_motor.on_for_degrees(10,degrees=10)
            dis = ultrasonic_sensor.distance_centimeters
            f.write(str(dis)+'   ')
            i=i-1
        f.write("\n")
        while i<36:
            medium_motor.on_for_degrees(-10,degrees=10)
            dis = ultrasonic_sensor.distance_centimeters
            f.write(str(dis)+'   ')
            i=i+1


'''
    多进程程版本
    创建子进程运行超声波传感器转动
    父进程进行读取数据并记录操作
'''
def create_circle_map_2():
    dis_list = []
    motor_pair = MoveSteering(OUTPUT_B, OUTPUT_D)
    medium_motor = MediumMotor(OUTPUT_C)
    ultrasonic_sensor = UltrasonicSensor()
    pid=os.fork()
    if pid==0:
        medium_motor.on_for_degrees(-10, degrees=360)
    else:
        dis = 0
        new_dis = ultrasonic_sensor.distance_centimeters_continuous
        while new_dis != dis:
            dis_list.append(dis)
            dis = new_dis
            new_dis = ultrasonic_sensor.distance_centimeters_continuous
        print(dis_list)
        print('finish')


'''超声波传感器一直转动，连续记录36次距离值，停止'''
'''但是需要调整参数使得每次正好可以转360度或者是一个已知度数，否则不能和之前数据进行融合'''
def create_circle_map_3(): 
    dis_list = []
    motor_pair = MoveSteering(OUTPUT_B, OUTPUT_D)
    medium_motor = MediumMotor(OUTPUT_C)
    ultrasonic_sensor = UltrasonicSensor()
    dis = -1
    i=0
    while i<36:
        medium_motor.on(5,brake=True,block=False)
        dis=ultrasonic_sensor.distance_centimeters_continuous
        dis_list.append(dis)
        i=i+1
        sleep(0.01)
    medium_motor.stop()
    print(dis_list)
    print('finish')


'''
 每转一个角度停止，进行一次记录
    第一个方法的改进版
'''
def create_circle_map_4():
    motor_pair = MoveSteering(OUTPUT_B,OUTPUT_D)
    medium_motor = MediumMotor(OUTPUT_C)
    ultrasonic_sensor = UltrasonicSensor()
    dis_list_1=[]
    dis_list_2=[]
    dis_list_3=[]
    i=18
    while i>0:
        medium_motor.on_for_degrees(15,degrees=10)
        dis = ultrasonic_sensor.distance_centimeters
        dis_list_1.append(dis)
        i=i-1
    while i<36:
        medium_motor.on_for_degrees(-15,degrees=10)
        dis = ultrasonic_sensor.distance_centimeters
        dis_list_2.append(dis)
        i=i+1
    i=18
    while i>0:
        medium_motor.on_for_degrees(15,degrees=10)
        dis = ultrasonic_sensor.distance_centimeters
        dis_list_3.append(dis)
        i=i-1
    with open('test.txt', 'w') as f:
        for k in dis_list_1:
            f.write(str(k)+'\t')
        f.write('\n')
        for k in dis_list_2:
            f.write(str(k)+'\t')
        f.write('\n')
        for k in dis_list_3:
            f.write(str(k)+'\t')
        f.write('\n')

def test_method():
    # create_circle_map_1()
    # create_circle_map_2()
    # create_circle_map_3()
    create_circle_map_4()
        
test_method()