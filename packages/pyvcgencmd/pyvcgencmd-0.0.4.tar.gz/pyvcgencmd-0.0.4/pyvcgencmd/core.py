import shlex
import subprocess
from typing import List, Dict, Union
import psutil

from .utils import check_disk_usage


def run_cmd(cmd: str) -> str:
    args = shlex.split(cmd)
    args.insert(0, "vcgencmd")
    out = (
        subprocess.check_output(args, stderr=subprocess.PIPE).decode("utf-8").strip()
    )
    return out


def camera() -> List[int]:
    cmd = "get_camera"
    out = run_cmd(cmd)
    out = out.split(" ")
    out = list(filter(None, out))
    out = [int(each.split("=")[1]) for each in out]
    return out


def state() -> str:
    cmd = "get_throttled"
    out = run_cmd(cmd)
    out = out.split("=")[1]
    return out


def temperature() -> float:
    cmd = "measure_temp"
    out = run_cmd(cmd)
    out = out.split("=")[1].split("'")[0]
    return float(out)


def arm_clock() -> int:
    cmd = "measure_clock arm"
    out = run_cmd(cmd)
    out = out.split("=")[1]
    return int(out)


def core_clock() -> int:
    cmd = "measure_clock core"
    out = run_cmd(cmd)
    out = out.split("=")[1]
    return int(out)


def serial_clock() -> int:
    cmd = "measure_clock uart"
    out = run_cmd(cmd)
    out = out.split("=")[1]
    return int(out)


def storage_clock() -> int:
    cmd = "measure_clock emmc"
    out = run_cmd(cmd)
    out = out.split("=")[1]
    return int(out)


def voltage() -> float:
    cmd = "measure_volts"
    out = run_cmd(cmd)
    out = out.split("=")[1].replace("V", "")
    return float(out)


def otp() -> Dict[str, bytes]:
    cmd = "otp_dump"
    out = run_cmd(cmd)
    out = out.split("\n")
    out = {(each.split(":"))[0]: ("0x" + (each.split(":"))[1]) for each in out}
    return out


def cpu_memory() -> int:
    cmd = "get_mem arm"
    out = run_cmd(cmd)
    out = out.split("=")[1].replace("M", "")
    return int(out)


def gpu_memory() -> int:
    cmd = "get_mem gpu"
    out = run_cmd(cmd)
    out = out.split("=")[1].replace("M", "")
    return int(out)


def config() -> Dict[str, Union[bytes, int]]:
    cmd = "get_config int"
    out = run_cmd(cmd)
    out = out.split("\n")
    out = {(each.split("="))[0]: (each.split("="))[1] for each in out}
    return out


# external
def space():
    mid: tuple = check_disk_usage()
    return dict(mid._asdict())


def memory():
    mid: tuple = psutil.virtual_memory()
    return dict(mid._asdict())
