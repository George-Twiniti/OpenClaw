# Migration strategy

Migrating asset data is usually harder than migrating the software.

## Principles

- preserve source-of-truth history
- migrate the minimum needed to support the next phase
- keep old and new models reconciled during transition
- avoid big-bang replacements where possible

## Typical approach

1. inventory source systems and data domains
2. define target canonical model
3. map fields and relationships
4. identify gaps and duplicates
5. run pilot migration on one scope
6. validate and reconcile
7. cut over in stages
8. monitor and clean up

## Common migration risks

- hidden duplicates
- unmapped historical records
- broken hierarchy references
- weak owner agreement
- too much transformation logic embedded in migration code

See also:
- [Canonical asset model](canonical-asset-model.md)
- [Implementation playbook](implementation-playbook.md)
