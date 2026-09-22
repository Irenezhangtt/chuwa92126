#!/usr/bin/env python3
"""Build the homework submission table from this repo's pull requests.

Usage:
    python .github/scripts/hwcal.py [owner/repo] [--readme README.md] [--csv out.csv]

The repo defaults to $GITHUB_REPOSITORY. Set GITHUB_TOKEN to avoid the
60 requests/hour limit for anonymous API calls. Only the standard library is used.
"""
import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
START = "<!-- SUBMISSIONS:START -->"
END = "<!-- SUBMISSIONS:END -->"
HEADER = ["GitHub", "Student Name", "HW", "PR Status", "Submitted At", "PR URL"]
# When a student opens several PRs for the same HW, keep the best status, then the newest.
STATUS_RANK = {"merged": 2, "open": 1, "closed": 0}
TEMPLATE_PREFIX = "firstname_lastname"


def get(path, token, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": "hwcal"}
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        sys.exit(f"GitHub API returned {e.code} for {url}: {body}")


def fetch_prs(repo, token):
    prs, page = [], 1
    while True:
        data = get(f"/repos/{repo}/pulls", token, {"state": "all", "per_page": 100, "page": page})
        if not data:
            return prs
        prs += data
        page += 1


def parse_hw(*texts):
    for text in texts:
        m = re.search(r"hw[\s_-]?(\d+)", text, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def name_from_branch(head_ref):
    if "/" not in head_ref:
        return ""
    prefix = head_ref.split("/")[0]
    if prefix.lower() == TEMPLATE_PREFIX or not re.search(r"[_-]", prefix):
        return ""
    return " ".join(p.capitalize() for p in re.split(r"[_-]+", prefix) if p)


def md_cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_rows(prs, token):
    profile_names = {}

    def profile_name(login):
        if login not in profile_names:
            profile_names[login] = get(f"/users/{login}", token).get("name") or ""
        return profile_names[login]

    best = {}
    for pr in prs:
        login = pr["user"]["login"]
        head_ref = pr["head"]["ref"]
        hw = parse_hw(head_ref, pr["title"])
        if pr["state"] == "open":
            status = "open"
        elif pr["merged_at"]:
            status = "merged"
        else:
            status = "closed"
        row = {
            "login": login,
            "name": name_from_branch(head_ref),
            "hw": hw,
            "status": status,
            "created": pr["created_at"][:19].replace("T", " "),
            "url": pr["html_url"],
        }
        # PRs without a recognisable HW number are all kept so they can be fixed by hand.
        key = (login, hw) if hw is not None else (login, pr["number"])
        cur = best.get(key)
        if cur is None or (STATUS_RANK[status], row["created"]) > (
            STATUS_RANK[cur["status"]],
            cur["created"],
        ):
            best[key] = row

    rows = list(best.values())
    # Fill missing names from the same student's other PRs, then from their GitHub profile.
    known = {r["login"]: r["name"] for r in rows if r["name"]}
    for row in rows:
        if not row["name"]:
            row["name"] = known.get(row["login"]) or profile_name(row["login"])
    rows.sort(key=lambda r: (r["login"].lower(), r["hw"] if r["hw"] is not None else 10**9))
    return rows


def to_table(rows):
    lines = [
        "| " + " | ".join(HEADER) + " |",
        "|" + "|".join("-" * (len(h) + 2) for h in HEADER) + "|",
    ]
    for r in rows:
        hw = f"hw{r['hw']}" if r["hw"] is not None else "?"
        cells = [r["login"], r["name"] or "?", hw, r["status"], r["created"]]
        lines.append(
            "| " + " | ".join(md_cell(c) for c in cells) + f" | [link]({r['url']}) |"
        )
    return "\n".join(lines)


def update_readme(path, table):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if START not in text or END not in text:
        sys.exit(f"{path} is missing the {START} / {END} markers")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    new = f"{before}{START}\n{table}\n{END}{after}"
    if new != text:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
        return True
    return False


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for r in rows:
            hw = f"hw{r['hw']}" if r["hw"] is not None else ""
            w.writerow([r["login"], r["name"], hw, r["status"], r["created"], r["url"]])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default=os.environ.get("GITHUB_REPOSITORY"))
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--csv")
    args = ap.parse_args()
    if not args.repo:
        ap.error("repo is required (owner/repo) when GITHUB_REPOSITORY is not set")

    token = os.environ.get("GITHUB_TOKEN")
    rows = build_rows(fetch_prs(args.repo, token), token)

    changed = update_readme(args.readme, to_table(rows))
    print(f"{len(rows)} submissions; {args.readme} {'updated' if changed else 'unchanged'}")
    if args.csv:
        write_csv(args.csv, rows)
        print(f"Wrote {args.csv}")


if __name__ == "__main__":
    main()
