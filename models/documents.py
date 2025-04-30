from baseObject import baseObject

class documents(baseObject):
    def __init__(self):
        self.tn = "documents"
        self.pk = "document_id"
        self.data = []
        self.errors = []
        self.fields = []
        self.setup()

    def get_by_evaluation(self, evaluation_id):
        from models.evaluation_stage import evaluation_stage

        # Fetch all stage IDs for the evaluation
        stages = evaluation_stage()
        stages.get_by_evaluation(evaluation_id)
        stage_ids = [s['stage_id'] for s in stages.data]

        if not stage_ids:
            self.data = []
            return

        # Fetch documents across all those stages
        format_strings = ','.join(['%s'] * len(stage_ids))
        self.cur.execute(
            f"SELECT * FROM documents WHERE stage_id IN ({format_strings})",
            tuple(stage_ids)
        )
        self.data = self.cur.fetchall()

