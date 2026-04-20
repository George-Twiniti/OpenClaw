# Twiniti AI Providers Landscape deployment plan

## Target host
- Oracle web server: `132.145.195.174`
- SSH host alias used on the server: `twiniti-alt-web`
- SSH key: `~/.ssh/ssh-key-2026-04-10.key`

## Nginx layout discovered on host
- Default/public site: `/srv/twiniti-aeo`
- Wiki site: `/srv/twiniti-wiki` on port `8080`
- Nginx config: `/etc/nginx/sites-enabled/twiniti`

## Public site URL
- `http://aeo.twiniti.ai/` or `http://132.145.195.174/`
- The new AI Providers Landscape page should live under this site as a standalone path, likely:
  - `/ai-providers-landscape`

## Deployment approach
- create a new HTML page in `/srv/twiniti-aeo/ai-providers-landscape/index.html`
- include the generated provider data or inline JSON
- keep the existing main site untouched
- refresh with a weekly update job that rewrites the data source and republishes the HTML

## Immediate next step
- inspect `/srv/twiniti-aeo`
- add the new route directory
- publish the page and verify it serves correctly
