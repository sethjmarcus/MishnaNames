import re
import unicodedata
from pathlib import Path
from Trie import Trie

FINAL_MAP = str.maketrans({
    'ך': 'כ',
    'ם': 'מ',
    'ן': 'נ',
    'ף': 'פ',
    'ץ': 'צ',
})

def normalize_hebrew(s):
    s = unicodedata.normalize("NFKD", s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^א-ת\s]', '', s)
    return s.translate(FINAL_MAP)


trie = Trie()

names = []

for line in Path("names.txt").read_text(encoding="utf-8").splitlines():

    name = normalize_hebrew(line.strip())

    if not name:
        continue

    names.append(name[::-1])
    trie.insert(name[::-1])


mishnas = []

for path in sorted(Path("mishnayot").glob("*.txt")):

    text = normalize_hebrew(
        path.read_text(encoding="utf-8")
    ).strip()

    if not text:
        continue

    first_word = text.split()[0]
    #print(first_word)
    mishnas.append({
        "file": path.name,
        "first_word": first_word,
        "initial": first_word[0],
    })


results = []

N = len(mishnas)

for start in range(N):

    node = trie.root
    pos = start

    while pos < N:

        ch = mishnas[pos]["initial"]

        if ch not in node.children:
            break

        node = node.children[ch]

        # emit all matching names
        for matched_name in node.names:

            results.append({
                "name": matched_name,
                "start": start,
                "end": pos,
                "mishnas": mishnas[start:pos+1]
            })

        pos += 1


for r in results:

    print("\nFOUND:", r["name"])

    for m in r["mishnas"]:
        print(
            m["file"],
            "->",
            m["first_word"]
        )