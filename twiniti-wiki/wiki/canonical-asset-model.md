# Canonical asset model

A canonical asset model is the shared structure and vocabulary used to represent assets consistently across systems.

## Why it matters

Without a canonical model, each platform invents its own version of the asset. That creates reconciliation work, unreliable analytics, and broken twins.

## Core elements

- asset class
- unique identifier
- hierarchy / parent-child relationships
- location
- status and lifecycle state
- critical attributes
- ownership metadata
- source and lineage references

## Design principles

- model the minimum viable truth first
- separate identity from descriptive attributes
- distinguish source data from derived data
- avoid overfitting the model to one system
- preserve history of changes

## Questions to answer

- What makes this asset distinct?
- Which attributes are mandatory?
- Which system owns each attribute?
- How are relationships represented?
- How are replacements, mergers, and splits handled?

See also:
- [Enterprise Asset Management](eam.md)
- [Ontology and asset semantics](ontology.md)
- [Migration strategy](migration-strategy.md)
