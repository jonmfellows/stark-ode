from __future__ import annotations

from stark.audit import Auditor
from stark.control import Tolerance
from stark.contracts import Derivative, IntervalLike, State, Workbench
from stark.scheme_butcher_tableau import ButcherTableau
from stark.scheme_identity import SchemeIdentity
from stark.scheme_parts import SchemeParts


HEUN_TABLEAU = ButcherTableau(
    c=(0.0, 1.0),
    a=((), (1.0,)),
    b=(0.5, 0.5),
    order=2,
)
HEUN_B = HEUN_TABLEAU.b


class SchemeHeun:
    """Two-stage second-order Heun method."""

    __slots__ = ("derivative", "k1", "k2", "parts", "stage", "trial")

    identity = SchemeIdentity("Heun", "Heun")
    tableau = HEUN_TABLEAU

    def __init__(self, derivative: Derivative, workbench: Workbench) -> None:
        translation_probe = workbench.allocate_translation()
        Auditor.require_scheme_inputs(derivative, workbench, translation_probe)
        self.derivative = derivative
        self.parts = SchemeParts(workbench, translation_probe)
        self.k1 = translation_probe
        parts = self.parts
        self.stage = parts.allocate_state_buffer()
        self.trial, self.k2 = parts.allocate_translation_buffers(2)

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
        combine2 = parts.combine2
        apply_delta = parts.apply_delta
        stage = self.stage
        trial_buffer = self.trial
        k1 = self.k1
        k2 = self.k2

        dt = interval.step if interval.step <= remaining else remaining
        derivative(state, k1)

        trial = scale(trial_buffer, dt, k1)
        trial(state, stage)
        derivative(stage, k2)

        delta = combine2(
            trial_buffer,
            dt * HEUN_B[0],
            k1,
            dt * HEUN_B[1],
            k2,
        )
        apply_delta(delta, state)
        return dt


__all__ = ["HEUN_TABLEAU", "SchemeHeun"]
