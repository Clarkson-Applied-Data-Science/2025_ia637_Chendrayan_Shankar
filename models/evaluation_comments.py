from baseObject import baseObject

class evaluation_comments(baseObject):
    def __init__(self):
        self.tn = "evaluation_comments"      # table name
        self.pk = "comment_id"               # primary key
        self.data = []
        self.errors = []
        self.fields = []
        self.setup()

    def get_by_stage(self, stage_id):
        self.cur.execute(
            "SELECT * FROM evaluation_comments WHERE stage_id = %s ORDER BY created_at",
            (stage_id,)
        )
        self.data = [row for row in self.cur]

    def get_by_evaluation(self, evaluation_id):
        from models.evaluation_stage import evaluation_stage

        # Fetch all stage IDs for the evaluation
        stages = evaluation_stage()
        stages.get_by_evaluation(evaluation_id)
        stage_ids = [s['stage_id'] for s in stages.data]

        if not stage_ids:
            self.data = []
            return

        # Fetch comments across all those stages
        format_strings = ','.join(['%s'] * len(stage_ids))
        self.cur.execute(
            f"SELECT * FROM evaluation_comments WHERE stage_id IN ({format_strings}) ORDER BY created_at",
            tuple(stage_ids)
        )
        self.data = self.cur.fetchall()

