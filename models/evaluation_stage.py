from baseObject import baseObject

class evaluation_stage(baseObject):
    def __init__(self):
        self.tn = "evaluation_stages"    # Table name
        self.pk = "stage_id"             # Primary key
        self.data = []
        self.errors = []
        self.fields = []
        self.setup()                     # Load DB structure and connection
    
    def get_by_evaluation(self, evaluation_id):
        self.cur.execute("SELECT * FROM evaluation_stages WHERE evaluation_id = %s ORDER BY stage_order", (evaluation_id,))
        self.data = [row for row in self.cur]

    def get_current_stage(self, evaluation_id):
        self.cur.execute("""
            SELECT * FROM evaluation_stages
            WHERE evaluation_id = %s AND status = 'Pending'
            ORDER BY stage_order ASC LIMIT 1
        """, (evaluation_id,))
        self.data = [row for row in self.cur]