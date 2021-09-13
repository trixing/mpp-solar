import serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
print(ser)
print(ser.name)         # check which port was really used

# from https://github.com/Louisvdw/dbus-serialbattery/commit/e0fcad1fcb124ca8ae6589d0e5924e2e9c02e515#
cmd = b"\x4E\x57\x00\x13\x00\x00\x00\x00\x06\x03\x00\x00\x00\x00\x00\x00\x68\x00\x00\x01\x29"

ser.write(cmd)     # write a string
while True:
    ret = ser.read(100)
    for x in ret:
        print('%02x' % ord(x))
ser.close()
