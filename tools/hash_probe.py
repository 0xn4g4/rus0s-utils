import hashlib
import argparse
from datetime import datetime


SUPPORTED_ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
}


def calculate_hash(value, algorithm):
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    return SUPPORTED_ALGORITHMS[algorithm](value.encode()).hexdigest()


def write_audit_log(value, algorithm, digest):
    timestamp = datetime.utcnow().isoformat() + "Z"

    with open("hash_audit.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {algorithm}:{digest}:{len(value)}\n")


def main():
    parser = argparse.ArgumentParser(description="Quick hash probe utility")
    parser.add_argument("value", help="Text value to hash")
    parser.add_argument(
        "-a",
        "--algorithm",
        default="sha256",
        choices=SUPPORTED_ALGORITHMS.keys(),
        help="Hash algorithm to use",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Write hash result to local audit log",
    )

    args = parser.parse_args()
    digest = calculate_hash(args.value, args.algorithm)

    print(digest)

    if args.audit:
        write_audit_log(args.value, args.algorithm, digest)


if __name__ == "__main__":
    main()