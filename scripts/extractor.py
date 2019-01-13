from pandas import DataFrame, read_csv
from os import path


# define directories
#TODO supply args using argparse?
_ROOT_DIR = path.dirname(path.dirname(__file__))
_FILES_DIR = path.join(_ROOT_DIR, "files")
_SOURCE_DIR = path.join(_FILES_DIR, "source")
_TARGET_DIR = path.join(_FILES_DIR, "target")


class Generator:

    def __init__(self, dataframe):
        if not isinstance(dataframe, DataFrame):
            raise TypeError("expecting DataFrame object for 'dataframe' variable")

        self.df = dataframe

    def portfolio(self, file, columns=None):
        if not isinstance(columns, list):
            raise TypeError("expecting list object for 'columns' variable")

        if columns:
            self.df.to_csv(file, sep="\t", index=False, columns=columns)
        else:
            self.df.to_csv(file, sep="\t", index=False)

    def timeseries(self, file, items):
        if not isinstance(items, list):
            raise TypeError("expecting list object for 'items' variable")

        # create local copy of dataframe object (to avoid changing the original)
        df = self.df.copy()

        # check CCY in dataframe else add a placeholder (as export will error)
        if "CURRENCY" not in df.index:
            df["CURRENCY"] = None

        # master dataframe to store all output
        mdf = DataFrame()

        # create item dataframe and append to master
        for item in items:
            #TODO not working
            # # check item exists in dataframe
            # if not item in df.index:
            #     continue

            idf = df[["SYMBOL", "DATE", "CURRENCY", item]].copy()
            idf["ITEM"] = item
            idf = idf.rename(columns={item: "VALUE"})
            #TODO remove rows with no value
            mdf = mdf.append(idf)

        if not mdf.empty:
            # sort dataframe for ease when loading into SQL
            mdf = mdf.sort_values(["ITEM", "SYMBOL"])

            # output dataframe to file
            mdf.to_csv(file, sep="\t", index=False, header=False, columns=["ITEM", "SYMBOL", "DATE", "VALUE", "CURRENCY"])

    def properties(self, file, items):
        if not isinstance(items, list):
            raise TypeError("expecting list object for 'items' variable")

        # create local copy of dataframe object (to avoid changing the original)
        df = self.df.copy()

        # master dataframe to store all output
        mdf = DataFrame()

        # create item dataframe and append to master
        for item in items:
            # TODO not working
            # # check item exists in dataframe
            # if not item in df.index:
            #     continue

            idf = df[["SYMBOL", "DATE", item]].copy()
            idf["ITEM"] = item
            idf = idf.rename(columns={item: "VALUE"})
            # TODO remove rows with no value
            mdf = mdf.append(idf)

        if not mdf.empty:
            # sort dataframe for ease when loading into SQL
            mdf = mdf.sort_values(["SYMBOL", "ITEM", "DATE"])

            # output dataframe to file
            mdf.to_csv(file, sep="\t", index=False, header=False, columns=["ITEM", "SYMBOL", "DATE", "VALUE"])


if __name__ == "__main__":
    # define source file
    filename = "cons20190110.csv"
    file = path.join(_SOURCE_DIR, filename)
    if not path.isfile(file):
        raise FileNotFoundError(file)

    # load data into dataframe
    df = read_csv(file)

    # remap column names
    mapping = {
        "Identifier": "SYMBOL",
        "Constituent": "DESC",
        "Country Code": "COUNTRY2",
        "ISO Code": "COUNTRY3",
        "Exchange Code": "XCHANGE",
        "Price": "PRICE",
        "Shares in Issue": "SHARES",
        "Weighting": "WEIGHT",
        # "Industry": "",
        # "Supersector": "",
        # "Sector": "",
        # "Subsector": "",
    }
    df = df.rename(columns=mapping)

    # add date
    df["DATE"] = "20190110" #TODO read from filename

    # create time series
    df["PR"] = df["PRICE"]
    df["SH"] = df["SHARES"]
    df["WE"] = df["WEIGHT"]

    # instantiate generator
    g = Generator(df)

    # create portfolio
    port_columns = ["SYMBOL", "DATE", "DESC", "SEDOL", "ISIN", "CUSIP", "COUNTRY2", "COUNTRY3", "PRICE", "SHARES", "WEIGHT"]
    port_filename = "PORT.tsv"
    port_file = path.join(_TARGET_DIR, port_filename)
    g.portfolio(port_file, columns=port_columns)

    # create time series
    time_items = ["PR", "SH", "WE"]
    time_filename = "TIME.tsv"
    time_file = path.join(_TARGET_DIR, time_filename)
    g.timeseries(time_file, items=time_items)

    # create properties
    prop_items = ["DESC", "SEDOL", "ISIN", "CUSIP", "COUNTRY2", "COUNTRY3"]
    prop_filename = "PROP.tsv"
    prop_file = path.join(_TARGET_DIR, prop_filename)
    g.properties(prop_file, items=prop_items)
