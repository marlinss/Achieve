"""Pair Extraordinaire achievement unlocker.

Like the Pull Shark unlocker, but each commit carries a "Co-authored-by"
trailer. When merged, a co-authored PR counts toward the "Pair Extraordinaire"
achievement for both accounts.

The co-author email MUST be a verified email of a real GitHub account, and that
account should be a collaborator on the repo. See README.md.
"""

import random
import string
import time

import requests

import config


def random_branch_name():
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"pair-extraordinaire-{suffix}"


def run_once(index):
    if not config.COAUTHOR_EMAIL:
        raise SystemExit(
            "GH_COAUTHOR_NAME / GH_COAUTHOR_EMAIL must be set for this script."
        )

    branch = random_branch_name()

    # 1. Branch off the base branch.
    config.create_branch(branch)

    # 2. Commit a change with a co-author trailer.
    sha, content = config.get_file(branch)
    new_content = content + "."
    message = (
        f"chore: pair extraordinaire #{index}\n\n"
        f"Co-authored-by: {config.COAUTHOR_NAME} <{config.COAUTHOR_EMAIL}>"
    )
    config.commit_file(branch, message, new_content, sha)

    # 3. Open and merge the pull request.
    pr_number = config.create_pull_request(branch, f"Pair Extraordinaire #{index}")
    config.merge_pull_request(pr_number)

    print(f"[{index}] merged co-authored PR #{pr_number} from {branch}")


def main():
    print(
        f"Pair Extraordinaire unlocker -> {config.OWNER}/{config.REPO} "
        f"(co-author {config.COAUTHOR_EMAIL}, iterations "
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
