#
# Created by LokiLuciferase on 03/10/2017.
#

import os
import sys

from lib.dbhandler import LabelBase
from testing.testdata import testdata

sys.path.insert(0, sys.path[0])


def main():

    lbase = LabelBase("./data/label_database.sqlite", create_new=True)

    for testitem in testdata:
        print(lbase.add_row(tablename="Spezies", insertdic=testitem))

    try:
        print(lbase.get_entry("Borsten-Schwertlilie"))
    except RuntimeError as e:
        print(e)

    print("That's all, folks!")
    lbase.close()


if __name__ == "__main__":

    main()
