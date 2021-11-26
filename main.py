import sys


class PageTableRow:
    def __init__(self):
        self.isPageValid = None
        self.accessPermissions = None
        self.frameNumber = None
        self.pageRecentlyUsed = None


class PageTable:
    def __init__(self, _numBitsInVirtualAddress, _numBitsInPhysicalAddress, _sizeOfPageBytes):
        self.numBitsInVirtualAddress = _numBitsInPhysicalAddress
        self.numBitsInPhysicalAddress = _numBitsInPhysicalAddress
        self.sizeOfPageBytes = _sizeOfPageBytes
        self.pageTableRowList = []


def readPageFileStart(file):
    startTargetVector = []

    pageNum = 0
    run = 0
    with open(file) as f:
        line = f.readline()
    line = line.strip()

    test = line.split()

    i = 0
    for num in test:
        startTargetVector.append(int(num))

    return startTargetVector


def readPageFileRows(file):
    pageTableRows = []

    f = open(file)

    next(f)

    for line in f:
        row = PageTableRow()
        line = line.split()
        if (len(line) != 0):
            row.isPageValid = int(line[0])
            row.accessPermissions = int(line[1])
            row.frameNumber = int(line[2])
            row.pageRecentlyUsed = int(line[3])
            pageTableRows.append(row)

    return pageTableRows


def binaryToDecimal(binary):
    binary = int(binary)
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def reverseStr(_str):
    return _str[::-1]


def hexToBinary(init_string):
    # Initialising hex string

    n = int(init_string, 16)
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    res = bStr

    return res


def getOffset(pageTable):
    _sizeOfPageBytes = pageTable.sizeOfPageBytes
    offset = 0
    if _sizeOfPageBytes > 0:
        while (_sizeOfPageBytes % 2 == 0):
            _sizeOfPageBytes /= 2
            offset = offset + 1
    return offset


def getNumberPages(pageTable, _offset):
    _numBitsVirtual = pageTable.numBitsInVirtualAddress
    intermediaryConv = _numBitsVirtual - _offset

    return pow(2, intermediaryConv)


def getNumberFrames(pageTable, _offset):
    _numBitsPhysical = pageTable.numBitsInPhysicalAddress
    intermediaryConv = _numBitsPhysical - _offset

    return pow(2, intermediaryConv)


def main():

    firstRow = readPageFileStart(sys.argv[1])

    newTable = PageTable(firstRow[1], firstRow[0], firstRow[2])

    pageTableRows = readPageFileRows(sys.argv[1])

    newTable.pageTableRowList = pageTableRows

    userInput = input("Enter a virtual address: ")

    while userInput != 'exit':
        bitOffset = getOffset(newTable)

        hexFind = "0x"

        choppedBinary = ''
        if hexFind in userInput:
            hexInput = ''
            print("Hex address entered...translating...")
            for i in range(2, len(userInput)):
                hexInput += userInput[i].lower()

            binaryString = hexToBinary(hexInput)

        else:
            binaryString = decimalToBinary(int(userInput))

        if (len(binaryString) < newTable.numBitsInVirtualAddress):
            numZerosPading = newTable.numBitsInVirtualAddress - len(binaryString)
            padding = ''
            for i in range(0, numZerosPading):
                padding += '0'

            binaryString = padding + binaryString

        elif (len(binaryString) > newTable.numBitsInVirtualAddress):
            for i in range(len(binaryString) - newTable.numBitsInVirtualAddress, len(binaryString)):
                choppedBinary += binaryString[i]

            binaryString = choppedBinary

        offsetBits = ''
        prependBits = ''

        for i in range(0, len(binaryString) - bitOffset):
            prependBits += binaryString[i]

        for i in range(len(binaryString) - bitOffset, len(binaryString)):
            offsetBits += binaryString[i]

        translatedPageIndex = binaryToDecimal(prependBits)
        if (newTable.pageTableRowList[translatedPageIndex].isPageValid == 0 and newTable.pageTableRowList[
            translatedPageIndex].accessPermissions != 0):
            print("DISK")
            exit(1)
        if (newTable.pageTableRowList[translatedPageIndex].isPageValid == 0 and newTable.pageTableRowList[
            translatedPageIndex].accessPermissions == 0):
            print("SEGFAULT")
            exit(1)

        frameNum = newTable.pageTableRowList[translatedPageIndex].frameNumber

        frameNumToBin = decimalToBinary(frameNum)

        physAddress = frameNumToBin + offsetBits

        decimalPhysAddress = binaryToDecimal(physAddress)

        print(decimalPhysAddress)

        userInput = input("Enter a virtual address: ")


main()
