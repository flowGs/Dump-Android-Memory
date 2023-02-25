import os

def GetPidOf(package: str) -> int:
  for pid in os.listdir('/proc'):
    try:
      with open(f'/proc/{pid}/cmdline', 'r') as f:
        if package in f.read():
          return int(pid)
        f.close()
    except (NotADirectoryError, FileNotFoundError):
      pass
  return None

def GetSoMap(pid: int, soname: str) -> dict:
  try:
    with open(f'/proc/{pid}/maps', 'r') as f:
      for line in f.readlines():
        if soname in line:
          info = line.split()
          return {'start': int(info[0].split('-')[0], 16), 'end': int(info[0].split('-')[1], 16), 'type': info[1], 'name': info[5].split('/')[-1]}
  except FileNotFoundError:
    pass
  return None

def MemRead(pid: int, address: int, size: int) -> bytes:
  try:
    with open(f'/proc/{pid}/mem', 'rb') as f:
      f.seek(address, 0)
      ret = f.read(size)
      f.close()
      return ret
  except FileNotFoundError:
    pass
  return None

def MemWrite(pid: int, address: int, value: bytes) -> bool:
  try:
    with open(f'/proc/{pid}/mem', 'wb') as f:
      f.seek(address, 0)
      f.write(value)
      f.close()
      return True
  except (FileNotFoundError, OSError) as e:
    pass
  return False