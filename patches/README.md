# Suggested code changes

The files in this directory are **LLM-generated implementation sketches**.

They are not reviewed, compiled, tested, or ready to apply directly. They are provided only to show the approximate scope, files, control flow, and code shape that may be involved in fixing each audited bug.

Before using any part of a sketch, a maintainer must:

- verify the behavior against the official MeshCore implementation;
- adapt or rewrite the code for the current OpenHop architecture;
- add focused unit, integration, and interoperability tests;
- review interactions with fixes for other findings; and
- perform normal security and protocol review.

Each `BUG-NNN.patch` is independent. The sketches are not designed as a combined patch series and may conflict with one another.
