# Maintainability And Design

## Complexity Growth

### What to look for

New ad-hoc conditionals, one-off booleans, nullable modes, feature checks, or special cases scattered through existing flows. Flag them when they make the surrounding control flow harder to reason about.

### Preferred fix

Move the decision into a dedicated policy, state model, dispatcher, helper, or module. Prefer a design that removes branches instead of adding another exception to the existing path.

Only flag complexity introduced or materially worsened by the diff, and explain the concrete reasoning burden it creates.

## Structural Simplification

### What to look for

Working code that preserves unnecessary concepts, branches, helper layers, or orchestration steps when the same behavior can be expressed more directly. Look for a clear restructuring that deletes complexity rather than merely moving it.

### Preferred fix

Reframe the state model, ownership boundary, or control flow so whole categories of complexity disappear. Do not demand speculative rewrites; flag only a high-confidence simplification that materially improves the changed code.

## Abstraction Quality

### What to look for

Thin wrappers, identity abstractions, pass-through helpers, generic mechanisms, or magical behavior that hide a simple flow without improving clarity. An abstraction is suspect when its name and layer add indirection but no meaningful responsibility.

### Preferred fix

Delete or inline abstractions that do not earn their complexity. Prefer direct, boring code unless the abstraction provides a real boundary, reuse, or domain meaning.

## Canonical Ownership

### What to look for

Feature logic leaking into shared paths, implementation details crossing API or package boundaries, or a bespoke helper duplicating a canonical utility. The changed code should live with the module, service, or layer that owns the concept.

### Preferred fix

Move the logic to its canonical owner and reuse existing helpers or contracts. Avoid normalizing architectural drift by adding another local implementation.

## File And Module Growth

### What to look for

A diff that makes a file or component substantially harder to scan, mixes several responsibilities, or crosses a project-defined size boundary. A large file is a concern when the new code could have a focused home elsewhere, not merely because of its line count.

### Preferred fix

Extract focused modules, helpers, subcomponents, or cohesive abstractions. Follow repository-specific size and organization conventions instead of enforcing a universal line-count threshold.
