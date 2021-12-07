from refsearch import hashing


def test_winnow():
    sample = "A black \ncat \tjumped   over FOX"
    assert hashing.sanitize(sample) == [
        "a",
        "b",
        "l",
        "a",
        "c",
        "k",
        "c",
        "a",
        "t",
        "j",
        "u",
        "m",
        "p",
        "e",
        "d",
        "o",
        "v",
        "e",
        "r",
        "f",
        "o",
        "x",
    ]

    s1 = hashing.winnow(sample)
    s2 = hashing.winnow("jumped over fox a black cat")

    t1 = set([x[1] for x in s1])
    t2 = set([x[1] for x in s2])

    assert len(t1) == len(t2) == 8
    common = t1.intersection(t2)
    assert len(common) == 6
    assert common == set({11809, 1346, 34977, 8935, 11180, 22966})


if __name__ == "__main__":
    test_winnow()
