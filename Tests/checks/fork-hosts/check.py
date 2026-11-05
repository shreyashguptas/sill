"""FORK.md's hard rule: no upstream repository, website or outside server in the fork's code.

Scans every tracked file under Sources, iOSClient, Packaging, Scripts, .github and Package.swift
(the code the apps run, how they are built, and what CI and the release scripts publish to).
Docs, the site/ folder, README.md, CLAUDE.md and LICENSE are upstream's words and are not scanned.
"""
import pathlib, re, subprocess, sys

FORK = "shreyashguptas/sill"
root = pathlib.Path(sys.argv[1])
scanned = ["Sources", "iOSClient", "Packaging", "Scripts", ".github", "Package.swift"]
files = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", *scanned],
                       capture_output=True, check=True).stdout.decode().split("\0")
files = [f for f in files if f]

failures, checks = [], 0
def check(ok, what):
    global checks
    checks += 1
    if not ok:
        failures.append(what)
        print(f"FAIL: {what}")

URL = re.compile(r"\b[a-z][a-z0-9+.-]*://([^\s\"'`<>)\],]*)", re.I)
LOCAL = {"localhost", "127.0.0.1", "::1", "[::1]", "0.0.0.0"}
# Words that name upstream's places: its GitHub owner, its website and its TestFlight beta.
FORBIDDEN = [re.compile(p, re.I) for p in (r"saffsanity", r"getsill\.app", r"testflight\.apple\.com/join/")]

def allowed(rest: str, scheme: str) -> bool:
    if scheme.lower() not in ("http", "https", "ws", "wss"):
        return True                      # sill://, x-apple.systempreferences:, file:// and the like
    rest = rest.replace("\\.", ".").rstrip(".;:")   # a regex's `\.`, a sentence's full stop
    host = rest.split("/", 1)[0].split("?", 1)[0]
    path = "/" + rest.split("/", 1)[1] if "/" in rest else "/"
    h = host.lower().split("@")[-1]
    h = h.rsplit(":", 1)[0] if h.count(":") == 1 else h
    if not re.search(r"[a-z0-9]\.[a-z]", h) and h not in LOCAL:
        return True                      # not a host: `https://}` in shell, `https://apps\.` in a regex
    if h in LOCAL or h.startswith("127."):
        return True
    if h == "apple.com" or h.endswith(".apple.com"):
        return True                      # Apple's own: plist DTDs, App Store Connect, example store links
    if h in ("github.com", "api.github.com"):
        p = path.lower()
        if p in ("/", ""):
            return True                  # the bare host, in comments
        if "$" in p or "\\(" in p:
            return True                  # a repository from a variable; its default is checked below
        return p.startswith(f"/{FORK}") or p.startswith(f"/repos/{FORK}")
    return False

for f in files:
    path = root / f
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        continue                         # images and other binaries
    clean = True
    for n, line in enumerate(text.splitlines(), 1):
        for m in URL.finditer(line):
            scheme = m.group(0).split("://", 1)[0]
            check(allowed(m.group(1), scheme), f"{f}:{n}: names an outside address: {m.group(0)}")
        for pat in FORBIDDEN:
            if pat.search(line):
                clean = False
                print(f"FAIL: {f}:{n}: names upstream ({pat.pattern}): {line.strip()[:120]}")
    check(clean, f"{f} names no upstream place")

def read(rel):
    return (root / rel).read_text(encoding="utf-8")

# The places that decide where the apps and scripts go, each pinned to the fork.
check(f'static let repo = "{FORK}"' in read("Sources/SillMenuBar/UpdatePolicy.swift"),
      "UpdatePolicy.repo is the fork: the Mac app's update check reads only the fork's releases")
check('static let feed = URL(string: "https://api.github.com/repos/\\(repo)/releases/latest")!' in read("Sources/SillMenuBar/UpdatePolicy.swift"),
      "UpdatePolicy.feed is built from UpdatePolicy.repo")
check('hasPrefix("/\\(repo)/releases/")' in read("Sources/SillMenuBar/UpdatePolicy.swift"),
      "UpdatePolicy.releasePage opens only the fork's release pages")
check(f'static let site = URL(string: "https://github.com/{FORK}")!' in read("iOSClient/SillLinks.swift"),
      "SillLinks.site is the fork's repository: the iPad app's footer links go there")
check('static let appStoreText = "APP_STORE_URL_PLACEHOLDER"' in read("iOSClient/SillLinks.swift"),
      "SillLinks.appStoreText is the placeholder: the fork has no App Store page, so no store link shows")
check(f"feed_repo={FORK}\n" in read("Scripts/release.sh"),
      "release.sh's default repository is the fork")

# No outside code is pulled into a build: no package dependencies, no build-time scripts.
pkg = read("Package.swift")
check(".package(" not in pkg, "Package.swift has no package dependencies")
pbx = read("iOSClient/Sill.xcodeproj/project.pbxproj")
check("XCRemoteSwiftPackageReference" not in pbx, "the Xcode project has no remote Swift packages")
check("PBXShellScriptBuildPhase" not in pbx, "the Xcode project runs no script at build time")
check(not (root / "Package.resolved").exists(), "no Package.resolved (no remote dependencies)")

print(f"{checks} checks, {len(failures)} failed")
sys.exit(1 if failures else 0)
