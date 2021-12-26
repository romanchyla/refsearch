# Local Hashing

Impl of the following paper: https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf

The idea is to generate (efficiently) small number of context dependent fingerprint signatures. So for example:

    Doe, J; Journal of Astrophysics; 2015

Will produce (not all, but quite a few) of the same signatures as:

    Journal of Astrophysics. John Doe. 2015

NOTE: the input is sanitized - we'll remove all punctions (basically we only care for alphanums and their order; but only localized order). Everything is also lowercased.

    journalofastrophysicsjohndoe2015
    doejjournalofastrophysics2015

The important parameters are:

- `k` : which governs the length of the n-gram; basically we are going to generate n-grams from the text (actually not n-grams, but just hashes of those ngrams and in `O(1)` time per one hash; so the whole business of creating hashes is `O(n)` where `n` is the lenght of the passed in text)
- `w` : length of the window from which fingerprints are selected. Bigger values mean bigger segment of the text (i.e. bigger gaps between signatures) - experimentation will tell us what are the right values. WARNING: large `w` may lead to slow processing because in the worst case, the runtime (of the whole winnowing) is `O(w*n)`


## Next Steps

Collect reference (texts) and generate fingerprints; try to see what is their frequencies and how many we need per one reference (with varied w/k params). Also what is the rate of success matching.

Next next is to see if we can use postgres (index) to afficiently search for those fingerprints. And then compute some measure of similarity between the input and what we have in our database. And see how many references we can successfully identify this way.

Next next next:
 - implement finite state transducers
 - fuzzy matching
 - tries
 - maybe heuristics on authors

After that, more heaveweight (but still light) tools need to kick in:

 - decision trees?
 - classification forests?
