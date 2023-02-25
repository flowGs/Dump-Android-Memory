from memory import *

def DumpMemory(pid: int, map: str, path: str) -> bool:
  try:
    map = GetSoMap(pid, map)
    off = map['end'] - map['start']
    dump = MemRead(pid, map['start'], off)
    with open(path, 'wb') as f:
      f.write(dump)
      f.close()
    return True
  except (NoneType, TypeError):
    return False

DumpMemory(GetPidOf('com.axlebolt.standoff2'), 'global-metadata.dat', '/data/local/tmp/dumped_global-metadata.dat')