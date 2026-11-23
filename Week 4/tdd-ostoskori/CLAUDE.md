# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Standalone [uv](https://docs.astral.sh/uv/) project (Python >=3.14, pytest as the only dev dependency). Run from this directory; the parent path contains a space, so quote it.

```bash
uv sync
uv run pytest                                                          # all tests
uv run pytest src/tests/ostoskori_test.py::TestOstoskori::test_name    # single test
```

`src/` is the import root: modules import each other by bare name (`from tuote import Tuote`), and `src/tests/` is a package. Run pytest from this directory so the imports resolve. `src/index.py` is an empty placeholder, there is no app entry point.

## Rules

Tests executed withuv run pytest
Code of ostos.pyand tuote.pyshould not be changed
Tests should not be edited unless explicitly asked
Always implement absolutely minimal code that makes the tests pass

## Architecture

A TDD exercise (Finnish naming): build a shopping cart (`Ostoskori`) test-first.

- `tuote.py` — `Tuote(nimi, hinta)`, a product. Accessed through `nimi()` and `hinta()` methods.
- `ostos.py` — `Ostos(tuote)`, a cart line: a product plus quantity (starts at 1). `muuta_lukumaaraa(muutos)` takes a delta and clamps the quantity at 0. Already complete.
- `ostoskori.py` — `Ostoskori`, the class under development. It is currently a stub: every method is `pass`, except `hinta()` which returns 0. The intended API is `tavaroita_korissa`, `hinta`, `lisaa_tuote`, `poista_tuote`, `tyhjenna` and `ostokset`. The cart is expected to hold `Ostos` objects, so adding a product that is already in the cart should increase that line's quantity instead of adding a new line.
- `tests/ostoskori_test.py` — `unittest.TestCase` tests, with a fresh `Ostoskori` in `setUp`. Only the empty-cart test exists so far.

Keep the stub's method names (`lisaa_tuote`/`poista_tuote`). The sibling `Week 4/verkkokauppa` project has a different cart API (`lisaa`/`poista`), so don't mix the two.
