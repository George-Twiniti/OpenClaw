# AI Providers Landscape — build spec

## Goal
Keep the Twiniti AI Providers Landscape page visually consistent with the current design, while making the provider/model content easy to refresh and keep current on a weekly schedule.

## Visual direction
Preserve the current look and feel:
- gradient page background
- centered white content container
- tiered layout
- provider cards in a responsive grid
- color-coded provider dots
- clickable model rows that reveal details
- “show all / hide all” toggle
- legend + note section

## Recommended architecture
- **Standalone route/page** on the same webserver used for AEO work
- **Template-driven layout** so the page style is preserved
- **Data-driven content layer** so providers/models can be updated without rewriting the HTML
- **Weekly refresh workflow** to keep it current

## Data model
Store provider data separately in JSON or Markdown.

Suggested fields per provider:
- `name`
- `tier`
- `color`
- `overview`
- `models[]`
- `bestFor[]`
- `contextWindow`
- `notes`
- `officialSources[]`
- `lastReviewed`

Suggested top-level fields:
- `pageTitle`
- `subtitle`
- `lastUpdated`
- `tiers[]`
- `footerNote`
- `sourcePolicy`

## Page behavior
- clicking a model row reveals the provider detail panel
- show a single toggle button for all cards
- surface a clear `Last updated` stamp
- optionally include a compact sources footer

## Refresh workflow
### Weekly
- update the provider data from official announcement pages/docs
- refresh the page output
- publish if the review passes

### Manual
- allow a one-off refresh when a major new model launches

### Safety
- use official provider sources as the primary truth
- avoid relying on secondary summaries for model names or release status
- if a provider has multiple active model families, include only the current primary ones

## Content strategy
The page should answer:
- Who are the main providers right now?
- What are their current flagship models?
- What are they best at?
- Which providers matter for frontier work, enterprise work, and local/open-weight work?

## Initial provider coverage
Core providers to include:
- OpenAI
- Anthropic
- Google DeepMind / Gemini
- Meta
- Mistral
- xAI
- Cohere
- Amazon Bedrock / Nova
- DeepSeek
- Qwen / Alibaba
- Microsoft Phi
- Ollama
- Hugging Face

## Update cadence recommendation
- **Weekly scheduled refresh** for general upkeep
- **Ad hoc refresh** for major launches or model retirements

## Implementation plan
1. Extract the existing page into a reusable template.
2. Move provider content into a separate structured file.
3. Add a renderer that generates the final HTML.
4. Add a weekly job to refresh the structured content.
5. Add a timestamp and sources so visitors can trust the page.

## Definition of done
- same visual style as the current page
- standalone page on the same webserver
- provider data editable independently from layout
- weekly update path exists
- the page can be kept current without hand-editing the full HTML
