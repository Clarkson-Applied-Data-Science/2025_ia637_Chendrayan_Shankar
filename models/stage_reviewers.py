from baseObject import baseObject

class stage_reviewers(baseObject):
    def __init__(self):
        self.tn = "stage_reviewers"
        self.pk = "id"
        self.data = []
        self.errors = []
        self.fields = []
        self.setup()

    def get_by_stage(self, stage_id):
        self.cur.execute("SELECT * FROM stage_reviewers WHERE stage_id = %s", (stage_id,))
        self.data = self.cur.fetchall()

    def get_pending_by_reviewer(self, reviewer_id):
        self.cur.execute("SELECT * FROM stage_reviewers WHERE reviewer_id = %s AND status = 'Pending'", (reviewer_id,))
        self.data = self.cur.fetchall()
