
import email
import re
from collections import Counter
from email.policy import default
from pathlib import Path

from tqdm import tqdm


# https://stackoverflow.com/a/59682472/6890681
class MboxReader:
    def __init__(self, filename):
        self.handle = open(filename, 'rb')
        assert self.handle.readline().startswith(b'From ')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.handle.close()

    def __iter__(self):
        return iter(self.__next__())

    def __next__(self):
        lines = []
        while True:
            line = self.handle.readline()
            if line == b'' or line.startswith(b'From '):
                yield email.message_from_bytes(b''.join(lines), policy=default)
                if line == b'':
                    break
                lines = []
                continue
            if line.startswith(b'>') and line.lstrip(b'>').startswith(b'From '):
                line = line[1:]
            lines.append(line)


def main():
    print_most_common_senders()
    print_names_and_emails_from_senders()


def print_most_common_senders():
    # print("opening mbox file")
    # mbox = mailbox.mbox("/mnt/c/Users/cpmqa/Downloads/Unread-001.mbox")

    print("counting senders")
    sender_counts = Counter()
    with MboxReader("data/Unread-001.mbox") as mbox:
        with tqdm(total=39629) as progress:
            for message in mbox:
                sender_counts.update([message["from"]])
                progress.update()

    # print("counting senders")
    # sender_counts = Counter()
    # with tqdm(total=50000) as progress:
    #     for message in mbox:
    #         sender_counts.update([message["from"]])
    #         progress.update()

    print("writing sender counts")
    outdir = Path("out")
    outdir.mkdir(exist_ok=True)
    outfile = outdir / "senders.txt"

    with open(outfile, "w+") as f:
        for sender, count in sender_counts.most_common():
            f.write(f"[{count}] {sender}\n")


def print_names_and_emails_from_senders():
    senders_file = Path("out/senders.txt")
    assert senders_file.exists()

    with open(senders_file, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    email_counts = Counter()
    p1 = re.compile("^\[(\d+)\].*<(.*)>")
    p2 = re.compile("^\[(\d+)\].* (.*)")

    for line in lines:
        m = p1.match(line) or p2.match(line)
        assert m is not None, f"{line=}"

        count = int(m.group(1))
        email_ = m.group(2)
        email_counts[email_] += count

    print("writing email counts")
    outdir = Path("out")
    outdir.mkdir(exist_ok=True)
    outfile = outdir / "emails.txt"

    with open(outfile, "w+") as f:
        for email_, count in email_counts.most_common():
            f.write(f"[{count}] {email_}\n")


if __name__ == "__main__":
    main()
