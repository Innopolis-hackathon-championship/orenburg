import enum



class OrderStatus(enum.Enum):
    prepare = 'prepare'
    ready = 'ready'
    wait = "wait"
    waitcourier = "waitcourier"
    delivery = 'delivery'
    arrived = 'arrived'
    finished = 'finished'
