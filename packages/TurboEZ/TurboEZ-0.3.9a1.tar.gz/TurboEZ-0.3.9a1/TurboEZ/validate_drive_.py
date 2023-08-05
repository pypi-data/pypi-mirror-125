import socket

def valid_addr(addr):
    try:
        socket.inet_pton(socket.AF_INET, addr)
        return True
    except socket.error:
        return False

def valid_addr6(addr):
    try:
        socket.inet_pton(socket.AF_INET6, addr)
        return True
    except socket.error:
        return False


def valid_addr_mask(addr_mask):
     if len(addr_mask.split('/')) != 2:
         return False

     addr, mask = addr_mask.split('/')
     if int(mask) < 1 or int(mask) > 31:
         print('Mask should be between [1-31]')
         return False

     try:
         socket.inet_pton(socket.AF_INET, addr)
         return True
     except socket.error:
         return False


def valid_addr6_mask(addr_mask):
     if len(addr_mask.split('/')) != 2:
         return False

     addr, mask = addr_mask.split('/')
     if int(mask) < 1 or int(mask) > 128:
         print('Mask should be between [1-128]')
         return False

     try:
         socket.inet_pton(socket.AF_INET6, addr)
         return True
     except socket.error:
         return False
