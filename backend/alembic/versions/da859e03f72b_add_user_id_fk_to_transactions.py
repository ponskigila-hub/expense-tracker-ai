"""add user_id fk to transactions

Revision ID: da859e03f72b
Revises: 77e170508412
Create Date: 2026-07-31 10:55:16.957436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da859e03f72b'
down_revision: Union[str, Sequence[str], None] = '77e170508412'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Adds transactions.user_id as a FK to users.id.

    SQLite can't ALTER TABLE ADD a NOT NULL column without a default
    when the table already has rows, and it can't add a foreign key
    constraint in place — so this uses Alembic's batch mode, which
    rebuilds the table under the hood.

    Any pre-existing transactions (created before auth existed) are
    orphaned with respect to ownership. They're backfilled onto the
    first registered user so the column can be made NOT NULL. In a
    real production migration you'd coordinate this with stakeholders
    instead of silently reassigning ownership.
    """

    bind = op.get_bind()

    # 1. Add the column as nullable first, so existing rows don't
    #    break the migration.
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))

    # 2. Backfill existing rows onto the first user in the system,
    #    if there is one and there are orphaned transactions.
    first_user_id = bind.execute(
        sa.text("SELECT id FROM users ORDER BY id LIMIT 1")
    ).scalar()

    if first_user_id is not None:
        bind.execute(
            sa.text(
                "UPDATE transactions SET user_id = :uid WHERE user_id IS NULL"
            ),
            {"uid": first_user_id}
        )

    # 3. Now that every row has a user_id, enforce NOT NULL and add
    #    the index + foreign key constraint.
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.Integer(),
            nullable=False
        )
        batch_op.create_index(
            op.f('ix_transactions_user_id'),
            ['user_id'],
            unique=False
        )
        batch_op.create_foreign_key(
            'fk_transactions_user_id_users',
            'users',
            ['user_id'],
            ['id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.drop_constraint(
            'fk_transactions_user_id_users',
            type_='foreignkey'
        )
        batch_op.drop_index(op.f('ix_transactions_user_id'))
        batch_op.drop_column('user_id')
