import os
import socket

## FIND LOCAL IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()

## FIND OS INFO
os_info = os.uname().sysname

## IF OS IS LINUX OR MACOS
if os_info == "Darwin":
    pass
elif os_info == "Linux":
    pass
else:
    pass

sending_from  = input("From:\t")
sending_to = input("To:\t")
print()
send_what = input("What do u wanna send?: ")
send_where = input("Where do u wanna send?: ")
print()

print("Sending...")
if sending_from == "me":
    os.system(f"rsync -Pr {send_what.strip()} {sending_to}:{send_where.strip()}")
    
elif sending_to == "me":
    os.system(f"rsync -Pr {sending_from}:{send_what.strip()} {send_where.strip()}")
