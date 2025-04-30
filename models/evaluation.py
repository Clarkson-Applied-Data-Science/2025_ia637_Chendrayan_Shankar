from baseObject import baseObject

class evaluation(baseObject):
    def __init__(self):
        self.tn = "evaluations"          # Table name
        self.pk = "evaluation_id"        # Primary key
        self.data = []
        self.errors = []
        self.fields = []
        self.setup()                     # Load DB structure and connection

    def get_by_dossier(self, dossier_id):
        self.cur.execute("SELECT * FROM evaluations WHERE dossier_id = %s", (dossier_id,))
        self.data = [row for row in self.cur]