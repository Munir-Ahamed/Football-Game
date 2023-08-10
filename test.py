from ursina import *

app = Ursina()

burst_entity = Entity(model='sphere', color=color.red, scale=0.01)

def burst_animation():
    global burst_entity
    burst_sequence = Sequence(
        ScaleTo(burst_entity, 1.0, duration=0.1),
        Func(burst_entity.disable),
    )
    burst_sequence.start()
    burst_entity = Entity(model='sphere', color=color.red, scale=0.01)

def input(key):
    if key == 'space':
        burst_animation()

app.run()
