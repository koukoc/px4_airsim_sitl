from cmath import pi
import setup_path
import airsim
import time
import asyncio
import pymap3d as pm
from mavsdk import System



UDP_IP = "127.0.0.1"
# UDP_IP = "192.168.137.1" #standard ip udp (localhost)


data = 0 #artificial data
client = airsim.VehicleClient()
client.confirmConnection()
pose = client.simGetVehiclePose()



async def run():


    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:8080")
    await drone.telemetry.set_rate_attitude(500)
    await drone.telemetry.set_rate_position(500)
    asyncio.ensure_future(get_position(drone))
    asyncio.ensure_future(get_attitude(drone))


async def get_attitude(drone):
    while True:
        async for attitude in drone.telemetry.attitude_euler():
            roll = attitude.roll_deg
            pitch =  attitude.pitch_deg
            yaw = attitude.yaw_deg

            pose.orientation=airsim.to_quaternion(pitch*0.017453,roll*0.017453, yaw*0.017453) 
            # 0.017453 deg to rad
            client.simSetVehiclePose( pose, False )
            break
        # data = {
        #     "rollVal":roll,
        #     "pitchVal":pitch,
        #     "yawVal":yaw,
        # }
        # timeStamp = time.time()
        # for key,value in data.items():
        #     # print("HI I'm here")
        #     MESSAGE = "{},{},{}".format(key,value, timeStamp)
        #     print(MESSAGE)
        #     print('\n')


async def get_position(drone):
    lat0=23.963356
    lon0=120.334663
    alt0=0
    while True:
        async for position in drone.telemetry.position():
            altitude =  position.relative_altitude_m
            latitude =  position.latitude_deg
            longitude =  position.longitude_deg
            x,y,z=pm.geodetic2enu(latitude, longitude, altitude, lat0, lon0, alt0)
            pose.position = airsim.Vector3r(y, x, -z+0.2)
            client.simSetVehiclePose( pose, True )
            break
        # data = {
        #     "xVal":x,
        #     "yVal":y,
        #     "zVal":z,

        # }
        # timeStamp = time.time()

        # for key,value in data.items():
        #     # print("HI I'm here")
        #     MESSAGE = "{},{},{}".format(key,value, timeStamp)
        #     print(MESSAGE)
        #     print('\n')

# async def get_odometry(drone):
#     while True:
#         async for Odometryk in drone.telemetry.odometry():
#             # x_m =  Odometryk.position.x_m
#             # y_m =  Odometryk.position.y_m
#             # z_m = Odometryk.position.z_m
#             pose.position = airsim.Vector3r(10, 10, 10)
#             client.simSetVehiclePose( pose, False )
#             break
#         data = {
#             # "xbodyVal":x_m,
#             # "ybodyVal":y_m,
#             # "zbodyVal":z_m,
#         }
#         timeStamp = time.time()
#         for key,value in data.items():

#             MESSAGE = "{},{},{}".format(key,value, timeStamp)
#             print(MESSAGE)
#             print('\n')







if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()

