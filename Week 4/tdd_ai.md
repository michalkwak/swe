# TDD with AI

The agent ended up with a good implementation and decent tests. All 16 tests pass. After a refactoring the item count and the price are calculated from the list of purchases, and one helper finds a purchase by product. The tests cover the empty cart, adding one or two products (same and different), the price, the list of purchases, removing a product and emptying the cart. Some cases are still missing, for example removing a product that is not in the cart. Also, two separate Tuote objects with the same name count as different products.

The agent stuck to the minimum implementation and did not change the existing tests. It only added new tests, finished one that I had started and renamed one when I asked. It wrote only the code that the failing test needed. For example, the price and the purchase list were not touched when removing a product until a test needed them. The downside is that minimal code left small gaps, like removing a product that was not in the cart, until the refactoring.

The agent did not cheat in a bad way. At the start it made tavaroita_korissa return 0, which is a hardcoded value, but that is a normal first TDD step and the next test forced a real implementation. It never changed a test to make it pass.

In this exercise I gave the test descriptions and the agent wrote both the tests and the code, so it was closer to division B. I think A is better, where I write the tests and the AI writes the code. The tests are the specification, and if the same AI writes them, it may write tests that fit its own code. With B I had to check everything myself. For example, the agent had to guess what I meant by an unfinished line in my test. B is faster, but A keeps the control with me.
