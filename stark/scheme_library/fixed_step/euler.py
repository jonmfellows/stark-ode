from __future__ import annotations

from stark.audit import Auditor
from stark.control import Tolerance
from stark.contracts import Derivative, IntervalLike, State, Workbench
from stark.scheme_butcher_tableau import ButcherTableau
from stark.scheme_identity import SchemeIdentity
from stark.scheme_parts import SchemeParts


EULER_TABLEAU = ButcherTableau(
    c=(0.0,),
    a=((),),
    b=(1.0,),
    order=1,
)
EULER_B = EULER_TABLEAU.b


class SchemeEuler:
    """Classic first-order explicit Euler method."""

    __slots__ = ("delta", "derivative", "k1", "parts")

    identity = SchemeIdentity("Euler", "Forward Euler")
    tableau = EULER_TABLEAU

    def __init__(self, derivative: Derivative, workbench: Workbench) -> None:
        translation_probe = workbench.allocate_translation()
        Auditor.require_scheme_inputs(derivative, workbench, translation_probe)
        self.derivative = derivative
        self.parts = SchemeParts(workbench, translation_probe)
        self.k1 = translation_probe
        self.delta = self.parts.allocate_translation()

    @classmethod
    def display_tableau(cls) -> str:
        return cls.identity.display_tableau(cls.tableau)

    @property
    def short_name(self) -> str:
        return self.identity.short_name

    @property
    def full_name(self) -> str:
        return self.identity.full_name

    def __repr__(self) -> str:
        return self.identity.repr_for(type(self).__name__, self.tableau)

    def __str__(self) -> str:
        return self.display_tableau()

    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)

    def set_apply_delta_safety(self, enabled: bool) -> None:
        self.parts.set_apply_delta_safety(enabled)

    def snapshot_state(self, state: State) -> State:
        return self.parts.snapshot_state(state)

    def __call__(self, interval: IntervalLike, state: State, tolerance: Tolerance) -> float:
        del tolerance
        remaining = interval.stop - interval.present
        if remaining <= 0.0:
            return 0.0

        parts = self.parts
        derivative = self.derivative
        scale = parts.scale
        apply_delta = parts.apply_delta
        k1 = self.k1
        delta_buffer = self.delta

        dt = interval.step if interval.step <= remaining else remaining
        derivative(state, k1)
        delta = scale(delta_buffer, dt * EULER_B[0], k1)
        apply_delta(delta, state)
        return dt


__all__ = ["EULER_TABLEAU", "SchemeEuler"]
