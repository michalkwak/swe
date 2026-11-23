# Reflection on the AI refactoring

**Did removing the duplication make sense? Is the test code easier to read?**
Yes, the agent moved the repeated setup (mocks, products, stock, creating the shop) into one setUp method. Before, every test would have had about 20 lines of the same setup. Now each test is only a few lines for adding products, paying and checking the call. It is much easier to see what each test is about.

**Did the agent change the functionality of the tests? Did it remove or weaken checks?**
No, all the new tests use assert_called_with, so the exact customer name, reference number, account numbers and amount are checked. The agent did not go back to the weaker assert_called. The original test was left as it was.

**Did I have to correct the agent or ask for changes?**
No, I did not need to correct anything. The tests passed on the first run. I only checked that the expected amounts (5, 8, 10, 5) match the product prices.
