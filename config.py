"""Shared configuration and GitHub API helpers.

Loads settings from a local .env file (see .env.example) and exposes small
wrappers around the GitHub REST API used by both unlocker scripts.
"""

import base64
import os
import sys

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # dotenv is optional; env vars still work without it
    pass

API_ROOT = "https://api.github.com"


def _require(name):
    value = os.getenv(name)
    if not value:
        sys.exit(
            f"Missing required setting '{name}'. "
            "Copy .env.example to .env and fill it in."
        )
    return value


# --- Settings -------------------------------------------------------------
TOKEN = _require("GH_TOKEN")
OWNER = _require("GH_OWNER")
REPO = _require("GH_REPO")
FILENAME = os.getenv("GH_FILENAME", "README.md")
BASE_BRANCH = os.getenv("GH_BASE_BRANCH", "main")
INTERVAL = int(os.getenv("GH_INTERVAL", "10"))
ITERATIONS = int(os.getenv("GH_ITERATIONS", "5"))

COAUTHOR_NAME = os.getenv("GH_COAUTHOR_NAME", "")
COAUTHOR_EMAIL = os.getenv("GH_COAUTHOR_EMAIL", "")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


# --- API helpers ----------------------------------------------------------
def repo_url(path):
    return f"{API_ROOT}/repos/{OWNER}/{REPO}{path}"


def get_file(branch):
    """Return (sha, decoded_text) for FILENAME on the given branch."""
    resp = requests.get(
        repo_url(f"/contents/{FILENAME}"),
        headers=HEADERS,
        params={"ref": branch},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return data["sha"], content


def get_branch_sha(branch):
    """Return the commit SHA the given branch points to."""
    resp = requests.get(
        repo_url(f"/git/ref/heads/{branch}"), headers=HEADERS, timeout=30
    )
    resp.raise_for_status()
    return resp.json()["object"]["sha"]


def create_branch(new_branch, base_branch=None):
    """Create new_branch pointing at the tip of base_branch."""
    base_sha = get_branch_sha(base_branch or BASE_BRANCH)
    resp = requests.post(
        repo_url("/git/refs"),
        headers=HEADERS,
        json={"ref": f"refs/heads/{new_branch}", "sha": base_sha},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def commit_file(branch, message, new_content, sha):
    """Update FILENAME on branch with new_content."""
    encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    resp = requests.put(
        repo_url(f"/contents/{FILENAME}"),
        headers=HEADERS,
        json={
            "message": message,
            "content": encoded,
            "sha": sha,
            "branch": branch,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def create_pull_request(head, title, base=None):
    resp = requests.post(
        repo_url("/pulls"),
        headers=HEADERS,
        json={
            "title": title,
            "head": head,
            "base": base or BASE_BRANCH,
            "body": "Automated pull request.",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["number"]


def merge_pull_request(pr_number):
    resp = requests.put(
        repo_url(f"/pulls/{pr_number}/merge"),
        headers=HEADERS,
        json={"merge_method": "merge"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
