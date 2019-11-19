from . import prepare, state_machine
from .states.game import Game


def main():
    run_it = state_machine.StateMachine(prepare.ORIGINAL_CAPTION)
    state_dict = {
        'GAME': Game(),
    }
    run_it.setup_states(state_dict, 'GAME')
    run_it.main()
