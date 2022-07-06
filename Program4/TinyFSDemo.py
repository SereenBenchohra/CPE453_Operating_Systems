
import os
import sys
from libTinyFS import *
# BLOCKSIZE = 256
# MAGICNUMBER = 0x5A
# fileSystems = []
# dynamicResourceTable = []
# fileDesc = 0


# In[8]:


def main():
    
    print("TEST FOR DISK FUNCTIONS\n")
    filename = "test.txt"
    bnum = 0
    fd = openDisk(filename, 256)
    writeB = str.encode("this is a test to see if this works")
    readB = [None]
    writeBlock(fd, 0, writeB)
    readBlock(fd, bnum, readB)
    print(readB[0])
    print('\n')
    
    
    print("TEST FOR TFS_MKFS\n")
    tfs_mkfs("test.txt", 256)
    f = open('test.txt', 'rb')
    print(f.readlines())
    print('\n')
    
    
    print("TEST FOR TFS_MOUNT\n")
    
    tfs_mount("test.txt")
    print(fileSystems[0].fileName, "Mounted (1 = yes, 0 = no)", fileSystems[0].mounted)
    print('\n')
    
    
    print("TEST FOR TFS_OPEN\n")
    fd = tfs_open("im_a_file")
    f = open('test.txt', 'rb')
    print(f.readlines())
    print(fd)
    print('\n')
    
    
    print("TEST FOR TFS_CLOSE\n")
    print(len(dynamicResourceTable))
    tfs_close(fd)
    print(len(dynamicResourceTable))
    print('\n')
    
    
    print("TEST FOR TFS_WRITE\n")
    fd = tfs_open("im_a_file")
    tfs_write(fd, "hello this is a test", 256)
    f = open('test.txt', 'rb')
    print(f.readlines())
    print('\n')
    
    
    print("TEST FOR TFS_DELETE\n")
    fd = tfs_open("im_a_file")
    tfs_delete(fd)
    f = open('test.txt', 'rb')
    print(f.readlines())
    print('\n')
    
    
    print("TEST FOR TFS_READBYTE\n")
    fd = tfs_open("im_a_file")
    buffer = [None]
    tfs_readByte(fd, buffer)
    print(chr(buffer[0]))
    print('\n')
    
    
    print("TEST FOR TFS_SEEK\n")
    fd = tfs_open("im_a_file")
    buffer = [None]
    tfs_seek(fd, 8)
    tfs_readByte(fd, buffer)
    print(chr(buffer[0]))
    print('\n')
    
    
    
#     print("TEST FOR TFS_STAT\n")
#     fd = tfs_open("im_a_file")
#     tfs_stat(fd)
#     print('\n')
    
    
#     print("TEST FOR TFS_RENAME\n")
#     fd = tfs_open("im_a_file")
#     f = open('test.txt', 'rb')
#     print(f.readlines())
#     tfs_rename("not_a_file", fd)
#     f = open('test.txt', 'rb')
#     print(f.readlines())
#     print('\n')
    
    
    print("TEST FOR TFS_UNMOUNT\n")
    tfs_unmount()
    print(fileSystems[0].fileName, "Mounted (1 = yes, 0 = no)", fileSystems[0].mounted)
    
if __name__ == "__main__":
    main()


# In[ ]:




