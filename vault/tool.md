---
title: "Tool"
type: foundation
status: draft
evidence: untested
secrets: false
---

# Tool

A **tool** is a note under `tools/`. It names one component: what it is for,
when to use it, when to avoid it, what it proves, how it attaches to Hermes,
its synthetic acceptance cases, and one typical job.

The note is the tool. The adapter that wraps it lives in each project under
`integrations/<component>/wrapper/`.

A component without a run on a named host keeps `verified-upstream` or
`untested`. Pattern: [[admit]]. See [[toolchain]].
