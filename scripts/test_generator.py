from pandas import DataFrame
from unittest import main, mock, TestCase

from generator import Generator


class GeneratorTests(TestCase):

    def setUp(self):
        # setup test data
        self._df = DataFrame({
            "SYMBOL": ["A", "B", "C"],
            "DESC": ["AA", "BB", "CC"],
            "UPLOC": [1, 2, 3]
        })
        self._df["DATE"] = "20190101"

    def test_init(self):
        # test invalid instantiation (not DataFrame)
        with self.assertRaises(TypeError):
            mg = Generator("")

        # test valid instantiation
        mg = Generator(DataFrame())

    @mock.patch("generator.DataFrame.to_csv")
    def test_portfolio(self, mock_to_csv):
        mg = Generator(self._df)

        # test invalid columns parameter (not list)
        with self.assertRaises(TypeError):
            mg.portfolio("filepath", {"foo", "bar"})

        # test valid call
        mg.portfolio("filepath")

        # test valid call (with columns parameter)
        mg.portfolio("filepath", ["SYMBOL", "DESC", "UPLOC"])

    @mock.patch("generator.DataFrame.to_csv")
    def test_timeseries(self, mock_to_csv):
        mg = Generator(self._df)

        # test invalid columns parameter (not list)
        with self.assertRaises(TypeError):
            mg.timeseries("filepath", "")

        # test to_csv called
        mg.timeseries("filepath", ["UPLOC"])
        mock_to_csv.assert_called_once()

    # test properties
    @mock.patch("generator.DataFrame.to_csv")
    def test_properties(self, mock_to_csv):
        mg = Generator(self._df)

        # test invalid columns parameter (not list)
        with self.assertRaises(TypeError):
            mg.properties("filepath", "")

        # test to_csv called
        mg.properties("filepath", ["DESC"])
        mock_to_csv.assert_called_once()


if __name__ == "__main__":
    main()