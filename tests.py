
import unittest
import bibtex

class BibTeXTests(unittest.TestCase):

    def setUp(self):
        with open("test/ocean.bib") as f:
            self.entries0 = bibtex.readentries(f)
        with open("test/glacier.bib") as f:
            self.entries1 = bibtex.readentries(f)
        pass

    def test_parser(self):
        s = "Author = {Wilson, N.J. and Flowers, G.F.}"
        self.assertEqual(bibtex.parseline(s),
                         ("Author", "Wilson, N.J. and Flowers, G.F."))

        s = "Year = {2011}"
        self.assertEqual(bibtex.parseline(s),
                         ("Year", 2011))

        # When the year isn't an integer, the correct result is 'None'
        s = "Year = {2003a}"
        self.assertEqual(bibtex.parseline(s),
                         ("Year", None))
        return

    def test_readentries(self):
        self.assertEqual(len(self.entries0), 14)
        self.assertEqual(len(self.entries1), 368)
        return

    def test_scan(self):
        res = bibtex.scan(self.entries1,
                          lambda a: a.year == 2013)
        self.assertEqual(len(res), 7)

        res = bibtex.scan(self.entries1,
                          lambda a: a.year == 2012,
                          lambda a: "Aschwanden" in a.author)
        self.assertEqual(len(res), 1)
        return

if __name__ == "__main__":
    unittest.main()


