"""Pull Shark achievement unlocker.

Repeatedly creates a branch, tweaks a file, opens a pull request, and merges it.
Each merged PR counts toward GitHub's "Pull Shark" achievement.

Run against a repository you own, using your own token. See README.md.
"""

import time
from datetime import datetime

import requests

import config


def run_once(index):
    branch = f"pull-shark-{datetime.now().strftime('%Y%m%d%H%M%S')}-{index}"

    # 1. Branch off the base branch.
    config.create_branch(branch)

    # 2. Modify the file on the new branch.
    sha, content = config.get_file(branch)
    new_content = content + "."
    config.commit_file(branch, f"chore: pull shark #{index}", new_content, sha)

    # 3. Open a pull request.
    pr_number = config.create_pull_request(branch, f"Pull Shark #{index}")

    # 4. Merge it.
    config.merge_pull_request(pr_number)

    print(f"[{index}] merged PR #{pr_number} from {branch}")


def main():
    print(
        f"Pull Shark unlocker -> {config.OWNER}/{config.REPO} "
        f"(interval {config.INTERVAL}s, iterations "
        f"{config.ITERATIONS or 'infinite'})"
    )
    index = 1
    try:
        while config.ITERATIONS == 0 or index <= config.ITERATIONS:
            try:
                run_once(index)
                index += 1
            except requests.HTTPError as exc:
                resp = exc.response
                print(f"HTTP {resp.status_code}: {resp.text[:200]}")
                print("Retrying in 60s...")
                time.sleep(60)
                continue
            time.sleep(config.INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped.")
    print("Done.")


if __name__ == "__main__":
    main()
