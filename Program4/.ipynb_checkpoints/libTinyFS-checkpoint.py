# CPE453 Program 4 - TinyFS and Disk emulator
# Damien Trunkey, Danveer Cheema, Sereen Benchohra



import sys
import os
import pickle
from libDisk import *
# global variables
BLOCKSIZE = 256
MAGICNUMBER = 0x5A
fileSystems = []
dynamicResourceTable = []
fileDesc = 0

class superBlock():
    magicNumber = 0
    freeBlocks = [None] * BLOCKSIZE
    def __init__(self, magicNumber, freeBlocks):
        self.magicNumber = magicNumber
        self.freeBlocks = freeBlocks


class Inode():
    name = None
    stats = None
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats


class dynamicResourceEntry():
    filePointer = 0
    blockIndex = 0
    fd = 0
    def __init__(self, filePointer, blockIndex, fd):
        self.filePointer = filePointer
        self.blockIndex = blockIndex
        self.fd = fd


# In[13]:


class fileSystem():
    fileName = None
    fd = 0
    mounted = None
    superBlock = None
    def __init__(self, fileName, fd, mounted, superBlock):
        self.fileName = fileName
        self.fd = fd
        self.mounted = mounted
        self.superBlock = superBlock


# In[14]:


# Makes an empty TinyFS file system of size nBytes on the file specified by ‘filename’. 
# This function should use the emulated disk library to open the specified file, and upon success, format the file to be mountable. 
# This includes initializing all data to 0x00, setting magic numbers, initializing and writing the superblock and other metadata, etc. 
# Must return a specified success/error code.

# pickle.dumps(<object>) turns a python object into a byte array so we can write it to a file
def tfs_mkfs(filename, nBytes):
    fd = openDisk(filename, nBytes)
    if fd < 0:
        print("File open error")
        return -1
    
    blocks = [None] * int(nBytes/BLOCKSIZE)
    sBlock = superBlock(MAGICNUMBER, blocks)
    if writeBlock(fd, 0, pickle.dumps(sBlock)) < 0:
        print("write error")
        return -1
    
    stats = os.fstat(fd)
    rootInode = Inode("/", stats)
    if writeBlock(fd, 1, pickle.dumps(rootInode)) < 0:
        print("write error")
        return -1
    
    fs = fileSystem(filename, fd, 0, sBlock)
    
    fileSystems.append(fs)
    return 0



# tfs_mount(char *filename) “mounts” a TinyFS file system located within ‘filename’. 
# tfs_unmount(void) “unmounts” the currently mounted file system. 
# As part of the mount operation, tfs_mount should verify the file system is the correct type. 
# Only one file system may be mounted at a time. 
# Use tfs_unmount to cleanly unmount the currently mounted file system. Must return a specified success/error code

def tfs_mount(filename):   
    tfs_unmount()
    for fs in fileSystems:
        if fs.fileName == filename:
            fs.mounted = 1
    return 0



def tfs_unmount():
    for file in fileSystems:
        # unmount
        if file.mounted == 1:
            file.mounted = 0
    return 0



# Opens a file for reading and writing on the currently mounted file system. 
# Creates a dynamic resource table entry for the file (the structure that tracks open files, the internal file pointer, etc.), 
# and returns a file descriptor (integer) that can be used to reference this file while the filesystem is mounted.
def tfs_open(name):
    global fileDesc
    currFileSystem = None
    fileIndex = 0
    for fs in fileSystems:
        if fs.mounted == 1:
            currFileSystem = fs
    for i in range(len(currFileSystem.superBlock.freeBlocks)):
        if currFileSystem.superBlock.freeBlocks[i] == None:
            fileIndex = i
    
    stats = os.fstat(currFileSystem.fd)
    inode = Inode(name, stats)
    currFileSystem.superBlock.freeBlocks[fileIndex] = inode
    if writeBlock(currFileSystem.fd, fileIndex, pickle.dumps(currFileSystem.superBlock)) < 0:
        print("write error")
        return -1
    fileDesc = fileDesc + 1
    dre = dynamicResourceEntry(0, fileIndex, fileDesc)
    dynamicResourceTable.append(dre)
    return fileDesc      


# Closes the file and removes dynamic resource table entry
def tfs_close(FD):
    for entry in dynamicResourceTable:
        if entry.fd == FD:
            dynamicResourceTable.remove(entry)



# Writes buffer ‘buffer’ of size ‘size’, which represents an entire file’s contents, 
# to the file described by ‘FD’. 
# Sets the file pointer to 0 (the start of file) when done. 
# Returns success/error codes.
def tfs_write(FD, buffer, size):
    for entry in dynamicResourceTable:
        if entry.fd == FD:
            blockIndex = entry.blockIndex
    for fs in fileSystems:
        if fs.mounted == 1:
            fs.superBlock.freeBlocks.append(str.encode(buffer))
            if writeBlock(fs.fd, blockIndex, pickle.dumps(fs.superBlock.freeBlocks)) < 0:
                print("write error")
                return -1


# deletes a file and marks its blocks as free on disk
def tfs_delete(FD):
    for entry in dynamicResourceTable:
        if entry.fd == FD:
             blockIndex = entry.blockIndex
    for fs in fileSystems:
        if fs.mounted == 1:
            fs.superBlock.freeBlocks[blockIndex] = None
            if writeBlock(fs.fd, blockIndex, pickle.dumps(fs.superBlock.freeBlocks)) < 0:
                print("write error")
                return -1




# reads one byte from the file and copies it to ‘buffer’, 
# using the current file pointer location and incrementing it by one upon success. 
# If the file pointer is already at the end of the file then tfs_readByte() 
# should return an error and not increment the file pointer
def tfs_readByte(FD, buffer):
    for entry in dynamicResourceTable:
        if entry.fd == FD:
            blockIndex = entry.blockIndex
            filePtr = entry.filePointer
            entry.filePointer += 1
    # get current mounted file system
    for file in fileSystems:
        # found mounted file system now we get a single byte and write to buffer
        if file.mounted == 1:
            # readBlock(FD, blockIndex, buffer) 
            buffer[0] = file.superBlock.freeBlocks[blockIndex+1][filePtr]




# change the file pointer location to offset (absolute). Returns success/error codes
def tfs_seek(FD, offset):
    for entry in dynamicResourceTable:
        if entry.fd == FD:
            entry.filePointer = offset



def tfs_rename(filename, fd):
    for entry in dynamicResourceTable:
        if entry.fd == fd:
            fileIndex = entry.blockIndex
    for file in fileSystems:
        # found mounted file system now we get a single byte and write to buffer
        if file.mounted == 1:
            # readBlock(FD, blockIndex, buffer) 
            inode = file.superBlock.freeBlocks[0]
            inode.name = filename
            file.superBlock.freeBlocks[0] = inode
            writeBlock(file.fd, fileIndex, pickle.dumps(file.superBlock))




def tfs_stat(fd):
    for entry in dynamicResourceTable:
        if entry.fd == fd:
            fileIndex = entry.blockIndex
    for file in fileSystems:
        # found mounted file system now we get a single byte and write to buffer
        if file.mounted == 1:
            # readBlock(FD, blockIndex, buffer) 
            inode = file.superBlock.freeBlocks[0]
            print(inode.stats)




