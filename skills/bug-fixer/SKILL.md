---
name: bug-fixer
description: Systematic bug fix workflow. Trigger this skill when users mention "fix bug", "bug fix", "修复bug", "修缺陷", "排查问题", "defect fix", "线上问题", or any context involving locating and fixing code defects. Even if the user doesn't explicitly say "fix bug", trigger this skill whenever the task involves diagnosing and resolving code defects.
---

# Bug Fixer — Systematic Defect Resolution Workflow

This skill defines a rigorous bug fix process that ensures every fix addresses root causes rather than symptoms, introduces no new issues, and prevents recurrence through regression tests and similar-pattern sweeps.

## Core Principles

1. **Evidence-Driven** — Never fix based on guesswork; every step must be backed by evidence
2. **Root Cause Over Symptom** — Fix the disease, not the symptom
3. **Minimal Change** — Only change what is necessary; no bundled refactors or new features
4. **Pattern Sweep** — Fix one, check all; address similar issues across the codebase
5. **Regression Guard** — Every fix must be backed by a regression test

## Workflow

### Step 1: Reproduce

A bug that cannot be reproduced cannot be confirmed as fixed. This is the one step you must never skip.

**Key actions:**
- Document exact reproduction steps (environment, data, operation sequence)
- Confirm reproduction frequency (100% / intermittent / conditional)
- If unable to reproduce, gather more context (logs, monitoring, user environment) rather than guessing
- Verify in a clean environment to rule out local configuration interference

**Must-answer questions:**
- Under what conditions does this bug reliably occur?
- Are there seemingly unrelated factors that affect reproduction?

### Step 2: Locate Root Cause

Trace backwards from the symptom to the root cause. Distinguish between "symptom" and "disease."

**Key actions:**
1. **Trace code path**: Follow the call stack / data flow backwards from the trigger point to the exact error location
2. **Pinpoint the break**: Identify the exact line/function responsible for the abnormal behavior
3. **Understand context**: Why does the code reach this error branch? Is it a data issue, logic error, or unhandled edge case?
4. **Check recent changes**: Use `git log` / `git blame` on relevant code to determine if this is a regression
5. **Bisect to narrow scope**: For large problem areas, use `git bisect`, conditional breakpoints, or elimination by commenting to narrow the range

**Must-answer questions:**
- What is the root cause? Data anomaly, logic error, missing edge case, or external dependency issue?
- Why wasn't this bug caught earlier? What is the blind spot in test coverage?

**Pitfalls to avoid:**
- ❌ Treating the error message as the root cause (the error is a symptom, not the disease)
- ❌ Assuming the cause without confirming
- ❌ Concluding after only examining the first level of the call stack

### Step 3: Sweep for Similar Patterns ⚡

**This is the step that separates thorough fixes from superficial ones.** Discovering one bug often means the same pattern exists elsewhere.

**Key actions:**
1. Extract the **failure pattern** from the current bug (e.g., unchecked null pointer, race condition, out-of-bounds access, type inconsistency)
2. Use search tools to globally scan the codebase for the same pattern
3. Evaluate each hit: does it carry the same risk?
4. Fix all discovered instances together, or annotate them in the fix record for follow-up

**Search strategy examples:**
- Null pointer → search all usage sites of similar variables, check for missing null checks
- Out-of-bounds → search similar array/collection operations, check boundary validation
- Concurrency → search similar shared-state access patterns
- Inconsistent API return values → search all callers of that API

**Must-answer questions:**
- Does the same failure pattern exist elsewhere in the codebase?
- If yes, fix them now or record them for later?

### Step 4: Implement the Fix

Fix the root cause, not the symptom. Minimal change, defensive coding.

**Key actions:**
- **Fix root cause**, not slap a try-catch at the error site to swallow the exception
- **Minimal change**: only modify necessary code; no bundled refactors in a bug fix PR
- **Defensive coding**: add necessary guards/validations at the fix point, but don't over-defend
- **Follow existing patterns**: see how similar situations are handled in the project and stay consistent
- **Type safety**: if the language supports it, use type constraints to prevent similar issues

**Prohibited actions:**
- ❌ Refactoring unrelated code during a fix
- ❌ Adding new features
- ❌ Over-defending (adding checks where they aren't needed)

### Step 5: Write Regression Tests

**Every bug fix must include regression tests.** This is the last line of defense against the same bug recurring.

**Key actions:**
1. **Write a test that reproduces the original bug** first, confirming it fails before the fix and passes after
2. Cover **edge cases** discovered during the fix
3. Write **integration tests** if the fix involves multi-component interaction
4. Update existing tests that contradict the new behavior

**Test coverage requirements:**
- ✅ Test reproducing the original bug
- ✅ Edge case tests
- ✅ Happy path still passes
- ✅ Tests for other locations with the same pattern (if Step 3 found and fixed similar issues)

### Step 6: Verify the Fix

Prove the bug is truly fixed, not merely masked.

**Verification checklist:**
- ✅ Follow original reproduction steps — bug no longer occurs
- ✅ Test edge conditions around the fix
- ✅ Confirm no new issues introduced (run full test suite)
- ✅ Verify in a near-production environment (e.g., staging)
- ✅ Verify that pattern-sweep fixes also work correctly
- ✅ Check for performance regression

### Step 7: Capture Knowledge

Turn the fix process into team knowledge assets.

**Key actions:**
- **Commit message**: clearly state what the bug was, what the root cause was, how it was fixed, and whether similar patterns were found
- **Knowledge base**: if this is a representative issue, add it to the team knowledge base
- **Preventive detection**: consider adding lint rules, type constraints, or other automated safeguards against similar issues
- **Process reflection**: why wasn't this bug caught earlier? What improvements can be made to testing / code review / design?

**Commit message format:**
```
fix(module): brief description of the fixed issue

Problem: [user-visible symptom description]
Root cause: [root cause analysis, pointing to specific code location]
Fix: [brief explanation of the fix and why it was done this way]
Similar: [whether similar patterns were swept, what was found]

Closes #xxx
```

## Common Anti-Patterns

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Guessing the cause and editing code directly | Reproduce first, locate root cause with evidence |
| Adding try-catch at the error site to swallow exceptions | Find out why the exception occurs, fix the root cause |
| Bundling refactors in a bug fix | Only fix the bug; open a separate PR for refactors |
| Not writing regression tests | Every bug fix must include tests |
| Fixing only this instance, not checking similar issues | Sweep for similar patterns, address them together |
| "It works on my machine" | Verify reproduction in a clean environment |
| Not running the full test suite after fixing | Confirm no new issues were introduced |

## Quick Checklist

Confirm each item after completing a fix:

- [ ] Bug has been reliably reproduced
- [ ] Root cause has been located and documented
- [ ] Similar patterns have been swept
- [ ] Fix targets the root cause, not the symptom
- [ ] Change scope is minimized
- [ ] Regression tests written and passing
- [ ] Full test suite passing
- [ ] Commit message includes complete context
