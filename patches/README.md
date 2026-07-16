# Suggested code changes for active findings

The files in this directory are **LLM-generated implementation sketches** for the currently active findings.

They are not reviewed, compiled, tested, or ready to apply directly. They show only the approximate scope, files, control flow and code shape that may be involved. Before using any part, a maintainer must verify the behavior against official MeshCore, rewrite it for the current architecture, add focused interoperability tests, and review interactions with every other finding.

Each `BUG-NNN.patch` is independent and the sketches are not designed as a combined patch series. Sketches for fully fixed historical findings are under [`archive/patches/`](../archive/patches/).

The deeper follow-up adds BUG-081 through BUG-100. BUG-023 has been moved to `archive/intentional/patches/` and is no longer an active recommendation.
