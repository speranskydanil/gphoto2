#!/usr/bin/env python3

import subprocess

def devices():
  return Device.all()

class Device:
  @staticmethod
  def _exec(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

  @staticmethod
  def raise_exception_if_not_installed():
    if not Device._exec('command -v gphoto2'): raise Exception('gPhoto2 is not installed')

  @classmethod
  def all(cls):
    cls.raise_exception_if_not_installed()

    description = cls._exec('gphoto2 --auto-detect | grep "usb"').strip()
    if not description: return []

    devices = []

    records = description.split('\n')

    for record in records:
      camera, port = record.split('usb:')
      camera, port = camera.strip(), 'usb:' + port.strip()
      devices.append(Device(camera, port))

    return sorted(devices)

  def __init__(self, camera, port):
    self.camera = camera
    self.port = port

  def capture(self, path):
    self.raise_exception_if_not_installed()

    cmd_tmpl = 'gphoto2 --quiet --camera "{0}" --port {1} --capture-image-and-download --filename "{2}"'
    cmd = cmd_tmpl.format(self.camera, self.port, path)
    self._exec(cmd)

  def __str__(self):
    return '{0} {1}'.format(self.camera, self.port)

  def __repr__(self):
    return 'Device("{0}", "{1}")'.format(self.camera, self.port)

  def __lt__(self, other):
    return self.port < other.port

  def __hash__(self):
    return hash((self.camera, self.port))

