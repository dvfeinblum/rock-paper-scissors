from random import randint

import click

import logging

LOGGER = logging.getLogger(__file__)


class RockPaperScissors:
    def __init__(
        self,
        autoplay: bool,
        game_count: int = 1,
    ) -> None:
        self.game_count = game_count
        self.autoplay = autoplay
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.move_map = {1: "Rock", 2: "Paper", 3: "Scissors"}

    def user_won(self, user_choice: int, bot_choice: int) -> bool:
        """Given the user's selection and the bot's selection, calculate if the user won."""
        result_dict = {1: 3, 2: 1, 3: 2}
        return result_dict[user_choice] == bot_choice

    def get_users_move(self):
        raw_choice = input(
            "Choose your move (enter the number)!\n1. Rock\n2. Paper\n3. Scissors\n"
        )
        try:
            user_choice = int(raw_choice)
            if not 0 < user_choice < 4:
                raise ValueError
        except ValueError:
            LOGGER.warning(
                f"Your selection ({raw_choice}) was invalid. Please enter an integer (1, 2, or 3)."
            )
            user_choice = self.get_users_move()

        return user_choice

    def simulate_game(self):
        """Runs a round of rock paper scissors"""
        if self.autoplay:
            user_choice = randint(1, 3)
            LOGGER.debug(f"Automated user selected {self.move_map[user_choice]}")
        else:
            user_choice = self.get_users_move()

        bot_choice = randint(1, 3)
        LOGGER.debug(f"The bot has selected {self.move_map[bot_choice]}")

        if bot_choice == user_choice:
            LOGGER.debug("Both users selected the same move. It's a draw!\n")
            self.draws += 1
        elif self.user_won(user_choice, bot_choice):
            LOGGER.debug("You win!\n")
            self.wins += 1
        else:
            LOGGER.debug("You lose.\n")
            self.losses += 1

    def simulate_games(self):
        for _ in range(self.game_count):
            self.simulate_game()


@click.command()
@click.option("--count", default=1, help="Number of games to simulate.")
@click.option("--autoplay", is_flag=True, help="Allows user to simulate without input")
@click.option(
    "--verbose",
    is_flag=True,
    help="Print out more info about each game as they are simulated",
)
def main(count: int, autoplay: bool, verbose: bool):
    """Entrypoint for rock paper scissor simulator"""
    if verbose:
        logging.basicConfig(format="%(message)s", level=logging.DEBUG)
        LOGGER.debug("Using verbose logging.\n")
    else:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    rps = RockPaperScissors(autoplay, game_count=count)
    rps.simulate_games()

    LOGGER.info(
        f"Results\n\nGames Played: {rps.game_count}\nWins: {rps.wins}"
        f"\nLosses: {rps.losses}\nWin Percentage {rps.wins/count:.2%}"
    )


if __name__ == "__main__":
    main()
