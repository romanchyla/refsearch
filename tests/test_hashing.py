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

    s1 = hashing.slow_winnow(sample)
    s2 = hashing.slow_winnow("jumped over fox a black cat")

    t1 = set([x[1] for x in s1])
    t2 = set([x[1] for x in s2])

    assert len(t1) == len(t2) == 8
    common = t1.intersection(t2)
    assert len(common) == 6
    assert common == set({11809, 1346, 34977, 8935, 11180, 22966})


def test_fast_winnow():

    assert list(hashing.winnow("aaa", k=4, w=3)) == []
    assert list(hashing.winnow("aaaa", k=4, w=3)) == [(15378, 0)]
    assert list(hashing.winnow("aaaaa", k=4, w=3)) == [(15378, 0)]
    assert list(hashing.winnow("aaaaaa", k=4, w=3)) == [(15378, 0)]

    assert list(hashing.winnow("a do run run run, a do run run", k=4, w=3)) == [
        (8439, 0),
        (15754, 1),
        (10104, 4),
        (10104, 7),
        (5542, 10),
        (5417, 11),
        (8439, 12),
        (15754, 13),
        (10104, 16),
    ]


if __name__ == "__main__":
    test_winnow()
