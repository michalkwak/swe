# TDD with AI

I gave the AI one test at a time. It wrote the test, saw it fail and then wrote the smallest code that made it pass, just as instructed. Some tests passed right away, for example the one about two different products, so no new code was needed. At first the AI kept the code very simple and used counters for the item count and the price.

After all the tests passed, I asked for a refactoring. The item count and the price were stored separately from the list of purchases, so the same data was kept in three places. Now the count and the price are calculated from the purchases, and a small helper method finds a purchase by product. The code got shorter and the behavior stayed the same. All 16 tests still pass.

I did not change the tests. They repeat the same setup such as creating the Maito product and adding it twice, and this could be moved to setUp. The test names are also partly Finnish and partly English.

Small steps worked well, and the AI did not add code that no test needed. I also had to check the AI's work. For example, it guessed that a typo in my test (poista_tuote instead of lisaa_tuote) was a mistake.
