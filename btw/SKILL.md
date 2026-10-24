---
name: btw
description: Manually-invoked side-question mode — answer a quick tangential question without disturbing the main task. Use when the user says "btw", "quick question", "side question", or asks something unrelated mid-task.
disable-model-invocation: true
---

the user is asking a quick side question. rules:

1. answer ONLY the side question, briefly. no preamble, no recap of the main task.
2. do NOT edit, write, or delete files. read-only lookups are allowed if the question needs a fact.
3. do NOT run commands that change state (no installs, no commits, no config changes).
4. after answering, state the main task you were on in one line so work can resume, then stop and wait.
