from enum import Enum

from algorithms.moves.Move import Move
from algorithms.moves.SwapTwoPoints import SwapTwoPoints
from algorithms.moves.TwoOpt import TwoOpt


class AvailableMoves(str, Enum):
    SWAP_TWO_POINTS = "SwapTwoPoints"  # SwapTwoPoints.__name__
    TWO_OPT = "TwoOpt"  # TwoOpt.__name__

    @classmethod
    def get_move(cls, move: "AvailableMoves") -> Move:
        match move:
            case AvailableMoves.SWAP_TWO_POINTS:
                return SwapTwoPoints
            case AvailableMoves.TWO_OPT:
                return TwoOpt
            case _:
                raise ValueError(f"Unknown move method: {move}")
