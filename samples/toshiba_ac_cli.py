#!/usr/bin/env python3
import argparse
import asyncio
import os
#from toshiba_ac.device import ToshibaAC
from toshiba_ac.device.properties import (
    ToshibaAcAirPureIon,
    ToshibaAcFanMode,
    ToshibaAcMeritA,
    ToshibaAcMeritB,
    ToshibaAcMode,
    ToshibaAcPowerSelection,
    ToshibaAcStatus,
    ToshibaAcSwingMode,
)
from toshiba_ac.device_manager import ToshibaAcDeviceManager

async def func(args):
    device_manager = ToshibaAcDeviceManager(user, password,"3e6e4eb5f0e5aa40") 
    print(f"Connecting...{user} ")
    await device_manager.connect()
    print("Connected")
    devices = await device_manager.get_devices()


    for device in devices:
        if(device.name == args.device): 
            #status at the end if defined 
            if args.status:
                print(f"Device: {device.name}")
                print(f"Power: {device.ac_status.name}")
                print(f"Mode: {device.ac_mode.name}")
                print(f"Fan Mode: {device.ac_fan_mode.name}")
                print(f"Swing Mode: {device.ac_swing_mode.name}")
                print(f"Power Selection: {device.ac_power_selection.name}")
                print(f"Merit A: {device.ac_merit_a.name}")
                print(f"Merit B: {device.ac_merit_b.name}")
                print(f"Air Pure Ion: {device.ac_air_pure_ion.name}")
                print(f"Temperature: {device.ac_temperature} °C")
            #temp
            if hasattr(args, 'temp') and args.temp is not None: 
                 print(f"Setting temp {args.temp} for device: {device.name}")
                 await device.set_ac_temperature(args.temp)
            #mode
            if hasattr(args, 'mode')  and args.mode in ["cool", "heat", "auto", "dry", "fan"]:
                 print(f"Setting mode {args.mode} for device: {device.name}")
                 await device.set_ac_mode(ToshibaAcMode[args.mode.upper()])
            #fan
            if hasattr(args, 'fan')  and args.fan in ["auto", "low", "medium", "high"]:
                 print(f"Setting fan mode {args.fan} for device: {device.name}")
                 await device.set_ac_fan_mode(ToshibaAcFanMode[args.fan.upper()])
            #power
            if hasattr(args, 'power') and args.power in ["on", "off"]:
                 print(f"Setting power  {args.power} for device: {device.name}")
                 await device.set_ac_status(ToshibaAcStatus[args.power.upper()])
            break;
    await device_manager.shutdown()

args = None; 
user = os.getenv("TOSHIBA_USER") 
password = os.getenv("TOSHIBA_PASS")

class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

def main():
    parser = argparse.ArgumentParser(description="CLI for Toshiba AC")

    parser.add_argument("device", help="Device name to adress")
    parser.add_argument("--power", choices=["on", "off"], help="Switches on / Off the device")
    parser.add_argument("--temp", type=float, help="Sets the target temperature (for example  22.5 °C)")
    parser.add_argument("--mode", choices=["cool", "heat", "auto", "dry", "fan"], help="sets the operation mode")
    parser.add_argument("--fan", choices=["auto", "low", "medium", "high"], help="sets the fan mode")
    parser.add_argument("--status", action="store_true", help="prints information about the current state of the device")
    args = parser.parse_args()    

    if not user or not password: 
        print("Error: TOSHIBA_USER and TOSHIBA_PASS environment variables must be set")
        return

    loop = asyncio.new_event_loop()
    loop.run_until_complete(func(args))
    loop.close()

    
if __name__ == "__main__":
    main()
