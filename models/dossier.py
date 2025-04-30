from baseObject import baseObject

class dossier(baseObject):
    def __init__(self):
        self.tn = "dossiers"           # table name
        self.pk = "dossier_id"         # primary key
        self.data = []
        self.errors = []
        self.fields = []
        self.setup()                   # initialize DB connection and schema
