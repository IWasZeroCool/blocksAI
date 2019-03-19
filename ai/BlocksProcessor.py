import math

from rl.core import Processor
import numpy as np
import Piece
import Board


class BlocksProcessor(Processor):

    board = None
    piece1 = None
    piece2 = None
    piece3 = None

    def process_step(self, observation, reward, done, info):
        """Processes an entire step by applying the processor to the observation, reward, and info arguments.
        # Arguments
            observation (object): An observation as obtained by the environment.
            reward (float): A reward as obtained by the environment.
            done (boolean): `True` if the environment is in a terminal state, `False` otherwise.
            info (dict): The debug info dictionary as obtained by the environment.
        # Returns
            The tupel (observation, reward, done, reward) with with all elements after being processed.
        """
        observation = self.process_observation(observation)
        reward = self.process_reward(reward)
        info = self.process_info(info)
        return observation, reward, done, info

    def process_observation(self, observation):
        """Processes the observation as obtained from the environment for use in an agent and
        returns it.
        # Arguments
            observation (object): An observation as obtained by the environment
        # Returns
            Observation obtained by the environment processed

        Test Observation:
        a = ['b0:0', 'b0:1', 'b0:2', 'b0:3', 'b0:4', 'b0:5', 'b0:6', 'b0:7',
        'b1:0', 'b1:1', 'b1:2', 'b1:3', 'b1:4', 'b1:5', 'b1:6', 'b1:7',
        'b2:0', 'b2:1', 'b2:2', 'b2:3', 'b2:4', 'b2:5', 'b2:6', 'b2:7',
        'b3:0', 'b3:1', 'b3:2', 'b3:3', 'b3:4', 'b3:5', 'b3:6', 'b3:7',
        'b4:0', 'b4:1', 'b4:2', 'b4:3', 'b4:4', 'b4:5', 'b4:6', 'b4:7',
        'b5:0', 'b5:1', 'b5:2', 'b5:3', 'b5:4', 'b5:5', 'b5:6', 'b5:7',
        'b6:0', 'b6:1', 'b6:2', 'b6:3', 'b6:4', 'b6:5', 'b6:6', 'b6:7',
        'b7:0', 'b7:1', 'b7:2', 'b7:3', 'b7:4', 'b7:5', 'b7:6', 'b7:7',
        'p1:0', 'p1:1', 'p1:2', 'p1:3', 'p1:4', 'p1:5', 'p1:6', 'p1:7', 
        'p1:8', 'p1:9', 'p1:10', 'p1:11', 'p1:12', 'p1:13', 'p1:14', 'p1:15', 
        'p1:16', 'p1:17', 'p1:18', 
        'p2:0', 'p2:1', 'p2:2', 'p2:3', 'p2:4', 'p2:5', 'p2:6', 'p2:7', 
        'p2:8', 'p2:9', 'p2:10', 'p2:11', 'p2:12', 'p2:13', 'p2:14', 'p2:15', 
        'p2:16', 'p2:17', 'p2:18', 
        'p3:0', 'p3:1', 'p3:2', 'p3:3', 'p3:4', 'p3:5', 'p3:6', 'p3:7', 
        'p3:8', 'p3:9', 'p3:10', 'p3:11', 'p3:12', 'p3:13', 'p3:14', 'p3:15', 
        'p3:16', 'p3:17', 'p3:18'
        ]
        """
        # print("--- PROCESS OBSERVATION")
        board1d = np.array(observation[0:64])
        piece11d = observation[64:83]
        piece21d = observation[83:102]
        piece31d = observation[102:]
        self.board = board1d.reshape((8, 8))
        self.piece1 = Piece.one_hot_to_piece_id(piece11d)
        self.piece2 = Piece.one_hot_to_piece_id(piece21d)
        self.piece3 = Piece.one_hot_to_piece_id(piece31d)
        # print("Board {} Piece1 {} Piece2 {} Piece3 {}".format(board1d, piece11d, piece21d, piece31d))
        # print("Processed Board {} Piece1 {} Piece2 {} Piece3 {}".format(self.board, self.piece1, self.piece2, self.piece3))
        return observation

    def process_reward(self, reward):
        """Processes the reward as obtained from the environment for use in an agent and
        returns it.
        # Arguments
            reward (float): A reward as obtained by the environment
        # Returns
            Reward obtained by the environment processed
        """
        return reward

    def process_info(self, info):
        """Processes the info as obtained from the environment for use in an agent and
        returns it.
        # Arguments
            info (dict): An info as obtained by the environment
        # Returns
            Info obtained by the environment processed
        """
        return info

    def process_action(self, action):
        """Processes an action predicted by an agent but before execution in an environment.
        # Arguments
            action (int): Action given to the environment
        # Returns
            Processed action given to the environment
        """
        """
        Alright. It looks like we're given an int here.
        This would translate to 1-64, piece 1, 65-128 piece 2, 129-192 piece 3
        where action % 64 == the position in a 1d plane
        """
        # pieceIdx = math.floor(action / 64)
        # position1d = action % 64
        # posy = math.floor(position1d / 8)
        # posx = position1d % 8
        # pid = -1
        # if pieceIdx == 0:
        #     pid = self.piece1
        # elif pieceIdx == 1:
        #     pid = self.piece2
        # else:
        #     pid = self.piece3
        # piece = Piece.piece_from_id(pid)
        # # print("Applying piece {} with pos {} {} to board {}".format(piece, posx, posy, self.board))
        # new_board = Board.apply_piece_only(np.zeros((8, 8), dtype=np.uint8), piece, posx, posy)
        # print("PROCESS ACTION {} , pieceIdx {} position {} posy {} posx {}".format(action, pieceIdx, position1d, posy, posx))
        # print("Piece is ", piece)
        # if new_board is None:
        #     new_board = np.zeros((8, 8), dtype=np.uint8)
        # # print("Applied Board ", new_board)
        # return new_board
        return action

    def process_state_batch(self, batch):
        """Processes an entire batch of states and returns it.
        # Arguments
            batch (list): List of states
        # Returns
            Processed list of states
        """
        return batch

    @property
    def metrics(self):
        """The metrics of the processor, which will be reported during training.
        # Returns
            List of `lambda y_true, y_pred: metric` functions.
        """
        return []

    @property
    def metrics_names(self):
        """The human-readable names of the agent's metrics. Must return as many names as there
        are metrics (see also `compile`).
        """
        return []
