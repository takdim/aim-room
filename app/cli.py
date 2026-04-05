import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models.user import User


@click.command("create-admin")
@click.option("--name", prompt="Full name", help="Nama lengkap admin.")
@click.option("--email", prompt="Email", help="Email admin.")
@click.password_option(
    confirmation_prompt=True,
    help="Password admin (akan disimpan sebagai hash).",
)
@with_appcontext
def create_admin_command(name: str, email: str, password: str) -> None:
    normalized_email = email.strip().lower()
    existing_user = User.query.filter_by(email=normalized_email).first()
    if existing_user:
        raise click.ClickException("Email sudah terdaftar.")

    user = User(full_name=name.strip(), email=normalized_email, role="admin")
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    click.echo(f"Admin berhasil dibuat: {normalized_email}")


def register_commands(app) -> None:
    app.cli.add_command(create_admin_command)
