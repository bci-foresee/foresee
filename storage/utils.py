from enum import Enum


class CellType(Enum):
    """
    Memory types supported for modeling
    """
    STT = "SST"
    PCM = "PCM"
    FeFET = "FeFET"
    RRAM = "RRAM"
    SRAM = "SRAM"
    CTT = "CTT"


class OpTarget(Enum):
    """
    Optimization targets for cell configuration
    (see NVSim documentation for further details)
    """
    ReadLatency = "ReadLatency"
    WriteLatency = "WriteLatency"
    ReadDynamicEnergy = "ReadDynamicEnergy"
    WriteDynamicEnergy = "WriteDynamicEnergy"
    ReadEDP = "ReadEDP"
    WriteEDP = "WriteEDP"
    LeakagePower = "LeakagePower"
    Area = "Area"
    Exploration = "Exploration"
