# Correctness, Boundaries, And Coverage

## Type Boundaries

### What to look for

Unnecessary `any`, `unknown`, casts, optional parameters, silent fallbacks, or ad-hoc object shapes that obscure the real invariant. Pay attention when a branch depends on a value being present or having a particular shape but the boundary does not express that contract.

### Preferred fix

Make the boundary explicit with a typed model, shared contract, validation, or a narrower API. Remove casts and optionality when they only paper over an unclear invariant. Follow established project conventions and do not flag intentional, well-supported flexibility.

## Async Orchestration

### What to look for

Independent operations serialized without a correctness or dependency reason, or orchestration whose extra steps make failure handling and control flow more brittle. Do not treat every sequential operation as a performance problem.

### Preferred fix

Run genuinely independent work in parallel when that keeps the flow clearer and preserves error, cancellation, and ordering semantics. Otherwise prefer the simplest explicit sequence.

## Atomicity And Partial State

### What to look for

Related updates that can leave state half-applied when one step fails, especially where readers or later operations can observe an invalid intermediate state.

### Preferred fix

Use a transaction, cohesive operation, staged update, rollback, or other atomic structure when the domain invariant requires it. Explain the failure scenario and the invalid state rather than flagging multi-step code automatically.

## Test Coverage

### What to look for

Changed behavior without focused coverage for its normal path, meaningful edge cases, error handling, or likely regressions. Check whether existing tests exercise the changed contract rather than counting test files or lines.

### Preferred fix

Add focused tests at the layer where the behavior is owned. Cover the inputs and failure modes that the diff changes, while following the repository's existing testing conventions and avoiding tests for behavior that is purely mechanical or already covered.
