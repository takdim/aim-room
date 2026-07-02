from app.extensions import db


class PaktaTemplate(db.Model):
    """Stores the latest pakta integritas template file path for download."""

    __tablename__ = "pakta_templates"

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"))
