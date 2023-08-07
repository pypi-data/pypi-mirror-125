import geopandas
import libpysal
import numpy
import unittest

from spopt.region import MaxPHeuristic


# Mexican states
pth = libpysal.examples.get_path("mexicojoin.shp")
MEXICO = geopandas.read_file(pth)


class TestMaxPHeuristic(unittest.TestCase):
    def setUp(self):

        self.mexico = MEXICO.copy()

        # labels for non-verbose and verbose:
        # count=1, threshold=4, top_n=2
        self.basic_labels = [5, 5, 3, 6, 6, 6, 1, 1, 1, 1, 8, 6, 8, 2, 2, 8]
        self.basic_labels += [2, 8, 7, 7, 2, 7, 5, 3, 3, 5, 3, 4, 4, 4, 4, 7]

        # labels for:
        # count=4, threshold=10, top_n=5
        self.complex_labels = [3, 3, 2, 10, 10, 2, 5, 6, 1, 7, 7, 10, 7, 4, 4]
        self.complex_labels += [6, 4, 6, 1, 1, 9, 9, 3, 8, 8, 2, 2, 2, 5, 8, 5, 9]

        # labels for one variable column:
        # count=1, threshold=5, top_n=5
        self.var1_labels = [3, 3, 6, 2, 2, 2, 2, 4, 2, 4, 5, 2, 5, 1, 1, 5, 1]
        self.var1_labels += [4, 5, 5, 1, 1, 3, 3, 6, 3, 6, 4, 4, 6, 6, 4]

    def test_maxp_heuristic_basic_nonverbose(self):
        self.mexico["count"] = 1
        w = libpysal.weights.Queen.from_dataframe(self.mexico)
        attrs_name = [f"PCGDP{year}" for year in range(1950, 2010, 10)]
        threshold = 4
        top_n = 2
        threshold_name = "count"
        numpy.random.seed(123456)
        args = (self.mexico, w, attrs_name, threshold_name, threshold, top_n)
        model = MaxPHeuristic(*args)
        model.solve()

        numpy.testing.assert_array_equal(model.labels_, self.basic_labels)

    def test_maxp_heuristic_basic_verbose(self):
        self.mexico["count"] = 1
        w = libpysal.weights.Queen.from_dataframe(self.mexico)
        attrs_name = [f"PCGDP{year}" for year in range(1950, 2010, 10)]
        threshold = 4
        top_n = 2
        threshold_name = "count"
        numpy.random.seed(123456)
        args = (self.mexico, w, attrs_name, threshold_name, threshold, top_n)
        model = MaxPHeuristic(*args, verbose=True)
        model.solve()

        numpy.testing.assert_array_equal(model.labels_, self.basic_labels)

    def test_maxp_heuristic_complex(self):
        self.mexico["count"] = 4
        w = libpysal.weights.Queen.from_dataframe(self.mexico)
        attrs_name = [f"PCGDP{year}" for year in range(1950, 2010, 10)]
        threshold = 10
        top_n = 5
        threshold_name = "count"
        numpy.random.seed(1999)
        args = (self.mexico, w, attrs_name, threshold_name, threshold, top_n)
        model = MaxPHeuristic(*args)
        model.solve()

        numpy.testing.assert_array_equal(model.labels_, self.complex_labels)

    def test_maxp_one_var(self):
        self.mexico["count"] = 1
        w = libpysal.weights.Queen.from_dataframe(self.mexico)
        attrs_name = ["PCGDP2000"]
        threshold = 5
        top_n = 5
        threshold_name = "count"
        numpy.random.seed(1999)
        args = (self.mexico, w, attrs_name, threshold_name, threshold, top_n)
        model = MaxPHeuristic(*args)
        model.solve()

        numpy.testing.assert_array_equal(model.labels_, self.var1_labels)
