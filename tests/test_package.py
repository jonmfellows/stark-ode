"""Basic smoke tests for the project scaffold."""

import importlib

from stark import Advance, Auditor, Integrate, Interval, StepController, Tolerance
from stark.scheme_butcher_tableau import ButcherTableau


def test_package_imports() -> None:
    """The top-level package should import cleanly."""
    assert importlib.import_module("stark") is not None


def test_advance_module_imports() -> None:
    """The advance module should exist and import cleanly."""
    assert importlib.import_module("stark.advance") is not None


def test_audit_module_imports() -> None:
    """The audit module should exist and import cleanly."""
    assert importlib.import_module("stark.audit") is not None


def test_control_module_imports() -> None:
    """The control module should exist and import cleanly."""
    assert importlib.import_module("stark.control") is not None


def test_integrate_module_imports() -> None:
    """The integrate module should exist and import cleanly."""
    assert importlib.import_module("stark.integrate") is not None


def test_rk4_module_imports() -> None:
    """The RK4 method module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.rk4") is not None


def test_fixed_step_rk4_module_imports() -> None:
    """The fixed-step RK4 method module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.fixed_step.rk4") is not None


def test_euler_module_imports() -> None:
    """The Euler scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.euler") is not None


def test_heun_module_imports() -> None:
    """The Heun scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.heun") is not None


def test_midpoint_module_imports() -> None:
    """The midpoint scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.midpoint") is not None


def test_ralston_module_imports() -> None:
    """The Ralston scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.ralston") is not None


def test_kutta3_module_imports() -> None:
    """The Kutta3 scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.kutta3") is not None


def test_ssprk33_module_imports() -> None:
    """The SSPRK33 scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.ssprk33") is not None


def test_rk38_module_imports() -> None:
    """The RK38 scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.rk38") is not None


def test_cash_karp_module_imports() -> None:
    """The Cash-Karp method module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.cash_karp") is not None


def test_adaptive_cash_karp_module_imports() -> None:
    """The adaptive Cash-Karp method module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.adaptive.cash_karp") is not None


def test_fehlberg45_module_imports() -> None:
    """The Fehlberg45 scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.fehlberg45") is not None


def test_bogacki_shampine_module_imports() -> None:
    """The Bogacki-Shampine scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.bogacki_shampine") is not None


def test_dormand_prince_module_imports() -> None:
    """The Dormand-Prince scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.dormand_prince") is not None


def test_tsitouras5_module_imports() -> None:
    """The Tsitouras 5 scheme module should exist and import cleanly."""
    assert importlib.import_module("stark.scheme_library.tsitouras5") is not None


class MinimalScheme:
    def __call__(self, interval: Interval, state: object, tolerance: Tolerance) -> float:
        del interval, state, tolerance
        return 0.0

    def snapshot_state(self, state: object) -> object:
        return state

    def set_apply_delta_safety(self, enabled: bool) -> None:
        del enabled


def test_core_objects_have_readable_representations() -> None:
    interval = Interval(0.0, 0.1, 1.0)
    tolerance = Tolerance(atol=1.0e-8, rtol=1.0e-6)
    controller = StepController()
    tableau = ButcherTableau(c=(0.0,), a=((),), b=(1.0,), order=1, short_name="E")
    advance = Advance(MinimalScheme(), tolerance)
    auditor = Auditor(interval=interval, advance=advance, snapshots=True, exercise=False)

    assert repr(interval) == "Interval(present=0.0, step=0.1, stop=1.0)"
    assert str(interval) == "[0, 1] step=0.1"
    assert repr(tolerance) == "Tolerance(atol=1e-08, rtol=1e-06)"
    assert str(tolerance) == "atol=1e-08, rtol=1e-06"
    assert "StepController" in repr(controller)
    assert "safety=" in str(controller)
    assert repr(tableau) == "ButcherTableau(stages=1, order=1, embedded_order=None, name='E')"
    assert str(Integrate()) == "STARK integrator (safe mode)"
    assert repr(advance) == "Advance(scheme='MinimalScheme', tolerance=Tolerance(atol=1e-08, rtol=1e-06), apply_delta_safety=True)"
    assert str(advance) == "Advance MinimalScheme with atol=1e-08, rtol=1e-06"
    assert "Auditor(status=" in repr(auditor)


def test_benchmark_packages_import() -> None:
    assert importlib.import_module("benchmarks.brusselator_2d.common") is not None
    assert importlib.import_module("benchmarks.fput.common") is not None
