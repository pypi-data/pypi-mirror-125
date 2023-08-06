class KeyCounter:

    def __init__(self, counts: dict):
        if not isinstance(counts, dict):
            raise ValueError("Storage path for key counting must be dict.")
        self.counts = counts

    def _increase(self, key):
        if key not in self.counts:
            self.counts[key] = 0
        self.counts[key] += 1

    def count(self, key):
        if not isinstance(key, list) and not isinstance(key, str):
            raise ValueError("Keys to count must be either list of strings or string {} given".format(type(key)))

        if isinstance(key, list):
            for k in key:
                self._increase(k)
        else:
            self._increase(key)
