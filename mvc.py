#!/usr/bin/python3

from depthcharge import Console, Depthcharge,log,memory
import time, logging

# Flash Partition Info
UBOOT_START = 0x2000
TRUST_START = 0x4000
ROOTFS_START = 0x9800
USERDATA_START = 0x31E00
BLOCK_SIZE = 0x200

# We use this addess for scratch space in RAM (it usually contains the flattened device tree)
TARGET_RAM_ADDR = 0x61700000

'''
console_setup
This is used to set up the console for Depthcharge
'''
def console_setup():
    console=Console("/dev/ttyS0",baudrate=115200)
    ctx = Depthcharge(console,arch="arm")
    return ctx

def mvcWrapper(ctx,cmd,timeout=10):
    count=0
    resp = ctx.send_command(cmd)
    log.info(resp)
    resp = ctx.console.readline(update_monitor=True)
    while("OK" not in resp and count !=timeout):
        time.sleep(1)
        count += 1
        resp = ctx.console.readline(update_monitor=True)
    if "OK" not in resp:
        log.warning("OK not received, consider increasing timeout")
    return resp

'''
usb_setup
This script is used to enumerate and set up the USB port
'''
def usb_setup(ctx,reset=False):
    resps = []
    if not reset:
        resp = ctx.send_command("usb start")
    else:
        resp = ctx.send_command("usb reset")
    time.sleep(5)
    resps.append(resp)
    resp = ctx.send_command("usb storage")
    resps.append(resp)
    resp = ctx.send_command("usb dev 0")
    resps.append(resp)
    return resps

def rksfc_read(ctx,dest_addr,src_addr,size):
    cmd = f"rksfc read  0x{dest_addr:02x} 0x{src_addr:02x} 0x{size:02x}"
    resp = mvcWrapper(ctx,cmd,timeout=20)
    return resp

def rksfc_write(ctx,dest_addr,src_addr,size):
    cmd = f"rksfc write 0x{dest_addr:02x} 0x{src_addr:02x} 0x{size:02x}"
    resp = mvcWrapper(ctx,cmd)
    return resp

def usb_raw_write(ctx,source_addr,block,size):
    cmd = f"usb write 0x{source_addr:x} 0x{block:x} 0x{size:x}"
    resp = mvcWrapper(ctx,cmd,timeout=20)
    return resp

def usb_raw_read(ctx,source_addr,block,size):
    cmd = f"usb read 0x{source_addr:x} 0x{block:x} 0x{size:x}"
    resp = mvcWrapper(ctx,cmd)
    return resp


if __name__ == "__main__":
    log.info("Marvel Super Heroes Deptcharge Test...")
    ctx = console_setup()
    usb_setup(ctx,reset=False)
    rksfc_read(ctx,TARGET_RAM_ADDR,0,0x35E00)
    log.info("Flash read into RAM")
    usb_raw_write(ctx,TARGET_RAM_ADDR,0,0x35E00)
    log.info("Flash written to USB")
