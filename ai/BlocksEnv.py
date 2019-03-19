import math

from rl.core import Env
import numpy as np
from gym.utils import seeding
import Piece
import Board


class BlocksEnv(Env):

    """The abstract environment class that is used by all agents. This class has the exact
        same API that OpenAI Gym uses so that integrating with it is trivial. In contrast to the
        OpenAI Gym implementation, this class only defines the abstract methods without any actual
        implementation.
        To implement your own environment, you need to define the following methods:
        - `step`
        - `reset`
        - `render`
        - `close`
        Refer to the [Gym documentation](https://gym.openai.com/docs/#environments).
        """

    reward_range = (-np.inf, np.inf)
    action_space = None
    observation_space = None
    board = np.zeros((8, 8), dtype=np.uint8)
    piece1 = -1
    piece2 = -1
    piece3 = -1
    np_random = None
    current_score = 0
    high_score = 0
    lines_cleared = 0
    last_lines_cleared = 0
    bad_piece_played = 0
    piece_played_off_board = 0

    def get_observation(self):
        flat_board = self.board.flatten()
        flat_board = np.append(flat_board, Piece.piece_id_to_one_hot(self.piece1))
        flat_board = np.append(flat_board, Piece.piece_id_to_one_hot(self.piece2))
        flat_board = np.append(flat_board, Piece.piece_id_to_one_hot(self.piece3))
        return flat_board

    def step(self, action):
        # print("--------- Got ACTION ", action)
        """Run one timestep of the environment's dynamics.
        Accepts an action and returns a tuple (observation, reward, done, info).
        # Arguments
            action (object): An action provided by the environment.
        # Returns
            observation (object): Agent's observation of the current environment.
            reward (float) : Amount of reward returned after previous action.
            done (boolean): Whether the episode has ended, in which case further step() calls will return undefined results.
            info (dict): Contains auxiliary diagnostic information (helpful for debugging, and sometimes learning).
        """

        self.last_lines_cleared = 0
        pieceIdx = math.floor(action / 64)
        position1d = action % 64
        posy = math.floor(position1d / 8)
        posx = position1d % 8
        pid = -1
        if pieceIdx == 0:
            pid = self.piece1
        elif pieceIdx == 1:
            pid = self.piece2
        else:
            pid = self.piece3
        # piece_id, piece_origin_x, piece_origin_y = Board.find_piece(action, [self.piece1, self.piece2, self.piece3])
        if pid == -1:
            # We played a non-existent or empty or already-played piece
            self.bad_piece_played += 1
            return self.get_observation(), 0, False, {}
        # Here we kinda need to keep track of what piece was placed where for rendering purposes
        # print("Trying to apply pieceId {} to origin {} {}".format(pid, posy, posx))
        new_board, score, lines_cleared, reward = Board.apply_piece(self.board, pid, posx, posy)
        self.board = new_board
        self.current_score += score
        self.lines_cleared += lines_cleared
        self.last_lines_cleared = lines_cleared
        if self.current_score > self.high_score:
            self.high_score = self.current_score
        if score == 0:
            self.piece_played_off_board += 1
            return self.get_observation(), 0, False, {}
        if self.piece1 == pid:
            self.piece1 = -1
        elif self.piece2 == pid:
            self.piece2 = -1
        elif self.piece3 == pid:
            self.piece3 = -1
        else:
            print("WE FOUND A PIECE BUT IT WASN'T OUR PIECE!!! ERROR")
            assert False
        done = False
        if self.piece1 == -1 and self.piece2 == -1 and self.piece3 == -1:
            self.piece1 = Piece.random_piece(self.np_random)
            self.piece2 = Piece.random_piece(self.np_random, exclude_pieces=[self.piece1])
            self.piece3 = Piece.random_piece(self.np_random, exclude_pieces=[self.piece1, self.piece2])
            # print("=====  Chose new pids 1: {} 2: {} 3: {}".format(self.piece1, self.piece2, self.piece3))
        for pid in [self.piece1, self.piece2, self.piece3]:
            if pid != -1 and not Board.piece_can_fit(self.board, pid):
                done = True
                break
        if done:
            reward += -100
        return self.get_observation(), reward, done, {}

    def reset(self):
        self.piece_played_off_board = 0
        self.bad_piece_played = 0
        self.current_score = 0
        self.lines_cleared = 0
        self.board = np.zeros((8, 8), dtype=np.uint8)
        self.piece1 = Piece.random_piece(self.np_random)
        self.piece2 = Piece.random_piece(self.np_random, exclude_pieces=[self.piece1])
        self.piece3 = Piece.random_piece(self.np_random, exclude_pieces=[self.piece1, self.piece2])
        # print("-----==== Chose pids 1: {} 2: {} 3: {}".format(self.piece1, self.piece2, self.piece3))
        return self.get_observation()

    def render(self, mode='cocoa', close=False):
        if mode == 'cocoa':
            pass
        elif mode == 'ascii':
            print(self.board)

    def close(self):
        """Override in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        pass

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def configure(self, *args, **kwargs):
        """Provides runtime configuration to the environment.
        This configuration should consist of data that tells your
        environment how to run (such as an address of a remote server,
        or path to your ImageNet data). It should not affect the
        semantics of the environment.
        """
        pass
