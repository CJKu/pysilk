import os

SilkAllProps = [
  ('silk.hw2vsync',       0),
  ('silk.vd',             0),
  ('silk.i.scope',        0),
  ('silk.c.scope',        0),
  ('silk.r.scope',        0),
  ('silk.r.scope.client', 0),
  ('silk.i.lat',          0),
  ('silk.c.lat',          0),
  ('silk.r.lat',          0),
  ('silk.ipc',            0),
  ('silk.vsync',          0),
  ('silk.timer.log',      0),
  ('silk.timer.log.raw',  0),
  ('silk.input.pos',      1),
  ('silk.scrollbar.hide', 0)
]

class SilkProperty(object):
  def __init__(self):
    pass

  def SetProps(self, props):
    for prop in props:
      self.SetProp(prop)

  def SetProp(self, prop):
    os.system('adb shell setprop ' + prop[0] + ' ' + str(prop[1]))

  def GetProps(self):
    os.system('adb shell getprop | grep silk')


if __name__ == '__main__':
  sp = SilkProperty()
  print('Set properities...');
  sp.SetProps(SilkProps)
  print('Set properities done');
  print('results:')
  sp.GetProps()
