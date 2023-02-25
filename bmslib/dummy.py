"""
This is code for a dummy BMS wich doesn't physically exist.

"""
import time

import math
from threading import Thread
from typing import Callable, Union

from .bms import BmsSample
from .bt import BtBms
from .util import get_logger


class DummyBt(BtBms):
    def __init__(self, address, **kwargs):
        super().__init__(address, **kwargs)
        self._switches = dict(charge=True, discharge=True)
        self._t0 = time.time()

    async def connect(self, **kwargs):
        pass

    async def disconnect(self):
        pass

    async def fetch(self) -> BmsSample:
        sample = BmsSample(
            voltage=12 - math.sin(time.time() / 4) * .5,
            current=math.sin(time.time() / 4),
            charge=50,
            capacity=100,
            num_cycles=3,
            temperatures=[21],
            switches=self._switches,
            uptime=(time.time() - self._t0)
        )
        return sample

    async def fetch_voltages(self):
        return [3000, 3001, 3002, 3003]

    async def set_switch(self, switch: str, state: bool):
        self.logger.info('set_switch %s %s', switch, state)
        assert isinstance(state, bool)
        self._switches[switch] = state


class BleakDummyClient():
    def __init__(self, address, disconnected_callback):
        self.address = address
        self._connected = False
        self._disconnected_callback = disconnected_callback
        self._bms = JKDummy()

    @property
    def is_connected(self):
        return self._connected

    async def connect(self, timeout):
        assert not self._connected
        self._connected = True

    async def disconnect(self):
        assert self._connected
        self._connected = False
        cb = self._disconnected_callback
        cb and cb(self)

    async def _connect_with_scanner(self):
        raise NotImplementedError()

    async def start_notify(self, char_specifier, callback: Callable[[int, bytearray], None]):
        return self._bms.start_notify(char_specifier, callback)

    async def write_gatt_char(self, char_specifier, data: Union[bytes, bytearray, memoryview], response: bool = False, ):
        return self._bms.write_gatt_char(char_specifier, data, response)


class JKDummy():
    DEVICE_INFO = b'U\xaa\xeb\x90\x03\x15JK-B2A24S20P\x00\x00\x00\x0010.X-W\x00\x0010.02\x00\x00\x00\xdc\xc6/\x00\x06\x00\x00\x00JK pw123456\x00\x00\x00\x00\x001234\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00220606\x00\x001120303218\x000000\x00Input Userdata\x00\x00123456\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc5\xaaU\x90\xeb\xc8\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00D'
    MSGS = [
        b'U\xaa\xeb\x90\x01\xd3X\x02\x00\x00(\n\x00\x00Z\n\x00\x00\xac\r\x00\x00\x16\r\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc4\t\x00\x00\xa0\x86\x01\x00\x1e\x00\x00\x00<\x00\x00\x00\xc0\xd4\x01\x00,\x01\x00\x00<\x00\x00\x00<\x00\x00\x00\xd0\x07\x00\x00\xa4\x01\x00\x00\x90\x01\x00\x00\xa4\x01\x00\x00\x90\x01\x00\x00\x00\x00\x00\x002\x00\x00\x00\x84\x03\x00\x00\xbc\x02\x00\x00\x08\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x0082\x04\x00\xdc\x05\x00\x00\xb8\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x83\xaaU\x90\xeb\xc8\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00D',
        b'U\xaa\xeb\x90\x02\xb9"\r$\r%\r*\r$\r"\r%\r"\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00$\r\x08\x00\x03\x016\x005\x004\x005\x004\x004\x005\x004\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1fi\x00\x00v\x04\x05\x00\xbb/\x00\x00\x0c\x01\xf8\x00\x1b\x01\x00\x00\x00\x00\x00A,\xc3\x02\x0082\x04\x00\x00\x00\x00\x00\x9dV\x00\x00d\x00\xa8\x02\x00\xfd/\x00\x01\x01\xd2\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x01\x00\x00\x00C\x048\x00\x00\x00\xf4\xaaA@\x00\x00\x00\x00\xe2\x04\xd40\x00\x00\x00\x01\x00\x05\x00\x00#)\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00='
    ]
    def __init__(self):
        self._callbacks = {}
        self.logger = get_logger()

    def start_notify(self, char_specifier, callback: Callable[[int, bytearray], None]):
        self._callbacks[char_specifier] = callback

    def write_gatt_char(self, char_specifier, data: Union[bytes, bytearray, memoryview], response: bool = False, ):
        crc = data[-1]
        data = bytes(data[:-1])
        from bmslib.jikong import calc_crc
        assert calc_crc(data) == crc

        if data.startswith(b'\xaaU\x90\xeb\x97'):
            # device info
            self.logger.info('dummy query device info')
            self._callbacks['0000ffe1-0000-1000-8000-00805f9b34fb'](self, bytes(self.DEVICE_INFO))
        elif data.startswith(b'\xaaU\x90\xeb\x96'):
            self.logger.info('dummy subscribe')
            def send_data():
                while True:
                    time.sleep(1)
                    for msg in self.MSGS:
                        self._callbacks['0000ffe1-0000-1000-8000-00805f9b34fb'](self, bytes(msg))

            Thread(target=send_data, daemon=True).start()
        else:
            raise Exception("dummy received unrecognized msg %s" % data)

