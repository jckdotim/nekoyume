import sys
import random

from nekoyume.battle.simul import DummyBattle


def main():
    seed = 1
    if len(sys.argv) >= 2:
        seed = int(sys.argv[1])
    simulator = DummyBattle(random.Random(seed))
    simulator.simulate()


if __name__ == '__main__':
    main()
