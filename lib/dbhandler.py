#
# Created by LokiLuciferase on 03/10/2017.
#

import sqlite3
import os

from data.schema import schema

# encapsulates methods and data of database
class LabelBase:
    def __init__(self, location, create_new=False):
        # Declare db schema here
        self.schema = schema
        self.location = location
        # if db file does not exist, make new one with the given schema
        if not os.path.exists(location):
            if not create_new:
                raise RuntimeError("No database file found at this location.")
            self.db, self.cursor = self.connect(self.location)
            self.create_scheme()
        else:
            self.db, self.cursor = self.connect(self.location)

    # connect with db and close afterwards
    def connect(self, loc):
        con = sqlite3.connect(loc)
        c = con.cursor()
        return con, c

    def close(self):
        self.db.close()

    # make schema as determined by self.schema
    def create_scheme(self):

        for t in self.schema:
            # add primary key and its data type
            self.cursor.execute("CREATE TABLE {tname} ({pk} {pk_type} PRIMARY KEY)"
                      .format(tname=t["tname"], pk=t["pk"][0], pk_type=t["pk"][1]))
            # add further columns
            for f in t["fields"]:
                self.cursor.execute("ALTER TABLE {sp} ADD COLUMN '{fieldname}' {fieldtype}"
                                    .format(sp=t["tname"],
                                            fieldname=f[0],
                                            fieldtype=f[1]))
        self.db.commit()

    # add new entry to selected table
    def add_row(self, tablename, insertdic, pk="speziesname_de"):
        pkey_name = pk
        pkval = insertdic[pkey_name]
        itup = insertdic.items()
        colnames = ", ".join([col for col, val in itup])
        colvals = ", ".join(["'%s'" % val for col, val in itup])

        try:
            self.cursor.execute("INSERT INTO {tname} ({cnames}) VALUES ({cvals})"
                      .format(tname=tablename,
                              cnames=colnames,
                              cvals=colvals))
            self.db.commit()
            return "Entry {pkey} added.".format(pkey=pkval)

        except sqlite3.IntegrityError:
            # if entry exists, update with given entry
            for tup in itup:
                self.cursor.execute("UPDATE {tname} SET {cname}=('{cval}') WHERE {pkey}=('{pkv}')"
                          .format(tname=tablename,
                                  cname=tup[0],
                                  cval=tup[1],
                                  pkey=pkey_name,
                                  pkv=pkval))
            self.db.commit()
            return "Entry updated: {pkey}".format(pkey=pkval)

    # get entry from table 'Spezies' by speciesname. can be abused to get other primary keys from other table.
    def get_entry(self, keyname, tablename="Spezies", primkey="speziesname_de"):

        self.cursor.execute("SELECT * FROM {tname} WHERE {pk}='{kname}'"
                            .format(tname=tablename,
                                    pk=primkey,
                                    kname=keyname))
        item = self.cursor.fetchone()
        if item:
            return item
        raise RuntimeError("No item was found with this primary key.")
