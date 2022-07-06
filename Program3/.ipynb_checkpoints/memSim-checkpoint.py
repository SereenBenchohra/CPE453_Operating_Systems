# CPE 453 program2 Memory Simulator
# Damien Trunkey, Danveer Cheema, Sereen Benchohra

import sys, getopt

# Created a page class to pass around page number, frame number, and the actual frame
# easier. This was done so we didnt have to pass 5+ arguments to helper function calls
# and it makes more sense to use a structure to track these attributes
class Page():
    pageNum = 0
    frameNum = 0
    frame = None
    def __init__(self, pageNum, frameNum, frame):
        self.pageNum = pageNum
        self.frameNum = frameNum
        self.frame = frame


# Shifts the address right 8 bits to get the page number and uses the and bitwise operator to get the offset
def get_pagenum_offset(address):
    return (address >> 8), (address & 0xFF)


# reads from the backing store binary file in 256 byte chunks from the pageNum
def read_backing(pageNum):
    backingStore = open("./BACKING_STORE.bin", 'rb')
    backingStore.seek(256 * pageNum)
    return backingStore.read(256)


# iterates through the tlb to find if the page exists in it
# returns None if page isnt in tlb
def tlb_lookup(pageNum, tlb):
    length = len(tlb)
    for i in range(length):
        if tlb[i].pageNum == pageNum:
            return tlb[i]
    return None


# inserts a page at the 0th index into the tlb. Pops the last item (FIFO) if tlb is full 
def tlb_insert(page, tlb):
    if len(tlb) == 16:
        tlb.pop()
    tlb.insert(0, page)


# Iterates through the page table to see if the page exists. Returns None if not
# Has two different functionalities based on which PRA were using
def page_table_lookup(pageNum, pageTable, algorithm):
    length = len(pageTable)
    for i in range(length):
        if pageTable[i].pageNum == pageNum:
            # for LRU we treat the pageTable like a stack and move the most recently used item to the front
            # this way when we try and insert when physical memory is full, we just pop the last item
            # from the page table and that will the the least recently used one
            if algorithm == 'LRU':
                #print("here")
                page = pageTable.pop(i)
                pageTable.insert(0, page)
                return page
            elif algorithm == 'FIFO':
                return pageTable[i]
    return None


# inserts a page into the page table. If physical memory is full then we do the page replacement 
def page_table_insert(pageTable, numFrames, page):
    # physical memory is full, evict the last item and insert into the 0th index
    if len(pageTable) >= numFrames:
        lastPage = pageTable.pop()
        page.frameNum = lastPage.frameNum
        pageTable.insert(0, page)
    # physical memory isnt full so insert the page
    else:
        pageTable.insert(0, page)


def read_file(fileName):
    f = open(fileName, "r")
    addresses = []
    for line in f:
        line = line.strip('\n')
        addresses.append(int(line))
    f.close()
    return addresses


def main(argv):
    if len(argv) == 1:
        fileName = argv.pop(0)
        addresses = read_file(fileName)
        numFrames = 256
        algorithm = 'FIFO'
    elif len(argv) == 3:
        fileName = argv.pop(0)
        addresses = read_file(fileName)
        numFrames = int(argv.pop(0))
        algorithm = argv.pop(0)
    else:
        print('Usage: memSim <reference-sequence-file.txt> <FRAMES> <PRA>')
        sys.exit(1)               

    tlbHits = 0
    tlbMisses = 0
    pageFaults = 0

    pageTable = []
    TLB = []
    physicalMem = [None] * numFrames
    physicalIdx = 0
    page = None


    for address in addresses:
        # retreives the pagenumber and offset from the address
        pageNum, offset = get_pagenum_offset(address)

        # tlb lookup if theres pages in memory
        if physicalIdx > 0:
            page = tlb_lookup(pageNum, TLB)

        # tlb miss now we look in page table
        if page == None:
            tlbMisses += 1
            # Page table lookup if there are pages in memory
            if physicalIdx > 0:
                page = page_table_lookup(pageNum, pageTable, algorithm)

            # Handling page fault due to page not being in page table
            if page == None:
                pageFaults += 1
                frame = read_backing(pageNum)
                page = Page(pageNum, physicalIdx, frame)
                page_table_insert(pageTable, numFrames, page)
                physicalMem[page.frameNum] = frame
                physicalIdx += 1
            tlb_insert(page, TLB)
        else:
            tlbHits += 1
        # get the referenced byte and make it a signed int
        referencedByte = int(frame[offset])
        if referencedByte > 127:
            referencedByte -= 256
        # prints the address, byte referenced, frame number, and the frame itself translated to hex
        print("%d, %d, %d, \n%s" % (address, referencedByte, page.frameNum, page.frame.hex().upper()))

    # prints out the page stats
    print("Number of Translated Addresses =", len(addresses))
    print("Page Faults =", pageFaults)
    print("Page Fault Rate = {:.3f}".format((pageFaults/len(addresses))))
    print("TLB Hits =", tlbHits)
    print("TLB Misses =", tlbMisses)
    print("TLB Hit Rate = {:.3f}".format((tlbHits/(tlbHits + tlbMisses))))
if __name__ == "__main__":
    main(sys.argv[1:])


# In[ ]:




