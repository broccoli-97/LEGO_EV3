from ev3dev2.motor import MoveSteering, MediumMotor, OUTPUT_D, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import UltrasonicSensor
from time import sleep
from ev3dev2.sensor.lego import GyroSensor
import os

motor_pair = MoveSteering(OUTPUT_B, OUTPUT_D)
gyro = GyroSensor()
gyro.mode = GyroSensor.MODE_GYRO_ANG
medium_motor = MediumMotor(OUTPUT_C)
ultrasonic_sensor = UltrasonicSensor()

matrix_map = [[0]*20 for i in range(20)]
# 记录某个坐标可否被访问
vis = [[0]*20 for i in range(20)]
# 定义四个方向
dire = [[0, 1],[1, 0], [0, -1], [-1, 0]]

# path = Stack()
# temp = Stack()
count = 0
# current_x = current_y = 10
is_obstacle = [0, 0, 0, 0]

# x,y为当前位置


'''
局部扫描函数4.0
每转一个角度停止，进行一次记录
第一个方法的改进版
'''


def create_circle_map_4(current_x, current_y, is_ob):
    #motor_pair = MoveSteering(OUTPUT_B, OUTPUT_D)
    # medium_motor = MediumMotor(OUTPUT_C)
    # ultrasonic_sensor = UltrasonicSensor()
    dis_list_1 = []
    dis_list_2 = []
    dis_list_3 = []
    i = 18
    while i > 0:
        medium_motor.on_for_degrees(15, degrees=10)
        dis = ultrasonic_sensor.distance_centimeters
        dis_list_1.append(dis)
        i = i-1
    while i < 36:
        medium_motor.on_for_degrees(-15, degrees=10)
        dis = ultrasonic_sensor.distance_centimeters
        dis_list_2.append(dis)
        i = i+1
    while i > 18:
        medium_motor.on_for_degrees(15, degrees=10)
        dis = ultrasonic_sensor.distance_centimeters
        dis_list_3.append(dis)
        i = i-1

    # if dis_list_2[7] > 250 or dis_list_2[8] > 250 or dis_list_2[9] > 250:
    if dis_list_2[8] > 250:
        is_ob[1] = 0
    else:
        is_ob[1] = 1

    # if dis_list_2[15] > 250 or dis_list_2[16] > 250 or dis_list_3[17] > 250:
    if dis_list_2[16] > 250:
        is_ob[0] = 0
    else:
        is_ob[0] = 1

    # if dis_list_3[0] > 250 or dis_list_3[1] > 250 or dis_list_2[0] > 250:
    if dis_list_2[0] > 250:
        is_ob[2] = 0
    else:
        is_ob[2] = 1

    # if dis_list_3[7] > 250 or dis_list_3[9] > 250 or dis_list_3[8] > 250:
    if  dis_list_3[8] > 250:
        is_ob[3] = 0
    else:
        is_ob[3] = 1

    with open('test.txt', 'a') as f:
        f.write(str(current_x)+','+str(current_y)+'\n')
        for k in dis_list_1:
            f.write(str(k)+'\t')
        f.write('\n')
        for k in dis_list_2:
            f.write(str(k)+'\t')
        f.write('\n')
        for k in dis_list_3:
            f.write(str(k)+'\t')
        f.write('\n')


def test_on_seconds():

    motor_pair.on_for_seconds(steering=0, speed=-50, seconds=8)


'''
行进函数，从current_x,current_y移动到next_x,next_y
'''


def move(current_x, current_y, next_x, next_y):
    if next_x-current_x < 0:
        # 逆时针转90度
        motor_pair.on(steering=100, speed=10)
        gyro.wait_until_angle_changed_by(90)

        # 走两米
        test_on_seconds()

    elif next_x-current_x > 0:
        # 顺时针转90度
        motor_pair.on(steering=-100, speed=10)
        gyro.wait_until_angle_changed_by(90)

        test_on_seconds()
    elif next_x-current_x == 0 and next_y-current_y > 0:
        # 直行
        test_on_seconds()
    elif next_x-current_x == 0 and next_y-current_y < 0:
        # 转180度
        motor_pair.on(steering=100, speed=10)
        gyro.wait_until_angle_changed_by(180)
        test_on_seconds()
    else:
        print("no way")


'''
返回进函数，从current_x,current_y移动到pre_x,pre_y
'''


def move_back(current_x, current_y, pre_x, pre_y):
    move(current_x, current_y, pre_x, pre_y)


'''
局部地图融合函数
'''


def map_union(map_list):
    pass


def dfs(x, y):
    if x < 0 or y < 0:
        return
    # current_x=x
    # current_y=y
    if vis[x][y] != 1:
        # 调用扫描方法，生成局部地图,生成一个是否有障碍物的标记数组
        create_circle_map_4(x, y, is_obstacle)
        vis[x][y] = 1
    for i in range(4):
        nx = x+dire[i][0]
        ny = y+dire[i][1]
        if is_obstacle[i] == 1:
            matrix_map[nx][ny] = -1
    for i in range(4):
        nx = x+dire[i][0]
        ny = y+dire[i][1]
        if nx >= 0 and ny >= 0 and matrix_map[nx][ny] == 0 and vis[nx][ny] == 0:
            # vis[nx][ny] = 1
            current_x = nx
            current_y = ny
            # 调用行进函数，使小车移动到指定位置
            # move(x,y)
            ##
            move(x, y, current_x, current_y)
            dfs(current_x, current_y)
            # 回溯
            # matrix_map[nx][ny]=-1
            # 调用返回函数，是小车移动到指定位置
            # move_back(x,y)
            move_back(current_x, current_y, x, y)


# def start():
#     count = 0
#     with open(filename, "w") as fp:

#         # 定义一个矩阵数组来代表二维地图
#         # 将地图划分为一个一个的格子，假设小车每次在格点上进行扫描
#         # 每次行走的半径为200cm
#         # 以matrix_map[10][10]为起始原点建立坐标系
#         # 最大可以扫描半径为20米的范围


def main():
    matrix_map = [[0]*20 for i in range(20)]
    # 记录某个坐标可否被访问
    vis = [[0]*20 for i in range(20)]
    # 定义四个方向
    dir = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # path = Stack()
    # temp = Stack()
    count = 0
    pre_x = pre_y = 0
    current_x = current_y = 10
    is_obstacle = [0, 0, 0, 0]

    # x,y为当前位置

    dfs(10, 10)


dfs(10, 10)
