import sys
from PyQt5.QtWidgets import QApplication, QWidget
from RecipeList import RecipeList
from WelcomeWindow import WelcomeWindow


class Recipe(QWidget):
    """
    The main class which contains the window with the implemented GUI
    """

    def __init__(self):
        """
        Initialize the program by calling the constructor from the super class to use variables from PyQt5
        Contains a width and height for the window
        Initializes and calls the RecipeList and WelcomeWindow classes
        """
        super().__init__()
        self.width, self.height = 1000, 700

        self.listWidget = RecipeList(self.width, self.height)
        self.welcomeWindow = WelcomeWindow()

        self.show_list_widget()
        self.show_welcome_window()

    def show_list_widget(self):
        """
        Displays the widgets properly in order
        Includes window title and window dimensions
        """
        self.listWidget.setWindowTitle("Find a Recipe")
        self.listWidget.resize(self.width, self.height)
        self.listWidget.show()

    def show_welcome_window(self):
        """
        Displays pop-up welcome message to the user by calling the
        :return:
        """
        self.welcomeWindow.setWindowTitle("Find a Recipe")
        self.welcomeWindow.resize(500, 340)
        self.welcomeWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Recipe()
    sys.exit(app.exec_())
