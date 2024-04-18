import logging
from typing import Any

from givenergy_modbus_async.model import GivEnergyBaseModel
from givenergy_modbus_async.model.battery import Battery
from givenergy_modbus_async.model.inverter import Inverter, Model, Generation
from givenergy_modbus_async.model.register import HR, IR
from givenergy_modbus_async.model.register_cache import (
    RegisterCache,
)
from givenergy_modbus_async.pdu import (
    ClientIncomingMessage,
    NullResponse,
    ReadHoldingRegistersResponse,
    ReadInputRegistersResponse,
    TransparentResponse,
    WriteHoldingRegisterResponse,
)

_logger = logging.getLogger(__name__)


class Plant(GivEnergyBaseModel):
    """Representation of a complete GivEnergy plant."""

    register_caches: dict[int, RegisterCache] = {}
    additional_holding_registers: list[int] = []
    inverter_serial_number: str = ""
    data_adapter_serial_number: str = ""
    number_batteries: int = 0
    slave_address: int = 0x32

    class Config:  # noqa: D106
        allow_mutation = True
        frozen = False

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not self.register_caches:
            self.register_caches = {self.slave_address: RegisterCache()}

    def update(self, pdu: ClientIncomingMessage):
        """Update the Plant state from a PDU message."""
        if not isinstance(pdu, TransparentResponse):
            _logger.debug(f"Ignoring non-Transparent response {pdu}")
            return
        if isinstance(pdu, NullResponse):
            _logger.debug(f"Ignoring Null response {pdu}")
            return
        if pdu.error:
            _logger.debug(f"Ignoring error response {pdu}")
            return
        _logger.debug(f"Handling {pdu}")

        if pdu.slave_address in (0x11, 0x00):
            # rewrite cloud and mobile app responses to "normal" inverter address
            slave_address = self.slave_address
        else:
            slave_address = pdu.slave_address

        if slave_address not in self.register_caches:
            _logger.debug(
                f"First time encountering slave address 0x{slave_address:02x}"
            )
            self.register_caches[slave_address] = RegisterCache()

        self.inverter_serial_number = pdu.inverter_serial_number
        self.data_adapter_serial_number = pdu.data_adapter_serial_number

        if isinstance(pdu, ReadHoldingRegistersResponse):
            self.register_caches[slave_address].update(
                {HR(k): v for k, v in pdu.to_dict().items()}
            )
        elif isinstance(pdu, ReadInputRegistersResponse):
            self.register_caches[slave_address].update(
                {IR(k): v for k, v in pdu.to_dict().items()}
            )
        elif isinstance(pdu, WriteHoldingRegisterResponse):
            if pdu.register == 0:
                _logger.warning(f"Ignoring, likely corrupt: {pdu}")
            else:
                self.register_caches[slave_address].update(
                    {HR(pdu.register): pdu.value}
                )

    def detect_batteries(self) -> None:
        """Determine the number of batteries based on whether the register data is valid.

        Since we attempt to decode register data in the process, it's possible for an
        exception to be raised.
        """
        i = 0
        for i in range(6):
            try:
                assert Battery.from_orm(self.register_caches[i + 0x32]).is_valid()
            except (KeyError, AssertionError):
                break
        self.number_batteries = i


    @property
    def inverter(self) -> Inverter:
        """Return Inverter model for the Plant."""
        return Inverter.from_orm(self.register_caches[self.slave_address])

    @property
    def batteries(self) -> list[Battery]:
        """Return Battery models for the Plant."""
        return [
            Battery.from_orm(self.register_caches[i + self.slave_address])
            for i in range(self.number_batteries)
        ]

##try single battery for testing
#    @property
#    def batteries_test(self) -> list[Battery]:
#        """Return Battery models for the Plant."""
#        return Battery.from_orm(self.register_caches[self.slave_address])
        
