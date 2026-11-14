# AI report

I used `/init` and it made a CLAUDE.md with commands for running the app and tests, and a short overview of the code. It also pointed out a bug (`delete()` uses `user.id`, but `User` has no id). I didn't have to fix anything.

It wrote the tests first and ran them. For the password story, 2 tests failed and then passed after the fix. For the password confirmation story, the feature was already in the code, so the tests passed straight away, and Claude ent told me so.

I didnt have to guide it much. I just pasted the user stories and said "write tests" and then "implement".

The tests failed "correctly". When I changed the code so it no longer worked, the matching tests failed.

I learned how to write Robot Framework tests for a web app, and that the app must be running before the tests start. Also that the agent checks its own work by running the tests.
