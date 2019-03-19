from rl.callbacks import Callback
import Piece


class StatsCallback(Callback):

    # episode = 0
    #
    # def on_episode_begin(self, episode, logs={}):
    #     self.episode = episode
    #
    # def on_action_end(self, action, logs={}):
    #     fmt = "Episode {:6}, Action {:4}, Lines Cleared {:4}, Current Score {:4}, High Score {:4}\n"\
    #           "Piece 1\n{}\nPiece 2\n{}\nPiece 3\n{}\nBoard\n{}"
    #     p1 = Piece.piece_from_id(self.env.piece1)
    #     p2 = Piece.piece_from_id(self.env.piece2)
    #     p3 = Piece.piece_from_id(self.env.piece3)
    #     print(fmt.format(self.episode, action, self.env.lines_cleared, self.env.current_score,
    #                      self.env.high_score, p1, p2, p3, self.env.board))
    #
    # def on_episode_end(self, episode, logs={}):
    #     fmt = "Episode {:4}, Lines Cleared {:4}, Current Score {:4}, High Score {:4}"
    #     print(fmt.format(episode, self.env.lines_cleared, self.env.current_score, self.env.high_score))

    interval_lines_cleared = 0
    interval_high_score = 0
    line_clears_1 = 0
    line_clears_2 = 0
    line_clears_3 = 0
    interval_bad_piece_played = 0
    interval_piece_played_off_board = 0

    def __init__(self, interval=10000):
        super().__init__()
        self.interval = interval
        self.step = 0
        self.reset()

    def reset(self):
        self.interval_bad_piece_played = 0
        self.interval_bad_piece_played = 0
        self.interval_lines_cleared = 0
        self.interval_high_score = 0
        self.line_clears_1 = 0
        self.line_clears_2 = 0
        self.line_clears_3 = 0

    def on_step_begin(self, step, logs):
        """ Print metrics if interval is over """
        if self.step % self.interval == 0:
            fmt = "Total High Score: {:5}\nInterval High Score: {:5}\nLines Cleared: {:5}\n"\
                  "1-Liners: {:4}\n2-Liners: {:4}\n3-Liners: {:4}\nBad Piece Played: {:5}\n"\
                  "Piece Played Off Board: {:5}"
            print(fmt.format(self.env.high_score, self.interval_high_score, self.interval_lines_cleared,
                             self.line_clears_1, self.line_clears_2, self.line_clears_3,
                             self.interval_bad_piece_played, self.interval_piece_played_off_board))
            self.reset()

    def on_step_end(self, step, logs):
        self.step += 1
        self.interval_lines_cleared += self.env.last_lines_cleared
        if self.env.current_score > self.interval_high_score:
            self.interval_high_score = self.env.current_score
        if self.env.last_lines_cleared == 1:
            self.line_clears_1 += 1
        elif self.env.last_lines_cleared == 2:
            self.line_clears_2 += 1
        elif self.env.last_lines_cleared == 3:
            self.line_clears_3 += 1

    def on_episode_end(self, episode, logs={}):
        self.interval_bad_piece_played = self.env.bad_piece_played
        self.interval_piece_played_off_board = self.env.piece_played_off_board
