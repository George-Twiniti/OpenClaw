# Lifecycle model

Assets, data, and digital twins all move through lifecycle stages. The wiki should reflect that lifecycle instead of treating the twin as a one-time deployment.

## Typical lifecycle stages

- **Plan** — define need, scope, standards, and governance.
- **Design** — model the asset, information requirements, and integrations.
- **Build** — create master data, mappings, and controls.
- **Commission** — validate handover, identity, and baseline state.
- **Operate** — keep the twin and operational systems in sync.
- **Maintain** — update, repair, inspect, and review performance.
- **Optimize** — use analytics and simulation to improve outcomes.
- **Retire / replace** — archive history and manage end-of-life transitions.

## Lifecycle thinking in practice

The key question at each stage is: what data must be trusted now, and who owns it?

## Common lifecycle gaps

- design data not handed over cleanly to operations
- asset identifiers changed midstream
- maintenance history detached from the original asset context
- retirement data not preserved for audit or lessons learned

## Practical guidance

Build workflows so that:
- lifecycle changes trigger data updates
- handover includes validation and approval
- retired assets remain traceable
- historical records stay queryable even after systems evolve

See also:
- [Enterprise Asset Management](eam.md)
- [Digital twin](digital-twin.md)
- [Implementation playbook](implementation-playbook.md)
