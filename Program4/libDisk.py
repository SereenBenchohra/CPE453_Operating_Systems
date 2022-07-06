# CPE453 Program 4 - TinyFS and Disk emulator
# Damien Trunkey, Danveer Cheema, Sereen Benchohra



import sys
import os
import pickle
# global variables
BLOCKSIZE = 256
# MAGICNUMBER = 0x5A
# fileSystems = []
# dynamicResourceTable = []
# fileDesc = 0


def openDisk(filename, nBytes):
    fd = 0
    # File doesnt exist. Return error
    if nBytes < 0:
        return -1
    # do nothing. file is already open
    if nBytes == 0:
        return
    try:
        # |os.O_EXCL
        fd = os.open(filename, os.O_RDWR|os.O_CREAT|os.O_TRUNC)
    except:
        return -1
    return fd


# readBlock() reads an entire block of BLOCKSIZE bytes from the open disk (identified by ‘disk’) and copies the result into a local buffer (must be at least of BLOCKSIZE bytes). 
# The bNum is a logical block number, which must be translated into a byte offset within the disk. 
# The translation from logical to physical block is straightforward: bNum=0 is the very first byte of the file. 
# bNum=1 is BLOCKSIZE bytes into the disk, bNum=n is n*BLOCKSIZE bytes into the disk. 
# On success, it returns 0. Errors must be returned if ‘disk’ is not available (i.e. hasn’t been opened) or for any other failures, as defined by your own error code system.

def readBlock(disk, bNum, block):
    offset = bNum * BLOCKSIZE
    try:
        os.lseek(disk, offset, 0)
    except:
        print("File either does not exist or hasnt been opened")
        return -1
    block[0] = os.read(disk, BLOCKSIZE)
    return 0


# In[4]:


# writeBlock() takes disk number ‘disk’ and logical block number ‘bNum’ and writes the content of the buffer ‘block’ to that location. 
# BLOCKSIZE bytes will be written from ‘block’ regardless of its actual size. The disk must be open. Just as in readBlock(), 
# writeBlock() must translate the logical block bNum to the correct byte position in the file. 
# On success, it returns 0. Errors must be returned if ‘disk’ is not available (i.e. hasn’t been opened) 
# or for any other failures, as defined by your own error code system.

def writeBlock(disk, bNum, block):
    offset = bNum * BLOCKSIZE
    try:
        os.lseek(disk, offset, 0)
    except:
        print("File either does not exist or hasnt been opened")
        return -1
    os.write(disk, block)
    return 0


# In[5]:


# closeDisk() takes a disk number ‘disk’ and makes the disk closed to further I/O; i.e. any subsequent reads or writes to a closed disk should return an error. 
# Closing a disk should also close the underlying file, committing any writes being buffered by the real OS.

def closeDisk(disk):
    try:
        os.close(disk)
    except:
        print("File either does not exist or hasnt been opened")
        return -1







