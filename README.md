# stark-ode

`stark-ode` is the starting point for **State Translation Adaptive Runge Kutta**.

STARK is an adaptive Runge-Kutta solver for user-defined state types. Instead of
flattening everything into a vector, it separates rich mutable states from
translation objects that carry the linear structure and error norm needed for
time-stepping.

The package code lives in `stark/`. Runge-Kutta schemes live under
`stark/scheme_library/`: embedded adaptive methods are in `adaptive/`, classic
explicit fixed-step methods are in `fixed_step/`, and the top-level scheme
library re-exports the public scheme classes.

## Development

Create a virtual environment, install the package in editable mode with dev
dependencies, and run the tests:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

## Packaging

The project is configured with `pyproject.toml`, which is enough to build a
distributable package later with:

```powershell
python -m build
```

The package is released under the MIT license. Before publishing to a package
index, add the repository and package index URLs you want exposed in the
metadata.

## Example

In a source checkout, a guided three-body notebook lives at
`examples/three_body_stark.ipynb`. It starts from a structured dataclass model
with an Euler stepper, shows why fixed-step Euler is fragile for Moore's
figure-eight orbit, then adds the small STARK adapter layer needed for adaptive
integration and checkpointed plotting.

From the repository root, install the optional notebook dependencies and open it
with:

```powershell
python -m pip install -e ".[notebooks]"
python -m jupyter lab examples/three_body_stark.ipynb
```

## Documentation

A compact functionality guide lives at
[`docs/README.md`](docs/README.md). It lists the built-in schemes, integration
APIs, checkpoints, auditing tools, custom scheme contract, and translation fast
paths.

## Citation

If you use `stark-ode` in research or published work, please cite the package
repository. Citation metadata is provided in `CITATION.cff`, which GitHub can
render as a ready-to-copy citation once the repository is public.

## GitHub And Release Automation

The repository includes:

- a CI workflow at `.github/workflows/ci.yml` for import and test checks
- a release workflow at `.github/workflows/release.yml` that builds and publishes
  on version tags once PyPI publishing is configured
