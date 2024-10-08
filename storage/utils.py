from enum import Enum


class CellType(Enum):
    STT = "SST"
    PCM = "PCM"
    FeFET = "FeFET"
    RRAM = "RRAM"
    SRAM = "SRAM"
    CTT = "CTT"

class OpTarget(Enum):
    ReadLatency = "ReadLatency"
    WriteLatency = "WriteLatency"
    ReadDynamicEnergy = "ReadDynamicEnergy"
    WriteDynamicEnergy = "WriteDynamicEnergy"
    ReadEDP = "ReadEDP"
    WriteEDP = "WriteEDP"
    LeakagePower = "LeakagePower"
    Area = "Area"
    Exploration = "Exploration"