from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class WelcomeWindow(QWidget):
    """
    Class that shows a welcome message and instructions of the Program to users.
    """

    def __init__(self):
        """
        Initializes the class and makes mainWidget.
        """
        super().__init__()
        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(0, 0, 500, 340)
        self.mainWidget.setStyleSheet("background-color: rgb(248, 248, 248);")

        self.set_ui()

    def set_ui(self):
        """
        Shows GUI of the Welcome Window before the Recipe List.
        :return: None
        """

        # initializes a title widget
        title = QLabel("Welcome to Find a Recipe!", self.mainWidget)

        # handles the style of the title widget
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("border-bottom: 1px solid #dddddd;")
        title.setAlignment(Qt.AlignCenter)
        title.setGeometry(0, 0, 500, 50)

        # initializes a message widget to show instructions for the program
        message = QLabel("Please input a single-word ingredient into the text bar at the top of the main page to add an"
                         " ingredient. Once you have added all of your desired ingredients, press the submit button and"
                         " wait for the page to load (this may take some time). Find a Recipe will provide you with a"
                         " list of recipes that contain your ingredients. \n\nHope you are ready to cook!",
                         self.mainWidget)
        message.setWordWrap(True)

        # handles the style of the message widget
        message.setFont(QFont("Arial", 15))
        message.setGeometry(20, 70, 460, 210)
        message.setStyleSheet("padding: 20px;"
                              "background-color: white;"
                              "border-radius: 10px;")

        # adds a shadow to the message widget
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 5)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor("#dddddd"))
        message.setGraphicsEffect(shadow)

        # create a authors widget
        authors = QLabel("Love, Soo & Jess 🫶", self.mainWidget)
        authors.setStyleSheet("background: None;")
        authors.setFont(QFont("Arial", 15, QFont.Bold))
        authors.setAlignment(Qt.AlignCenter)
        authors.setGeometry(20, 285, 460, 50)
