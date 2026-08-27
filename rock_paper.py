import os
import sys
import time
import random
import json
from collections import defaultdict

if sys.platform.startswith('win'):
    os.system('color')

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
   
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"

ASCII_ART = {
    "rock": [
        "    _______      ",
        "---'   ____)     ",
        "      (_____)    ",
        "      (_____)    ",
        "      (____)     ",
        "---.__(___)      "
    ],
    "paper": [
        "    _______      ",
        "---'   ____)____ ",
        "          ______)",
        "          _______)",
        "         _______)",
        "---.__________)  "
    ],
    "scissors": [
        "    _______      ",
        "---'   ____)____ ",
        "          ______)",
        "       __________)",
        "      (____)     ",
        "---.__(___)      "
    ],
    "lizard": [
        "    _______      ",
        "---'   ____)____ ",
        "          ______)",
        "       (________)",
        "      (_____)    ",
        "---.__(___)      "
    ],
    "spock": [
        "    _______      ",
        "---'   ____)____ ",
        "          ______)",
        "       __________)",
        "      (________) ",
        "---.__(________) "
    ]
}

RULES = {
    "rock": {
        "beats": ["scissors", "lizard"],
        "verbs": {"scissors": "crushes", "lizard": "crushes"}
    },
    "paper": {
        "beats": ["rock", "spock"],
        "verbs": {"rock": "covers", "spock": "disproves"}
    },
    "scissors": {
        "beats": ["paper", "lizard"],
        "verbs": {"paper": "cuts", "lizard": "decapitates"}
    },
    "lizard": {
        "beats": ["spock", "paper"],
        "verbs": {"spock": "poisons", "paper": "eats"}
    },
    "spock": {
        "beats": ["scissors", "rock"],
        "verbs": {"scissors": "smashes", "rock": "vaporizes"}
    }
}

MOVE_EMOJIS = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️",
    "lizard": "🦎",
    "spock": "🖖"
}

def clear_screen():
    """Clears the console screen across OS platforms."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.02, end="\n"):
    """Prints text with a typewriter effect for dramatic impact."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def draw_header(title):
    """Draws a stylized header banner."""
    width = 60
    print(f"{Colors.CYAN}═" * width + f"{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{title.center(width)}{Colors.RESET}")
    print(f"{Colors.CYAN}═" * width + f"{Colors.RESET}")

def play_sound_beep():
    """Triggers terminal bell audio feedback."""
    sys.stdout.write('\a')
    sys.stdout.flush()

class PlayerProfile:
    """Manages player statistics, win streaks, XP level, and achievements."""
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.current_streak = 0
        self.best_streak = 0
        self.xp = 0
        self.level = 1
        self.history = []
        self.achievements = {
            "First Victory": False,
            "On Fire (3 Win Streak)": False,
            "Unstoppable (5 Win Streak)": False,
            "Spock Enthusiast (5 Spock plays)": False,
            "Mind Reader (Beat Hard AI 3 times)": False
        }
        self.spock_count = 0
        self.hard_ai_wins = 0

    def add_result(self, result, player_move, ai_difficulty):
        """Updates stats based on round outcome."""
        self.history.append(player_move)
        if player_move == "spock":
            self.spock_count += 1

        if result == "win":
            self.wins += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            
            xp_gained = 50 + (self.current_streak * 10)
            self.xp += xp_gained
            
            if ai_difficulty == "Hard":
                self.hard_ai_wins += 1

        elif result == "loss":
            self.losses += 1
            self.current_streak = 0
            self.xp += 10
        else: # Tie
            self.ties += 1
            self.xp += 20

        level_threshold = self.level * 100
        if self.xp >= level_threshold:
            self.level += 1
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 LEVEL UP! You reached Level {self.level}! 🎉{Colors.RESET}")
            time.sleep(1)

        self.check_achievements()

    def check_achievements(self):
        """Evaluates and unlocks user achievements."""
        newly_unlocked = []
        
        if self.wins >= 1 and not self.achievements["First Victory"]:
            self.achievements["First Victory"] = True
            newly_unlocked.append("First Victory")

        if self.current_streak >= 3 and not self.achievements["On Fire (3 Win Streak)"]:
            self.achievements["On Fire (3 Win Streak)"] = True
            newly_unlocked.append("On Fire (3 Win Streak)")

        if self.current_streak >= 5 and not self.achievements["Unstoppable (5 Win Streak)"]:
            self.achievements["Unstoppable (5 Win Streak)"] = True
            newly_unlocked.append("Unstoppable (5 Win Streak)")

        if self.spock_count >= 5 and not self.achievements["Spock Enthusiast (5 Spock plays)"]:
            self.achievements["Spock Enthusiast (5 Spock plays)"] = True
            newly_unlocked.append("Spock Enthusiast (5 Spock plays)")

        if self.hard_ai_wins >= 3 and not self.achievements["Mind Reader (Beat Hard AI 3 times)"]:
            self.achievements["Mind Reader (Beat Hard AI 3 times)"] = True
            newly_unlocked.append("Mind Reader (Beat Hard AI 3 times)")

        for ach in newly_unlocked:
            print(f"\n{Colors.BG_YELLOW}{Colors.WHITE}{Colors.BOLD}🏆 ACHIEVEMENT UNLOCKED: {ach}! 🏆{Colors.RESET}")
            play_sound_beep()
            time.sleep(1.2)

class AIEngine:
    """Provides multiple difficulty levels, including Markov chain pattern prediction."""
    def __init__(self):
        # Markov Chain model for predicting player's next move based on previous move
        self.transition_matrix = defaultdict(lambda: defaultdict(int))

    def update_history(self, history):
        """Learns from player history to build prediction model."""
        if len(history) >= 2:
            prev_move = history[-2]
            curr_move = history[-1]
            self.transition_matrix[prev_move][curr_move] += 1

    def choose_move(self, available_options, difficulty, history):
        """Selects move based on difficulty mode."""
        if difficulty == "Easy" or len(history) == 0:
            return random.choice(available_options)

        if difficulty == "Medium":
            # 50% random, 50% counter player's most frequent move
            if random.random() < 0.5:
                return random.choice(available_options)
            most_common = max(set(history), key=history.count)
            return self.get_counter_move(most_common, available_options)

        if difficulty == "Hard":
            # Predictive AI using Markov Chain
            last_move = history[-1]
            predictions = self.transition_matrix[last_move]
            
            if predictions:
                predicted_next_move = max(predictions, key=predictions.get)
            else:
                predicted_next_move = random.choice(available_options)

            return self.get_counter_move(predicted_next_move, available_options)

        return random.choice(available_options)

    def get_counter_move(self, target_move, available_options):
        """Finds a move that beats target_move."""
        counters = [move for move in available_options if target_move in RULES[move]["beats"]]
        return random.choice(counters) if counters else random.choice(available_options)

def render_battle(player_move, computer_move):
    """Prints player and computer ASCII hands side-by-side."""
    p_art = ASCII_ART[player_move]
    c_art = ASCII_ART[computer_move]

    print(f"\n{Colors.CYAN}{'YOUR MOVE: ' + player_move.upper():<30} {Colors.MAGENTA}{'COMPUTER MOVE: ' + computer_move.upper():<30}{Colors.RESET}\n")

    for p_line, c_line in zip(p_art, c_art):
        # Mirror computer's hand ASCII for visual effect
        c_mirrored = c_line.replace("(", "TEMP").replace(")", "(").replace("TEMP", ")")
        c_mirrored = c_mirrored[::-1]
        print(f"{Colors.CYAN}{p_line:<32} {Colors.MAGENTA}{c_mirrored:>28}{Colors.RESET}")

def animate_countdown():
    """Displays visual countdown before move reveals."""
    print()
    words = ["🪨 ROCK", "📄 PAPER", "✂️ SCISSORS", "💥 SHOOT!"]
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN]
    
    for word, color in zip(words, colors):
        sys.stdout.write(f"\r\t\t{Colors.BOLD}{color}{word.center(30)}{Colors.RESET}")
        sys.stdout.flush()
        play_sound_beep()
        time.sleep(0.4)
    print("\n")

def display_profile(profile):
    """Prints current stats and unlocked achievements."""
    clear_screen()
    draw_header("📊 PLAYER PROFILE & STATS")
    total_games = profile.wins + profile.losses + profile.ties
    win_rate = (profile.wins / total_games * 100) if total_games > 0 else 0

    print(f"\n{Colors.BOLD}Level:{Colors.RESET} {profile.level} (XP: {profile.xp})")
    print(f"{Colors.BOLD}Total Games Played:{Colors.RESET} {total_games}")
    print(f"{Colors.GREEN}Wins:{Colors.RESET} {profile.wins}")
    print(f"{Colors.RED}Losses:{Colors.RESET} {profile.losses}")
    print(f"{Colors.YELLOW}Ties:{Colors.RESET} {profile.ties}")
    print(f"{Colors.CYAN}Win Rate:{Colors.RESET} {win_rate:.1f}%")
    print(f"{Colors.MAGENTA}Current Win Streak:{Colors.RESET} {profile.current_streak}")
    print(f"{Colors.MAGENTA}Best Win Streak:{Colors.RESET} {profile.best_streak}")

    print(f"\n{Colors.BOLD}{Colors.YELLOW}🏆 Achievements:{Colors.RESET}")
    for ach, unlocked in profile.achievements.items():
        status = f"{Colors.GREEN}✓ UNLOCKED{Colors.RESET}" if unlocked else f"{Colors.GRAY}🔒 LOCKED{Colors.RESET}"
        print(f"  • {ach:<35} [{status}]")

    input(f"\n{Colors.GRAY}Press Enter to return to main menu...{Colors.RESET}")

def display_rules():
    """Displays rules for RPS and RPSLS."""
    clear_screen()
    draw_header("📜 GAME RULES & MANUAL")
    print(f"\n{Colors.BOLD}{Colors.YELLOW}Classic Mode (RPS):{Colors.RESET}")
    print("  • Rock crushes Scissors")
    print("  • Paper covers Rock")
    print("  • Scissors cuts Paper")

    print(f"\n{Colors.BOLD}{Colors.CYAN}Extended Mode (RPSLS - Big Bang Theory Style):{Colors.RESET}")
    print("  • Rock crushes Scissors & Lizard")
    print("  • Paper covers Rock & disproves Spock")
    print("  • Scissors cuts Paper & decapitates Lizard")
    print("  • Lizard poisons Spock & eats Paper")
    print("  • Spock smashes Scissors & vaporizes Rock")

    input(f"\n{Colors.GRAY}Press Enter to return to main menu...{Colors.RESET}")

def play_round(profile, ai, game_mode, ai_difficulty):
    """Executes a single game round."""
    options = ["rock", "paper", "scissors"]
    if game_mode == "RPSLS":
        options.extend(["lizard", "spock"])

    print(f"\n{Colors.BOLD}{Colors.YELLOW}--- Choose your move ---{Colors.RESET}")
    for opt in options:
        emoji = MOVE_EMOJIS[opt]
        print(f" • [{opt[0].upper()}] {emoji} {opt.capitalize()}")

    while True:
        user_input = input(f"\n{Colors.CYAN}Enter choice ({'/'.join(options)}): {Colors.RESET}").lower().strip()
        
        # Shortcut single key matching
        matched = [opt for opt in options if opt.startswith(user_input)]
        if len(matched) == 1:
            user_choice = matched[0]
            break
        elif user_choice_exact := [opt for opt in options if opt == user_input]:
            user_choice = user_choice_exact[0]
            break
        else:
            print(f"{Colors.RED}Invalid move! Please select a valid option.{Colors.RESET}")

    computer_choice = ai.choose_move(options, ai_difficulty, profile.history)
    ai.update_history(profile.history)

    # Dramatic reveal countdown
    animate_countdown()

    # Render ASCII Visuals
    render_battle(user_choice, computer_choice)

    # Determine Winner
    if user_choice == computer_choice:
        result = "tie"
        message = f"{Colors.BOLD}{Colors.YELLOW}🤝 IT'S A TIE! Both chose {user_choice.upper()}!{Colors.RESET}"
    elif computer_choice in RULES[user_choice]["beats"]:
        result = "win"
        verb = RULES[user_choice]["verbs"][computer_choice]
        message = f"{Colors.BOLD}{Colors.GREEN}🎉 YOU WIN! Your {user_choice.upper()} {verb} Computer's {computer_choice.upper()}! 🎉{Colors.RESET}"
    else:
        result = "loss"
        verb = RULES[computer_choice]["verbs"][user_choice]
        message = f"{Colors.BOLD}{Colors.RED}😞 YOU LOSE! Computer's {computer_choice.upper()} {verb} your {user_choice.upper()}!{Colors.RESET}"

    print(f"\n{message}\n")
    profile.add_result(result, user_choice, ai_difficulty)
    return result

def play_tournament(profile, ai, game_mode, ai_difficulty, best_of=3):
    """Executes a Best-Of match series."""
    clear_screen()
    draw_header(f"🏆 TOURNAMENT: BEST OF {best_of}")
    
    player_score = 0
    computer_score = 0
    target_wins = (best_of // 2) + 1
    round_num = 1

    while player_score < target_wins and computer_score < target_wins:
        print(f"{Colors.MAGENTA}═════════ ROUND {round_num} ═════════{Colors.RESET}")
        print(f"{Colors.BOLD}Score: YOU {player_score} - {computer_score} COMPUTER (First to {target_wins}){Colors.RESET}")
        
        res = play_round(profile, ai, game_mode, ai_difficulty)
        if res == "win":
            player_score += 1
        elif res == "loss":
            computer_score += 1

        round_num += 1
        time.sleep(1.5)

    clear_screen()
    draw_header("🏁 TOURNAMENT OVER")
    if player_score > computer_score:
        print(f"\n{Colors.BOLD}{Colors.GREEN}🏆 CONGRATULATIONS! You won the Tournament ({player_score} - {computer_score})! 🏆{Colors.RESET}\n")
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}💔 GAME OVER! Computer won the Tournament ({computer_score} - {player_score})!{Colors.RESET}\n")

    input(f"{Colors.GRAY}Press Enter to return to main menu...{Colors.RESET}")

def main():
    profile = PlayerProfile()
    ai = AIEngine()

    game_mode = "Classic"      # "Classic" (RPS) or "RPSLS"
    ai_difficulty = "Medium"   # "Easy", "Medium", "Hard"

    while True:
        clear_screen()
        draw_header("🎮 ROCK PAPER SCISSORS: DELUXE EDITION")
        print(f" Current Mode: {Colors.CYAN}{game_mode}{Colors.RESET} | AI Difficulty: {Colors.MAGENTA}{ai_difficulty}{Colors.RESET}")
        print(f" Player Streak: {Colors.YELLOW}{profile.current_streak} 🔥{Colors.RESET} | Level: {Colors.GREEN}{profile.level}{Colors.RESET}\n")

        print("1. ⚡ Quick Match (Single Round)")
        print("2. 🏆 Tournament Mode (Best of 3 / 5)")
        print("3. ⚙️ Change Game Mode / AI Difficulty")
        print("4. 📊 View Stats & Achievements")
        print("5. 📜 How to Play / Rules")
        print("6. 🚪 Exit Game")

        choice = input(f"\n{Colors.CYAN}Select an option (1-6): {Colors.RESET}").strip()

        if choice == "1":
            clear_screen()
            draw_header("⚡ QUICK MATCH")
            play_round(profile, ai, game_mode, ai_difficulty)
            
            while True:
                again = input(f"{Colors.YELLOW}Play another round? (y/n): {Colors.RESET}").lower().strip()
                if again in ['y', 'yes']:
                    clear_screen()
                    draw_header("⚡ QUICK MATCH")
                    play_round(profile, ai, game_mode, ai_difficulty)
                else:
                    break

        elif choice == "2":
            clear_screen()
            draw_header("🏆 TOURNAMENT SELECT")
            print("1. Best of 3")
            print("2. Best of 5")
            sub = input(f"\n{Colors.CYAN}Choose match length (1-2): {Colors.RESET}").strip()
            length = 3 if sub != "2" else 5
            play_tournament(profile, ai, game_mode, ai_difficulty, best_of=length)

        elif choice == "3":
            clear_screen()
            draw_header("⚙️ GAME SETTINGS")
            print(f"\n{Colors.BOLD}1. Toggle Game Variant{Colors.RESET}")
            print(f"   Current: {game_mode} (Options: Classic RPS, RPSLS)")
            print(f"\n{Colors.BOLD}2. Change AI Difficulty{Colors.RESET}")
            print(f"   Current: {ai_difficulty} (Options: Easy, Medium, Hard)")

            set_choice = input(f"\n{Colors.CYAN}Select setting to change (1-2): {Colors.RESET}").strip()
            if set_choice == "1":
                game_mode = "RPSLS" if game_mode == "Classic" else "Classic"
                print(f"{Colors.GREEN}Game Mode set to {game_mode}!{Colors.RESET}")
                time.sleep(1)
            elif set_choice == "2":
                print("\nDifficulties:")
                print("1. Easy (Rookie - Random choice)")
                print("2. Medium (Tactician - Pattern recognition)")
                print("3. Hard (Psychic Master - Markov prediction)")
                diff_choice = input(f"\n{Colors.CYAN}Select AI Difficulty (1-3): {Colors.RESET}").strip()
                if diff_choice == "1":
                    ai_difficulty = "Easy"
                elif diff_choice == "3":
                    ai_difficulty = "Hard"
                else:
                    ai_difficulty = "Medium"
                print(f"{Colors.GREEN}AI Difficulty set to {ai_difficulty}!{Colors.RESET}")
                time.sleep(1)

        elif choice == "4":
            display_profile(profile)

        elif choice == "5":
            display_rules()

        elif choice == "6":
            clear_screen()
            print_slow(f"\n{Colors.CYAN}Thanks for playing Rock Paper Scissors: Deluxe Edition! Goodbye! 👋{Colors.RESET}\n", delay=0.03)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Game interrupted. Thanks for playing! 👋{Colors.RESET}")
