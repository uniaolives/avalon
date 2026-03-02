# arkhe/tests/test_arkhenet.py
import pytest
from arkhenet.core.world import World
from arkhenet.core.automaton import Automaton
from arkhenet import config

def test_arkhenet_basic_flow():
    # Setup world
    world = World(config)

    # Create automaton
    adam = Automaton(
        name="AdamTest",
        wallet=100.0,
        cpu_cost=0.1,
        inference_cost=0.05,
        world=world
    )
    world.add_automaton(adam)

    assert len(world.automatons) == 1
    assert adam.wallet == 100.0

    # Heartbeat
    adam.heartbeat()
    assert adam.wallet == pytest.approx(99.9)
    assert adam.uptime == 1

    # Earning and Spending
    adam.earn(10.0)
    assert adam.wallet == pytest.approx(109.9)

    success = adam.spend(50.0)
    assert success is True
    assert adam.wallet == pytest.approx(59.9)

    fail = adam.spend(100.0)
    assert fail is False
    assert adam.wallet == pytest.approx(59.9)

def test_arkhenet_world_step():
    config.SIM_TIME = 10
    world = World(config)
    adam = Automaton("Adam", 100.0, 0.1, 0.05, world)
    world.add_automaton(adam)

    # Em um passo, o autômato pensa e pode ganhar dinheiro.
    # Vamos apenas verificar se o tempo passa e se ele permanece vivo.
    stat = world.step()
    assert stat['time'] == 1
    assert stat['alive'] >= 1
    # total_wallet pode variar, então não testamos limite fixo aqui se houver ganhos
