# Security and access control

Governed asset platforms must protect sensitive operational, commercial, and safety-related information.

## Core controls

- authentication
- role-based or attribute-based access control
- least privilege
- audit logging
- versioned approvals
- segregation of duties where needed

## Data sensitivity examples

- critical infrastructure details
- facility layouts
- maintenance histories
- security-relevant attributes
- regulated compliance evidence

## Design guidance

- classify data by sensitivity early
- keep raw source access narrower than read-model access where appropriate
- log changes to governed attributes
- treat admin access as a separate control surface

## Watchouts

- broad access “for convenience” that becomes permanent
- copying sensitive data into unmanaged exports
- unclear ownership of permission changes

See also:
- [Data governance foundations](data-governance.md)
- [Reference architecture](architecture.md)
