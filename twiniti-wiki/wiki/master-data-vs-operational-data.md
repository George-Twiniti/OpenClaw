# Master data vs operational data

Understanding the difference helps teams avoid mixing stable definitions with live state.

## Master data

Master data describes the things that exist:
- asset identifiers
- asset classes
- location references
- reference hierarchies
- approved attribute values

## Operational data

Operational data describes what is happening:
- work orders
- sensor readings
- inspections
- incidents
- status changes
- measurements over time

## Why the distinction matters

Master data should be relatively stable and governed tightly. Operational data changes continuously and often needs different storage, latency, and access patterns.

## Common problem

Organizations often store operational facts in master records because it is convenient. That makes the master model noisy, hard to trust, and difficult to integrate.

See also:
- [Data governance foundations](data-governance.md)
- [Reference architecture](architecture.md)
