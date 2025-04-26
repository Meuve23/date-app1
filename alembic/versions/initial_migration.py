"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('gender', sa.String(), nullable=False),
        sa.Column('looking_for', sa.String(), nullable=False),
        sa.Column('bio', sa.String(), nullable=True),
        sa.Column('interests', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('personality_traits', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('profile_picture', sa.String(), nullable=True),
        sa.Column('min_age_preference', sa.Integer(), nullable=True),
        sa.Column('max_age_preference', sa.Integer(), nullable=True),
        sa.Column('max_distance', sa.Integer(), nullable=True),
        sa.Column('relationship_goals', sa.String(), nullable=True),
        sa.Column('languages', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('zodiac_sign', sa.String(), nullable=True),
        sa.Column('education', sa.String(), nullable=True),
        sa.Column('occupation', sa.String(), nullable=True),
        sa.Column('smoking', sa.String(), nullable=True),
        sa.Column('drinking', sa.String(), nullable=True),
        sa.Column('has_children', sa.Boolean(), nullable=True),
        sa.Column('wants_children', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_active', sa.Date(), nullable=True),
        sa.Column('compatibility_score', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('receiver_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.Date(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create likes table
    op.create_table(
        'likes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('liker_id', sa.Integer(), nullable=False),
        sa.Column('liked_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['liked_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['liker_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create compatibility_reports table
    op.create_table(
        'compatibility_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('compatibility_score', sa.Float(), nullable=False),
        sa.Column('common_interests', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('personality_match', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('potential_issues', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['target_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('compatibility_reports')
    op.drop_table('likes')
    op.drop_table('messages')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users') 