# Reference architecture

This page describes a practical architecture for governed asset data and digital twins.

## Core layers

1. **Source systems**
   - EAM / CMMS
   - ERP
   - BIM / CAD
   - GIS
   - IoT / telemetry
   - document and content stores

2. **Governed asset foundation**
   - canonical asset model
   - master identifiers
   - hierarchy and location model
   - business rules and attribute standards

3. **Integration and validation**
   - ingestion pipelines
   - mapping and transformation
   - data quality checks
   - approval and exception handling

4. **Twin and analytics services**
   - operational views
   - simulation / prediction
   - dashboards and alerts
   - downstream APIs

5. **Workflow and action**
   - maintenance work orders
   - review / approval tasks
   - compliance evidence
   - change tracking

## Design patterns

- **Canonical asset model first**: define shared semantics before integration expands.
- **Hub-and-spoke integration**: central governed core with system adapters.
- **Event-driven updates**: refresh critical states from operational events.
- **Read-optimized twin**: separate operational write systems from analytical read models.
- **Policy-enforced access**: permission rules sit alongside data delivery.

## Anti-patterns

- point-to-point integrations without semantic governance
- treating a dashboard as the twin
- forcing every system to mirror every field
- mixing source-of-record data with derived metrics without labeling

## Architecture questions to answer early

- What is the system of record for identity?
- Which attributes are authoritative in which system?
- What refresh latency is actually required?
- Which workflows need human approval?
- Which data is safety-critical or regulated?

See also:
- [Canonical asset model](canonical-asset-model.md)
- [Integration patterns](integration-patterns.md)
- [Security and access control](security-and-access-control.md)
