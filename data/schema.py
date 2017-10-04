#
# Created by LokiLuciferase on 03/10/2017.
#

schema = [
            {"tname" : "Spezies",
             "pk"    : ("speziesname_de", "TEXT"),
             "fields": [("speziesname_la", "TEXT"),
                        ("min_wuchshoehe", "INTEGER"),
                        ("max_wuchshoehe", "INTEGER"),
                        ("bluete", "TEXT"),
                        ("bluetezeit", "TEXT"),
                        ("standort", "TEXT"),
                        ("besonderheiten", "TEXT"),
                        ("preis", "REAL"),
                        ("foto", "TEXT")]
             },
        ]