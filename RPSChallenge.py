import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLabel, QMessageBox, QInputDialog, QProgressBar, QFrame, QSizePolicy,
)
from PyQt5.QtCore import QTimer, Qt, QCoreApplication


ascii_art = {
    "rock": "✊",
    "paper": "✋",
    "scissors": "✌️"
}


class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.initVariables()
        self.initUI()


    def initVariables(self):
        self.user_score = 0
        self.computer_score = 0
        self.game_time_left = 0
        self.rounds_left = 0
        self.total_rounds = 0
        self.game_mode = ""
        self.timer_running = False
        self.total_time = 0


    def initUI(self):
        self.setWindowTitle("Rock, Paper, Scissors Game")
        self.setFixedSize(600, 700)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        self.createResultDisplay()
        self.createScoreDisplay()
        self.createAsciiDisplays()
        self.createGameButtons()
        self.createModeSelection()
        self.createTimerDisplay()
        self.createControlButtons()

        self.showInitialState()


    def createResultDisplay(self):
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(
            """
            QLabel {
                font: bold 16px;
                color: #2c3e50;
                padding: 10px;
            }
        """
        )
        self.main_layout.addWidget(self.result_label)


    def createScoreDisplay(self):
        self.score_label = QLabel("Score - You: 0 | Computer: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet(
            """
            QLabel {
                font: bold 14px;
                color: #34495e;
                background: #ecf0f1;
                border-radius: 5px;
                padding: 8px;
            }
        """
        )
        self.main_layout.addWidget(self.score_label)


    def createAsciiDisplays(self):
        ascii_style = """
            QTextEdit {
                background: #f8f9fa;
                border: 5px solid #bdc3c7;
                border-radius: 10px;
                font-family: 'Courier New';
                font-size: 40px;
                padding: 10px;
                text-align: center;
            }
        """

        ascii_layout = QHBoxLayout()
        ascii_layout.setSpacing(15)

        self.user_choice_display = QTextEdit()
        self.user_choice_display.setReadOnly(True)
        self.user_choice_display.setStyleSheet(ascii_style)
        self.user_choice_display.setAlignment(Qt.AlignCenter)
        self.user_choice_display.setMinimumSize(200, 200)
        self.user_choice_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.vs_label = QLabel("VS")
        self.vs_label.setAlignment(Qt.AlignCenter)
        self.vs_label.setStyleSheet("font: bold 70px; color: #e74c3c;")

        self.computer_choice_display = QTextEdit()
        self.computer_choice_display.setReadOnly(True)
        self.computer_choice_display.setStyleSheet(ascii_style)
        self.computer_choice_display.setAlignment(Qt.AlignCenter)
        self.computer_choice_display.setMinimumSize(200, 200)
        self.computer_choice_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        ascii_layout.addWidget(self.user_choice_display)
        ascii_layout.addWidget(self.vs_label)
        ascii_layout.addWidget(self.computer_choice_display)

        self.main_layout.addLayout(ascii_layout)


    def createGameButtons(self):
        self.game_buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(self.game_buttons_frame)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(15)

        self.rock_btn = self.createGameButton(f"{ascii_art['rock']}", "rock")
        self.paper_btn = self.createGameButton(f"{ascii_art['paper']}", "paper")
        self.scissors_btn = self.createGameButton(f"{ascii_art['scissors']}", "scissors")

        buttons_layout.addWidget(self.rock_btn)
        buttons_layout.addWidget(self.paper_btn)
        buttons_layout.addWidget(self.scissors_btn)

        self.main_layout.addWidget(self.game_buttons_frame)


    def createGameButton(self, text, choice):
        btn = QPushButton(text)
        btn.setProperty("choice", choice)
        btn.setStyleSheet(
            """
            QPushButton {
                background: #3498db;
                color: white;
                font: bold 50px;
                padding: 15px;
                border: none;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
            QPushButton:disabled {
                background: #bdc3c7;
            }
        """
        )
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.clicked.connect(lambda: self.playGame(choice))
        return btn


    def createModeSelection(self):
        self.mode_frame = QFrame()
        mode_layout = QVBoxLayout(self.mode_frame)
        mode_layout.setContentsMargins(50, 50, 50, 50)
        mode_layout.setSpacing(30)

        mode_layout.addStretch(1)

        self.time_mode_btn = self.createModeButton("Time Mode", "time")
        self.rounds_mode_btn = self.createModeButton("Rounds Mode", "rounds")

        mode_layout.addWidget(self.time_mode_btn)
        mode_layout.addWidget(self.rounds_mode_btn)
        
        mode_layout.addStretch(1)

        self.main_layout.addWidget(self.mode_frame, stretch=1)  # Added stretch

    def createModeButton(self, text, mode):
        btn = QPushButton(text)
        btn.setProperty("mode", mode)
        btn.setStyleSheet(
            """
            QPushButton {
                background: #2ecc71;
                color: white;
                font: bold 24px;  /* Increased font size */
                padding: 30px;   /* Increased padding */
                border: none;
                border-radius: 15px;
                min-height: 100px;  /* Minimum height */
            }
            QPushButton:hover {
                background: #27ae60;
            }
        """
        )
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.clicked.connect(lambda: self.startGame(mode))
        return btn
    

    def createTimerDisplay(self):
        self.timer_label = QLabel("Time left: 0m 0s")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font: bold 14px; color: #2c3e50;")

        self.rounds_label = QLabel("Rounds left: 0")
        self.rounds_label.setAlignment(Qt.AlignCenter)
        self.rounds_label.setStyleSheet("font: bold 14px; color: #2c3e50;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                height: 20px;
            }
            QProgressBar::chunk {
                background: #3498db;
                width: 10px;
            }
        """
        )

        self.main_layout.addWidget(self.timer_label)
        self.main_layout.addWidget(self.rounds_label)
        self.main_layout.addWidget(self.progress_bar)


    def createControlButtons(self):
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(15)

        self.pause_btn = QPushButton("Pause")
        self.reset_btn = QPushButton("Reset")
        self.quit_btn = QPushButton("Quit")

        buttons = [
            (self.pause_btn, "#f1c40f", self.pauseGame),
            (self.reset_btn, "#e67e22", self.resetGame),
            (self.quit_btn, "#e74c3c", self.quitGame),
        ]

        for btn, color, handler in buttons:
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: {color};
                    color: white;
                    font: bold 14px;
                    padding: 12px;
                    border: none;
                    border-radius: 5px;
                    min-width: 100px;
                }}
                QPushButton:hover {{
                    background: {color.replace('f', 'e')};
                }}
            """
            )
            btn.clicked.connect(handler)
            control_layout.addWidget(btn)

        self.main_layout.addWidget(control_frame)


    def showInitialState(self):
        self.user_choice_display.hide()
        self.computer_choice_display.hide()
        self.vs_label.hide()
        self.score_label.hide()
        self.timer_label.hide()
        self.rounds_label.hide()
        self.progress_bar.hide()
        self.game_buttons_frame.hide()
        self.pause_btn.hide()
        self.reset_btn.hide()


    def playGame(self, user_choice):
        if not self.timer_running and self.game_mode == "time":
            return

        computer_choice = random.choice(["rock", "paper", "scissors"])
        self.determineWinner(user_choice, computer_choice)
        self.updateAsciiArt(user_choice, computer_choice)
        self.updateGameState()
        self.updateScoreDisplay()

        if self.shouldEndGame():
            self.endGame()


    def determineWinner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return
        win_conditions = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper",
        }
        if win_conditions[user_choice] == computer_choice:
            self.user_score += 1
        else:
            self.computer_score += 1


    def updateAsciiArt(self, user_choice, computer_choice):
        self.user_choice_display.setHtml(f'<p style="font-size: 100px; text-align: center;">{ascii_art.get(user_choice, "")}</p>')
        self.computer_choice_display.setHtml(f'<p style="font-size: 100px; text-align: center;">{ascii_art.get(computer_choice, "")}</p>')


    def updateGameState(self):
        if self.game_mode == "rounds":
            self.rounds_left -= 1
            self.rounds_label.setText(f"Rounds left: {self.rounds_left}")
            self.updateProgressBar(self.rounds_left, self.total_rounds)


    def updateScoreDisplay(self):
        self.score_label.setText(
            f"Score - You: {self.user_score} | Computer: {self.computer_score}"
        )


    def shouldEndGame(self):
        if self.game_mode == "rounds" and self.rounds_left <= 0:
            return True
        if self.game_mode == "time" and self.game_time_left <= 0:
            return True
        return False


    def startGame(self, mode):
        self.game_mode = mode
        self.resetScores()

        start_success = False
        
        if mode == "time":
            start_success = self.startTimeMode()
        elif mode == "rounds":
            start_success = self.startRoundsMode()

        if start_success:
            self.showGameInProgressState()
        else:
            self.game_mode = ""
            self.mode_frame.show()
            self.showInitialState()


    def startTimeMode(self):
        minutes, ok = QInputDialog.getInt(
            self, "Game Duration", "Enter game duration (minutes):", 
            min=1, max=60, value=3
        )
        
        if not ok:
            return False
            
        self.game_time_left = minutes * 60
        self.total_time = self.game_time_left
        self.timer_label.setText(f"Time left: {minutes}m 00s")
        self.startTimer()
        return True


    def startRoundsMode(self):
        rounds, ok = QInputDialog.getInt(
            self, "Number of Rounds", "Enter number of rounds:", 
            min=1, max=50, value=5
        )
        
        if not ok:
            return False
            
        self.rounds_left = rounds
        self.total_rounds = rounds
        self.rounds_label.setText(f"Rounds left: {rounds}")
        self.updateProgressBar(rounds, rounds)
        return True


    def resetScores(self):
        self.user_score = 0
        self.computer_score = 0
        self.updateScoreDisplay()


    def showGameInProgressState(self):
        self.user_choice_display.show()
        self.computer_choice_display.show()
        self.vs_label.show()
        self.score_label.show()
        self.mode_frame.hide()
        self.game_buttons_frame.show()
        self.timer_label.setVisible(self.game_mode == "time")
        self.rounds_label.setVisible(self.game_mode == "rounds")
        self.progress_bar.show()
        self.pause_btn.setVisible(self.game_mode == "time")
        self.reset_btn.show()
        self.enableGameButtons(True)
        self.timer_running = True


    def startTimer(self):
        if not self.timer.isActive():
            self.timer.start(1000)


    def updateTimer(self):
        if self.game_time_left > 0:
            self.game_time_left -= 1
            mins, secs = divmod(self.game_time_left, 60)
            self.timer_label.setText(f"Time left: {mins}m {secs:02d}s")
            self.updateProgressBar(self.game_time_left, self.total_time)
        else:
            self.endGame()


    def updateProgressBar(self, current, total):
        if total > 0:
            progress = ((total - current) / total) * 100
            self.progress_bar.setValue(int(progress))
        else:
            self.progress_bar.setValue(0)


    def pauseGame(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.pause_btn.setText("Resume")
            self.enableGameButtons(False)
        else:
            if self.game_mode == "time":
                self.timer.start()
            self.timer_running = True
            self.pause_btn.setText("Pause")
            self.enableGameButtons(True)


    def enableGameButtons(self, enable):
        for btn in [self.rock_btn, self.paper_btn, self.scissors_btn]:
            btn.setEnabled(enable)


    def endGame(self):
        self.timer.stop()
        self.timer_running = False
        self.enableGameButtons(False)
        self.showFinalResults()


    def showFinalResults(self):
        if self.user_score == 0 and self.computer_score == 0:
            result_text = "Game Over!\nNo scores recorded."
        else:
            winner = "You" if self.user_score > self.computer_score else "Computer"
            result_text = f"""
                Game Over!
                Final Score:
                You: {self.user_score}
                Computer: {self.computer_score}
                Winner: {winner}!
            """
        self.result_label.setText(result_text)
        QMessageBox.information(self, "Game Over", result_text.strip())
        self.resetUI()
        self.mode_frame.show()
        self.showInitialState()


    def resetGame(self):
        if (
            QMessageBox.Yes
            == QMessageBox.question(
                self,
                "Reset Game",
                "Are you sure you want to reset?",
                QMessageBox.Yes | QMessageBox.No,
            )
        ):
            self.timer.stop()
            self.resetUI()
            self.showInitialState()
            self.mode_frame.show()


    def resetUI(self):
        self.initVariables()
        self.user_choice_display.clear()
        self.computer_choice_display.clear()
        self.user_choice_display.hide()
        self.computer_choice_display.hide()
        self.vs_label.hide()
        self.score_label.hide()
        self.result_label.clear()
        self.progress_bar.setValue(0)
        self.timer_label.hide()
        self.rounds_label.hide()
        self.score_label.setText("Score - You: 0 | Computer: 0")


    def quitGame(self):
        if (
            QMessageBox.Yes
            == QMessageBox.question(
                self, "Quit Game", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No
            )
        ):
            QCoreApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec_())

