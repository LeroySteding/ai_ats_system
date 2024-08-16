"""Fixed Job model JSON fields

Revision ID: 6449b422ae52
Revises: 1a31ce608336
Create Date: 2024-08-16 11:59:03.505029

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6449b422ae52'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('website', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_company_name'), 'company', ['name'], unique=True)
    op.create_table('permission',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permission_name'), 'permission', ['name'], unique=True)
    op.create_table('profile',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('bio', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('skills', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('experience', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('education', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('job_preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('resume_url', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('role',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_name'), 'role', ['name'], unique=True)
    op.create_table('job',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('location', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('salary_range', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.Column('employment_type', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('requirements', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('benefits', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('company_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rolepermissionlink',
    sa.Column('role_id', sa.Uuid(), nullable=False),
    sa.Column('permission_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_table('application',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('job_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('cover_letter', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('applied_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('role_id', sa.Uuid(), nullable=True))
    op.add_column('user', sa.Column('company_id', sa.Uuid(), nullable=True))
    op.add_column('user', sa.Column('profile_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    op.create_foreign_key(None, 'user', 'profile', ['profile_id'], ['id'])
    op.create_foreign_key(None, 'user', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'profile_id')
    op.drop_column('user', 'company_id')
    op.drop_column('user', 'role_id')
    op.drop_table('application')
    op.drop_table('rolepermissionlink')
    op.drop_table('job')
    op.drop_index(op.f('ix_role_name'), table_name='role')
    op.drop_table('role')
    op.drop_table('profile')
    op.drop_index(op.f('ix_permission_name'), table_name='permission')
    op.drop_table('permission')
    op.drop_index(op.f('ix_company_name'), table_name='company')
    op.drop_table('company')
    # ### end Alembic commands ###
