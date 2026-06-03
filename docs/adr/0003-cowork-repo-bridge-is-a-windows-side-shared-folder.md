# The Cowork ↔ repo handoff bridges via a Windows-side shared folder, not the WSL2 path or Drive

**Status:** accepted

Claude Code runs in WSL2 (repo at `/home/ringo/soriza-startup-layer`); Cowork runs in Claude Desktop
on the Windows host. The official local-access docs state Cowork's sandbox "cannot reach network
shares" and that "raw UNC paths (`\\server\share`) are not supported; map the share to a drive letter
first." The WSL2 filesystem is reachable from Windows *only* as a UNC path (`\\wsl.localhost\…`), so
attaching the WSL2 repo folder to Cowork does not work.

**Decision.** The customer-discovery handoff bridges through a **Windows-side local NTFS folder**
(`C:\dev\soriza-cowork\`), attached natively in Cowork and reached from WSL2 as
`/mnt/c/dev/soriza-cowork/`. Only the small handoff files live there (run-pack out; interview notes +
tracking sheet back); the git repo stays native in WSL2 ext4. The Cowork run-pack remains **sealed**
regardless (works even with no folder attached). Google Drive stays a **connector** for
outreach/scheduling/tracking — not the file-share substrate.

## Considered Options

- **Attach the WSL2 repo folder directly.** Rejected: only reachable as a UNC path, which Cowork
  doesn't support, and the sandbox can't reach network shares.
- **Google Drive as the file bridge.** Rejected for now: adds a sync layer + a second copy to
  reconcile, and puts prospect PII in a third-party cloud (the founder's risk appetite is low). The
  only upside — headless/multi-device access — doesn't apply to a single-machine solo founder.

## Consequences

- Single-machine coupling: the bridge assumes Cowork and Claude Code share one host. **If Cowork ever
  runs headless or from another machine, switch to the Drive bridge.**
- Keep `/mnt/c` use to small markdown only; git/node work stays in WSL2 ext4 for speed.
