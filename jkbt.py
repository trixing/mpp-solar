from bluepy import btle
import logging
from mppsolar.outputs import mqtt

from mppsolar.io.baseio import BaseIO
from mppsolar.helpers import get_kwargs
from mppsolar.io.jkbledelegate import jkBleDelegate
from mppsolar.io.jkbleio import JkBleIO
from mppsolar.protocols import jk02
import sys
import time

# btle.Debugging = True

log = logging.getLogger("JkBleIO")


def main():
  mac = '3C:A5:51:86:01:9C'
  if len(sys.argv) > 1:
      mac = sys.argv[1]
  root = logging.getLogger()
  root.setLevel(logging.INFO)

  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  root.addHandler(handler)


  j = JkBleIO(mac)

  protocol=jk02.jk02()
  j.ble_connect(mac, protocol=protocol)
  command = 'getCellData'
  full_command = protocol.get_full_command(command)
  raw_response = None
  try:
    raw_response = j.ble_get_data(full_command)
  finally:
    j.ble_disconnect()
  info_data = {}
  if j.info_record:
    p2=jk02.jk02()
    p2.get_full_command('getInfo')
    info_data = p2.decode(j.info_record, 'getInfo')
  if not raw_response:
    log.error('Invalid Response')
    return False
  data = protocol.decode(raw_response, command)
  if data['Battery_Voltage'][0] < 40:
    log.error('Invalid Battery Voltage')
    return False
  if data['Battery_Voltage'][0] > 100:
    log.error('Invalid Battery Voltage')
    return False
  data.update(info_data)
  del data['raw_response']
  for k, v in data.copy().items():
    # print(k, v[0])
    if k.startswith('Unknown'):
      del data[k]
  log.info(data)
  m = mqtt.mqtt()
  m.output(data=data, tag='jkbms')
  return True


if not main():
    sys.exit(1)
