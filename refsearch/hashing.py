from winnowing import kgrams, select_min, winnowing_hash


def sanitize(text):
    out = []
    for c in text:
        if c.isalpha():
            out.append(c.lower())
    return out


def slow_winnow(text, k=5, w=4):

    text = sanitize(text)
    text = zip(range(len(text)), text)

    hashes = map(lambda x: winnowing_hash(x), kgrams(text, k))
    out = set()

    for window in kgrams(hashes, w):
        out.add(select_min(window))  # FIXME: this is very inefficient

    return out


def winnow(text, k=5, w=4, R=256, mod=21017):
    """
    Go through the text (just **once**) generating a hash
    in a Rabin-Karp way; also implements the efficient
    search for the local hash (taking rightmost value
    when tied). At least one hash will be generated for
    segment of size: k+w-1

    @arg k: int, how big piece of text we should consider
    @kw: w: int, how big a window we are examining
    @kw R: int, alphabet size
    @kw mod: int, this **should** be some large prime number
    """

    text = sanitize(text)

    # we cannot generate a reliable hash so let's give up early...
    if len(text) < k:
        return

    i = 0  # position in the text
    curr_hash = 0
    W = 1
    for _ in range(k - 1):
        W = W * R % mod
    hashes = []
    h = hmin = 0

    # first build one hash (made of first k elements)
    for i in range(k):
        curr_hash = (curr_hash * R + ord(text[i])) % mod

    if i + 1 == len(text):
        yield curr_hash, 0
        return

    # next fill the buffer
    for i in range(i + 1, min(len(text), i + w + 1)):
        x = ((((curr_hash - ord(text[i - k]) * W) % mod) * R) + ord(text[i])) % mod
        hashes.append(x)
        if x < curr_hash:
            hmin = len(hashes) - 1
        curr_hash = x

    # we got at least one minimum
    yield hashes[hmin], hmin

    # main loop: go through remainder and find the local minima
    wi = w - 1
    for i in range(i + 1, len(text)):
        wi += 1
        h = wi % w  # move one position to the right
        curr_hash = ((((curr_hash - ord(text[i - k]) * W) % mod) * R) + ord(text[i])) % mod
        hashes[h] = curr_hash
        # print(text[i - k : i], curr_hash, text[i - k])

        if h == hmin:
            # minimum is no longer in the buffer
            # TODO: we are basically going through the whole buffer
            # could optimize it by remembering previous 1-2 minimums
            # and then if those were exhausted, do the sweep XOR
            # we could simply maintain a priority queue and get
            # stuff out of there; however this starts to matter only
            # when w becomes large (and that actually defeats the
            # purpose of local hashing; would only match big chunks
            # of text)
            jj = 0
            for j in range(1, w):
                left = (wi - j) % w  # look left to find a new minimum
                if hashes[left] < hashes[hmin]:
                    hmin = left
                    jj = j
            yield hashes[hmin], i - k - jj
        else:
            # minimum is still in the buffer
            if curr_hash < hashes[hmin]:
                hmin = h
                yield curr_hash, i - k


def test():
    text = "a do run run run, a do run run"
    s = sanitize(text)
    for hash, pos in winnow(text, k=4, w=3):
        print(hash, pos, "".join(s[pos : pos + 4]))


if __name__ == "__main__":
    test()
