# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### GitHub Keys

- ~/.ssh/id_ed25519_github_openclaw → deploy/access key for OpenClaw backup repo

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Local Notes

### GitHub Keys

- `~/.ssh/id_ed25519_github_openclaw` → SSH key associated with the **OpenClaw backup repo** (`George-Twiniti/OpenClaw`)
- Public export copied to `github-openclaw.pub`
- This key is for the OpenClaw backup repo and should be treated/labeled that way to avoid confusion with future repo-specific keys (for example `Second-Brain`)

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
