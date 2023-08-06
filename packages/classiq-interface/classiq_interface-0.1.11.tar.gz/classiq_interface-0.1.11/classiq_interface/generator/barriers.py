import pydantic

from classiq_interface.generator.circuit_outline import Cycle, Qubit


class SingleRegisterBarrier(pydantic.BaseModel):
    cycle: Cycle


class SingleQubitBarrier(pydantic.BaseModel):
    qubit: Qubit
    cycle: Cycle
