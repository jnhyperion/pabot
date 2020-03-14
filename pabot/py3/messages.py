
import struct
import socket

REGISTER = 'register'
CLIENT = 'client'
WORKER = 'worker'
REQUEST = 'request'
CLOSE = 'close'
WORK = 'work'
INSTRUCTION = 'instruction'
COMMAND = 'cmd'
WORK_RESULT = 'rc'
LOG = 'log'
OUTPUT = 'output'

format = struct.Struct('!I')  # for messages up to 2**32 - 1 in length

def recvall(sock, length:int) -> bytes:
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return b''
        data += more
    return data

def get(sock) -> str:
    return str(get_bytes(sock), 'utf-8')

def put(sock, message):
    put_bytes(sock, bytes(message, 'utf-8'))

def put_bytes(sock, bytes_msg:bytes):
    sock.send(format.pack(len(bytes_msg)) + bytes_msg)

def get_bytes(sock) -> bytes:
    lendata = recvall(sock, format.size)
    if not lendata:
        return b''
    (length,) = format.unpack(lendata)
    return recvall(sock, length)