# Integration patterns

## Common patterns

- **Batch sync** — simple and robust for low-frequency updates.
- **API federation** — query systems at runtime through interfaces.
- **Event streaming** — propagate important changes as they happen.
- **ETL / ELT into a governed store** — useful for analytics and twin read models.
- **Hub-and-spoke** — central governed core with adapters to source systems.

## Choosing a pattern

Use the simplest pattern that meets the use case’s freshness, reliability, and governance requirements.

## Pattern selection questions

- How fresh does the data need to be?
- Is the downstream use operational or analytical?
- Do we need write-back or only read access?
- Can we tolerate temporary inconsistency?
- Which validations must happen before data is published?

## Anti-patterns

- point-to-point spaghetti
- duplicating all data in every system
- using integration as a substitute for governance
- overusing real-time plumbing when daily refresh is enough

See also:
- [Reference architecture](architecture.md)
- [Data quality and stewardship](data-quality.md)
