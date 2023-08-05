# python core imports
from typing import Dict, List, Union, Optional
from datetime import datetime

# to check space and memory
from . import core

# pydantic imports
from pydantic import BaseModel

"""

camera          get_camera
state           get_throttled
temperature     measure_temp
arm_clock       measure_clock arm
core_clock      measure_clock core
serial_clock    measure_clock uart
storage_clock   measure_clock emmc
voltage         measure_volts
otp             otp_dump
cpu_memory      get_mem arm
gpu_memory      get_mem gpu
config          get_config [config|int|str]
---------------------------------------
space
memory

"""


class Camera(BaseModel):
    supported: int
    detected: int


class State(BaseModel):
    throttled: bytes


class Temperature(BaseModel):
    temperature: float


class ArmClock(BaseModel):
    arm_clock: int


class CoreClock(BaseModel):
    core_clock: int


class SerialClock(BaseModel):
    serial_clock: int


class StorageClock(BaseModel):
    storage_clock: int


class Voltage(BaseModel):
    voltage: float


class Otp(BaseModel):
    otp: Dict[str, bytes]


class CpuMemory(BaseModel):
    cpu_memory: int


class GpuMemory(BaseModel):
    gpu_memory: int


class Config(BaseModel):
    config: Dict[str, Union[bytes, int]]


class Space(BaseModel):
    total: int
    used: int
    free: int


class Memory(BaseModel):
    total: int
    available: int
    percent: float
    used: int
    free: int


class VcmdSchemaBase(BaseModel):
    updated: datetime = datetime.utcnow()
    camera: List[int] = core.camera()
    state: bytes = core.state()
    temperature: float = core.temperature()
    arm_clock: int = core.arm_clock()
    core_clock: int = core.core_clock()
    serial_clock: int = core.serial_clock()
    storage_clock: int = core.storage_clock()
    voltage: float = core.voltage()
    otp: Dict[str, bytes] = core.otp()
    cpu_memory: int = core.cpu_memory()
    gpu_memory: int = core.gpu_memory()
    config: Dict[str, Union[bytes, int]] = core.config()
    space: Dict[str, int] = core.space()
    memory: Dict[str, Union[int, float]] = core.memory()


class VcmdSchema(VcmdSchemaBase):
    id: Optional[int]

    class Config:
        orm_mode = True
