import enum



class OrderStatus(enum.Enum):
    prepare = 'prepare'
    ready = 'ready'
    delivery = 'delivery'
    arrived = 'arrived'
    finished = 'finished'
