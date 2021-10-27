from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    COLUMNS = ["title", "description"]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, values):
        columns = set(cls.COLUMNS)
        filtered = {k:v for k, v in values.items() if k in columns}
        return cls(**filtered)

    def update_from_dict(self, values):
        for column in self.COLUMNS:
            if column in values:
                setattr(self, column, values[column])


    def replace_with_dict(self, values):
        for column in self.COLUMNS:
            if column in values:
                setattr(self, column, values[column])
            else:
                raise ValueError(f"required column {column} missing")