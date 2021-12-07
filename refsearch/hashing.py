from winnowing import kgrams, select_min, winnowing_hash


def sanitize(text):
    out = []
    for c in text:
        if c.isalpha():
            out.append(c.lower())
    return out


def winnow(text, k=5, w=4):

    text = sanitize(text)
    text = zip(range(len(text)), text)

    hashes = map(lambda x: winnowing_hash(x), kgrams(text, k))
    out = set()
    for window in kgrams(hashes, w):
        out.add(select_min(window))  # FIXME: this is very inefficient

    return out
