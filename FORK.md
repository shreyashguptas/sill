# This fork: hard rules

This repository is **shreyashguptas/sill**, a fork of **Saffsanity/sill** ("upstream"). Its owner
builds and runs the apps from this fork only. These rules bind every agent and every person working
here, every time, with no exceptions. Only the owner changes this file.

## 1. Upstream is a source to review, never to sync

- Never press GitHub's "Sync fork", never reset or fast-forward `main` to upstream, never push to
  upstream, never open a pull request to upstream.
- To bring in upstream's work: `git fetch upstream`, then review **every commit** in
  `main..upstream/main`. Read every changed line of code, scripts, build settings and workflows in
  full, not a skim. Docs-only changes can be read faster, but still read.
- Look for, and refuse anything that adds or changes:
  - a network address, server, domain, relay, proxy, CDN, analytics or telemetry service, crash
    reporter or any outbound connection (URLSession, NWConnection or sockets to fixed hosts);
  - data sent off the devices (clipboard, keys, screen, typed text, logs) to anything but the
    owner's own Mac and devices;
  - a dependency (Package.swift, Xcode packages), a build-time script or run-script phase, a
    downloaded-and-run step (curl, wget, pip, npm, brew), obfuscated code or encoded blobs, dynamic
    code loading, new subprocesses or privileges;
  - weaker pairing, TLS, pinning, admission or test-hook gating; new entitlements or permissions.
- Anything malicious or suspicious is **not brought in**. Report it to the owner with file:line.
- Good changes are brought in on a branch (`upstream-review-YYYY-MM-DD`), merged with a merge commit
  (never a rebase), with these fork changes kept, and offered to the owner as a pull request into
  this fork's `main` with the review's findings. The owner decides.

## 2. Servers: ours only

The apps and scripts may reach only:

- the owner's own Mac and devices (found on the local network, typed in, or paired);
- this fork's GitHub repository, `github.com/shreyashguptas/sill` and
  `api.github.com/repos/shreyashguptas/sill`;
- Apple's own services (`*.apple.com`: App Store Connect for TestFlight, system pages).

Any repository, website or server upstream names in code, scripts or workflows is changed to this
fork's, or removed. No third-party server, ever. Upstream's documentation (`docs/`, `site/`,
`README.md`, `CLAUDE.md`, `LICENSE`) may keep its own words; the apps never contact those places.
Keep GitHub Pages off for this fork (`site/CNAME` names upstream's domain).

## 3. The fork's changes stay as they are

An upstream merge must never undo these. On a conflict, keep this fork's side, then fit upstream's
change around it.

| Where | What this fork changed |
|---|---|
| `Sources/SillMenuBar/UpdatePolicy.swift` | `repo = "shreyashguptas/sill"`; `feed` built from it; `releasePage` opens only `github.com/shreyashguptas/sill/releases/…` |
| `iOSClient/SillLinks.swift` | `site` is the fork's GitHub repository; download, support and privacy links under it; `appStoreText` stays `APP_STORE_URL_PLACEHOLDER` (no App Store link) |
| `Scripts/release.sh` | `feed_repo=shreyashguptas/sill`; release notes link the fork's releases; `nightly_testflight_link` empty |
| `Scripts/nightly-notes.sh`, `Scripts/asc.swift`, `Scripts/sillfeed.py` | the fork's repository, no upstream links or email |
| `.github/` | `FUNDING.yml` removed; issue templates point at the fork |
| `Sources/SillMenuBar/DebugHooks.swift`, `Tests/checks/update-policy/` | the fork's release pages in previews and tests; tests that refuse upstream's pages |
| `Tests/checks/fork-hosts/` | the check below |
| `FORK.md`, `AGENTS.md`, the first block of `CLAUDE.md` | these rules |

Add a row whenever the fork changes something new.

## 4. The check, after every merge

```
Tests/checks/fork-hosts/run.sh      # this file's rules: fails on any upstream or outside address
Tests/checks/run-all.sh             # every check (CI runs both)
```

Both must pass before anything is merged or built. Never weaken `fork-hosts` to make a merge pass;
change it only to add a new fork value, with the owner's yes.

## 5. Identifiers, not servers

The bundle IDs (`me.saffer.sill`, `me.saffer.sill.mac`) and upstream's team ID in the Xcode project
are identifiers, not places the apps contact. The owner sets his own team and iOS bundle ID in
Xcode when building; they need not be committed.
