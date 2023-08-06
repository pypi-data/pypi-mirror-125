import io
import random
import time
from threading import Lock
from uuid import UUID

__uuid_v6_max_seq = 0x3FFF
__uuid_v6_seq = random.randrange(0, __uuid_v6_max_seq)
__uuid_v6_mutex = Lock()


def __uuid_v6_clk_seq():
    global __uuid_v6_mutex
    global __uuid_v6_seq
    __uuid_v6_mutex.acquire()
    try:
        __uuid_v6_seq += 1
        if __uuid_v6_seq >= __uuid_v6_max_seq:
            __uuid_v6_seq = 0
        return __uuid_v6_seq | 0x8000
    finally:
        __uuid_v6_mutex.release()


def __uuid_v6_time(timestamp):
    timestamp -= 12219305144  # timestamp of 1582-Oct-15
    time_high = timestamp & 0xFFFF_FFFF_FFFF_0000
    time_low = ((timestamp & 0x0000_0000_0000_FFFF) >> 4) | 0x6000
    return time_high | time_low


def uuid6() -> UUID:
    """Generate a sequential time-based UUID."""
    data = io.BytesIO()
    now = time.time_ns()
    data.write(__uuid_v6_time(now).to_bytes(8, "big"))
    data.write(__uuid_v6_clk_seq().to_bytes(2, "big"))
    data.write(random.randbytes(6))
    data.seek(0)
    return UUID(bytes=data.read())
