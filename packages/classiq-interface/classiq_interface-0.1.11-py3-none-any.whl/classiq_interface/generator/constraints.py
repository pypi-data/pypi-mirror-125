from collections import defaultdict
from typing import Dict, List, Optional, Union

import networkx as nx
import pydantic

import classiq_interface.generator.validations.flow_graph as flow_graph
from classiq_interface.generator.barriers import (
    SingleQubitBarrier,
    SingleRegisterBarrier,
)
from classiq_interface.generator.classical_if import Cif
from classiq_interface.generator.custom_functions.custom_function import CustomFunction
from classiq_interface.generator.custom_functions.custom_function_library_data import (
    CustomFunctionLibraryData,
)
from classiq_interface.generator.custom_gates import CustomGate, ValidGateName
from classiq_interface.generator.entanglers import (
    CXSlideEntangler,
    PhaseCXSlideEntangler,
)
from classiq_interface.generator.function_call import FunctionCall
from classiq_interface.generator.measurements import Measurement
from classiq_interface.generator.phase_estimation import PhaseEstimation
from classiq_interface.generator.preferences.optimization import Optimization
from classiq_interface.generator.preferences.randomness import create_random_seed
from classiq_interface.generator.qiskit_quantum_gates import QiskitBuiltinQuantumGates
from classiq_interface.generator.range_types import NonNegativeIntRange
from classiq_interface.generator.result import QuantumFormat
from classiq_interface.generator.sat_problem import SatProblem
from classiq_interface.generator.slides import PhaseSlide
from classiq_interface.generator.teleport import Teleport
from classiq_interface.generator.transpilation import TranspilationPreferences

DEFAULT_MINIMAL_DEPTH = 1
CYCLE_ERROR_MSG = "Inputs and outputs cannot form a cycle"


# TODO define a type that can be used in variable declaration that is consistent with usage
def normalize_dict_key_to_str(d):
    return {k.name: v for k, v in d.items()}


class QuantumCircuitConstraints(pydantic.BaseModel):
    """
    Input constraints for the generated quantum circuit.
    """

    # TODO: Consider moving timeout outside of constraints, and supply it (optionally) separate of the constraints.
    # TODO: Remove hard coded timeout when issue,https://github.com/MiniZinc/minizinc-python/pull/8 is resolved
    timeout_seconds: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=300, description="Generation timeout in seconds"
    )
    qubit_count: pydantic.PositiveInt = pydantic.Field(
        default=...,
        description="Number of qubits in generated quantum circuit",
    )
    min_depth: pydantic.PositiveInt = DEFAULT_MINIMAL_DEPTH
    max_depth: pydantic.PositiveInt
    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the generation",
    )
    gate_count_constraints: Dict[
        QiskitBuiltinQuantumGates, NonNegativeIntRange
    ] = pydantic.Field(default_factory=lambda: defaultdict(NonNegativeIntRange))
    custom_gate: Optional[Dict[ValidGateName, CustomGate]] = None
    cx_slide_entangler: Optional[CXSlideEntangler] = None
    phase_cx_slide_entangler: Optional[PhaseCXSlideEntangler] = None
    phase_slide: Optional[PhaseSlide] = None
    # Must be validated before logic_flow
    custom_function_library_data: Optional[CustomFunctionLibraryData] = pydantic.Field(
        default=None,
        description="The user-defined custom function library.",
    )
    logic_flow: List[FunctionCall] = pydantic.Field(
        default_factory=list,
        description="List of function calls to be applied in the circuit",
    )
    combine_segments: bool = pydantic.Field(
        default=False,
        description="If set to true, all segments will be combined into one"
        "segment. The way they are connected and the qubit assignment "
        "will be set deterministically, without using the CSP model.",
    )
    allowed_gates: List[QiskitBuiltinQuantumGates] = pydantic.Field(
        default_factory=list
    )
    phase_estimation: Optional[PhaseEstimation] = None
    teleport: Optional[Teleport] = None
    optimization: Optional[Optimization] = pydantic.Field(default_factory=Optimization)
    single_measurements: List[Measurement] = pydantic.Field(default_factory=list)
    register_barriers: List[SingleRegisterBarrier] = pydantic.Field(
        default_factory=list
    )
    qubit_barriers: List[SingleQubitBarrier] = pydantic.Field(default_factory=list)
    single_cifs: List[Cif] = pydantic.Field(default_factory=list)
    sat_problem: Optional[SatProblem] = None
    two_qubits_gate_count: NonNegativeIntRange = pydantic.Field(
        default_factory=NonNegativeIntRange
    )
    transpilation: Optional[TranspilationPreferences] = pydantic.Field(
        default_factory=TranspilationPreferences
    )
    segment_qubit_count: bool = pydantic.Field(
        default=False,
        description="If set to True, the number of qubits will"
        " be determined by the width of the single"
        " segment in the circuit",
    )
    output_format: Union[
        QuantumFormat,
        pydantic.conlist(
            item_type=QuantumFormat,
            min_items=1,
            max_items=len(QuantumFormat),
        ),
    ] = pydantic.Field(
        default=[QuantumFormat.QASM],
        description="The quantum circuit output format(s). "
        "When multiple formats are requested, only the first one will be presented. "
        "Note that generating the `ll` format (Microsoft QIR) takes an extra time.",
    )
    use_synthesis_engine: bool = True

    _gate_count_constraints = pydantic.validator(
        "gate_count_constraints", allow_reuse=True
    )(normalize_dict_key_to_str)

    draw_as_functions: bool = pydantic.Field(
        default=False,
        description="If true, the generation output will be "
        "visualized as functions and not as an unrolled circuit",
    )

    class Config:
        extra = "forbid"

    @pydantic.validator("max_depth")
    def validate_max_depth(cls, max_depth, values):
        min_depth = values.get("min_depth")
        if min_depth and max_depth < min_depth:
            raise ValueError("max_depth must be greater or equal to min_depth")

        return max_depth

    @pydantic.validator("allowed_gates")
    def normalize_list_key_to_str(cls, use_gate):
        return [v.name for v in use_gate]

    @pydantic.validator("logic_flow")
    def validate_logic_flow(cls, logic_flow: List[FunctionCall], values):
        if not logic_flow:
            return logic_flow

        library: CustomFunctionLibraryData = values.get("custom_function_library_data")
        for function_call in logic_flow:
            params = function_call.function_params
            if isinstance(params, CustomFunction):
                params.validate_custom_function_in_library(library=library)
                function_data = library.custom_functions_dict[params.name]
                params.generate_io_names(
                    input_set=function_data.input_set,
                    output_set=function_data.output_set,
                )
                function_call.validate_custom_function_io()

        graph = flow_graph.create_flow_graph(logic_flow)

        if not nx.algorithms.is_directed_acyclic_graph(graph):
            cycles = list(nx.algorithms.simple_cycles(graph))
            raise ValueError(CYCLE_ERROR_MSG + ". Cycles are: " + str(cycles))

        return logic_flow

    @pydantic.validator("segment_qubit_count")
    def validate_segment_qubit_count(cls, segment_qubit_count, values):
        if not segment_qubit_count:
            return segment_qubit_count

        segments = values.get("logic_flow")
        if segments is None:
            return segment_qubit_count
        if len(segments) == 1:
            return segment_qubit_count

        combine_segments = values.get("combine_segments")
        if combine_segments:
            return segment_qubit_count

        raise ValueError(
            "Segment qubit count can only be true if there is only one segment"
        )

    @pydantic.validator("output_format")
    def validate_output_format(cls, output_format):
        if isinstance(output_format, QuantumFormat):
            return [output_format]
        else:
            if len(output_format) == len(set(output_format)):
                return output_format
            else:
                raise ValueError(
                    f"{output_format=}\n"
                    "has at least one format that appears twice or more"
                )
