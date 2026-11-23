# TDD with AI

## How it went
- I gave one test at a time. The AI wrote the test, saw it fail, then wrote the smallest code to pass.
- Some tests passed right away (for example "two different products"). No new code was needed.
- The AI kept the code very simple at first. It used counters for items and price.

## Refactoring
- Problem: item count and price were stored separately from the purchase list. The same data was kept in three places.
- Fix: count and price are now calculated from the purchases. A helper finds a purchase by product.
- The code got shorter and the behavior stayed the same. All 16 tests still pass.

## Not changed
- The tests repeat the same setup (`Tuote("Maito", 3)`, adding it twice). This could be moved to `setUp`.
- Test names are partly Finnish and partly English.

## Thoughts
- Small steps worked well. The AI did not add code that no test needed.
- Minimal code can be a bit "fake" (counters). Refactoring is needed to clean it up.
- I had to check the AI's work: it guessed a typo in my test (`poista_tuote` instead of `lisaa_tuote`).
