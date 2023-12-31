"""models

Revision ID: e041be5a996d
Revises: 
Create Date: 2023-10-14 18:34:35.665439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e041be5a996d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('telegram_id', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('customer', 'courier', 'barmaid', 'admin', name='role'), nullable=True),
    sa.Column('joined', sa.DateTime(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.Column('code', sa.String(length=5), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('barmaid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_online', sa.Boolean(), nullable=True),
    sa.Column('raiting', sa.Float(), nullable=True),
    sa.Column('is_delivering', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('prepare', 'ready', 'wait', 'waitcourier', 'delivery', 'arrived', 'finished', name='orderstatus'), nullable=True),
    sa.Column('delivery_address', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('delivery_start_date', sa.DateTime(), nullable=True),
    sa.Column('courier_id', sa.Integer(), nullable=True),
    sa.Column('finish_date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['courier.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('delivery_queue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('queue', sa.String(), nullable=True),
    sa.Column('pointer', sa.Integer(), nullable=True),
    sa.Column('last_offer_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    op.create_table('product_to_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_to_order')
    op.drop_table('delivery_queue')
    op.drop_table('order')
    op.drop_table('customer')
    op.drop_table('courier')
    op.drop_table('barmaid')
    op.drop_table('admin')
    op.drop_table('user')
    op.drop_table('product')
    # ### end Alembic commands ###
