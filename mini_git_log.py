#!/usr/bin/env python3

import os
import zlib

GIT_DIR = ".git"
OBJECTS_DIR = os.path.join(GIT_DIR, "objects")


def read_object(hash_id):
    path = os.path.join(OBJECTS_DIR, hash_id[:2], hash_id[2:])

    with open(path, "rb") as f:
        compressed = f.read()

    raw = zlib.decompress(compressed)
    header, content = raw.split(b"\x00", 1)

    obj_type = header.split()[0].decode()
    return obj_type, content


def get_head_commit():
    with open(os.path.join(GIT_DIR, "HEAD"), "r") as f:
        head = f.read().strip()

    if head.startswith("ref:"):
        ref_path = head.split(" ", 1)[1]
        with open(os.path.join(GIT_DIR, ref_path), "r") as f:
            return f.read().strip()

    return head


def parse_commit(content):
    text = content.decode(errors="ignore")
    header_part, message = text.split("\n\n", 1)

    parents = []
    author = ""
    tree = ""

    for line in header_part.splitlines():
        if line.startswith("tree "):
            tree = line.split(" ", 1)[1]
        elif line.startswith("parent "):
            parents.append(line.split(" ", 1)[1])
        elif line.startswith("author "):
            author = line.split(" ", 1)[1]

    first_message_line = message.splitlines()[0] if message.splitlines() else ""

    return {
        "tree": tree,
        "parents": parents,
        "author": author,
        "message": first_message_line
    }


def mini_log():
    current = get_head_commit()

    while current:
        obj_type, content = read_object(current)

        if obj_type != "commit":
            print(f"ERROR: {current} is not a commit object")
            break

        commit = parse_commit(content)

        short_hash = current[:7]
        print(f"{short_hash} {commit['message']}")

        if commit["parents"]:
            current = commit["parents"][0]
        else:
            current = None


if __name__ == "__main__":
    if not os.path.isdir(GIT_DIR):
        print("ERROR: Not inside a Git repository")
        exit(1)

    mini_log()
