import os.path
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QTextBrowser, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt


class RecipeDetail(QWidget):
    """
    Class that controls the Recipe Detail GUI for each recipe.
    """

    def __init__(self, title, ingredient, instruction, image):
        """
        Initializes the class given a title, ingredient, instruction and image of a recipe.
        :param title: the name of a recipe
        :param ingredient: all the ingredients of a recipe as a string
        :param instruction: all the instructions of a recipe as a string
        :param image: the image file name of a recipe
        :return None
        """

        super().__init__()
        self.title = title
        self.ingredients = ingredient
        self.instructions = instruction
        self.image = image

        # initiate a main widget
        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(0, 0, 1000, 700)
        self.mainWidget.setStyleSheet("background-color: rgb(248, 248, 248);")

        self.showDetail()

    def showDetail(self):
        """
        Shows GUI of the Recipe Detail page for each recipe.
        :return: None
        """

        # set a background image and recipe title
        if self.image:
            self.setBackgroundImage(self.image)
            self.setRecipeTitle(self.title)

        # show all ingredients (handling delay)
        if self.ingredients:
            # create ingredients group box and set the title
            ingredientsGroupBox = self.getIngredientsGroupBox()
            self.setIngredientsTitle()

            # handle the format of given ingredients
            ingredients = self.handleIngredients(self.ingredients)

            # create ingredients text browser in the ingredients group box and add ingredients
            ingredientsTextBrowser = self.getIngredientsTextBrowser(ingredientsGroupBox)
            ingredientsTextBrowser.append(ingredients)

        # show all instructions (handling delay)
        if self.instructions:
            # create instruction group box and set the title
            instructionsGroupBox = self.getInstructionsGroupBox()
            self.setInstructionsTitle()

            # handle the format of given instructions
            instructions = self.handleInstructions(self.instructions)

            # create instructions text browser in the instructions group box and add instructions
            instructionsTextBrowser = self.getInstructionsTextBrowser(instructionsGroupBox)
            instructionsTextBrowser.append(instructions)

    def setRecipeTitle(self, title: str):
        """
        Sets a recipeTitle label with the given title string and handles its style.
        :param title: recipe title
        :return: None
        """
        # create a label with given title
        recipeTitle = QLabel(title, self.mainWidget)

        # set the style of the label
        recipeTitle.setGeometry(0, 130, 1000, 41)
        recipeTitle.setAlignment(Qt.AlignCenter)
        recipeTitle.setFont(QFont("Arial", 30, QFont.Bold))
        recipeTitle.setStyleSheet("background-color: None;"
                                  "color: white;")

        # set a drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 1)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("black"))
        recipeTitle.setGraphicsEffect(shadow)

    def setBackgroundImage(self, image: str):
        """
        Finds a proper image with the given image name and sets it as a background.
        If the given image name doesn't match with any file in the root folder,
        sets the background as a default image.
        :param image: a file name of the target image
        :return: None
        """
        # create a label for a background image
        backgroundLabel = QLabel(self.mainWidget)
        backgroundLabel.setGeometry(0, 0, 1000, 180)
        backgroundLabel.setStyleSheet("background-color: #cccccc;")

        # add image to the label
        image_path = self.getImagePath(image)
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(backgroundLabel.width(), backgroundLabel.height(), Qt.KeepAspectRatioByExpanding)
        backgroundLabel.setPixmap(scaled_pixmap)

    def setIngredientsTitle(self):
        """
        Sets a ingredientsTitle label and handles its style.
        :return: None
        """
        # create a label for ingredients title
        ingredientsTitle = QLabel("Ingredients", self.mainWidget)

        # set the style of the label
        ingredientsTitle.setGeometry(40, 200, 251, 31)
        self.handleSubtitleStyle(ingredientsTitle)

    def getIngredientsGroupBox(self) -> object:
        """
        Creates a group box to wrap all ingredients and handles its style.
        :return: a group box to wrap ingredients
        """
        # create a group box to wrap all ingredients
        ingredientsGroupBox = QGroupBox(self.mainWidget)

        # set the style of the group box
        ingredientsGroupBox.setGeometry(40, 240, 251, 411)
        self.handleGroupBoxStyle(ingredientsGroupBox)

        return ingredientsGroupBox

    def setInstructionsTitle(self):
        """
        Sets a instructionsTitle label and handles its style.
        :return: None
        """
        # create a label for instructions title
        instructionsTitle = QLabel("Instructions", self.mainWidget)

        # set the style of the label
        instructionsTitle.setGeometry(310, 200, 641, 31)
        self.handleSubtitleStyle(instructionsTitle)

    def getInstructionsGroupBox(self) -> object:
        """
        Creates a group box to wrap all instructions and handles its style.
        :return: a group box to wrap ingredients
        """
        # create a group box to wrap all instructions
        instructionsGroupBox = QGroupBox(self.mainWidget)

        # set the style of the group box
        instructionsGroupBox.setGeometry(310, 240, 641, 411)
        self.handleGroupBoxStyle(instructionsGroupBox)

        return instructionsGroupBox

    @staticmethod
    def getImagePath(image_path: str) -> str:
        """
        Returns the path to the image if it exits, otherwise the path to a default image.
        :param image_path: path to the desired image
        :return: path to either the desired image or the default image
        """
        rout = "statics/images/"
        name = image_path if os.path.exists(rout + image_path + ".jpg") else "default"
        return rout + name + ".jpg"

    @staticmethod
    def getIngredientsTextBrowser(ingredients_group_box: object) -> object:
        """
        Creates ingredientsBrowser to put the ingredients text and sets its location.
        :param ingredients_group_box: QGroupBox object to wrap all ingredients
        :return: QTextBrowser added to the given group box
        """
        # create a text browser with given ingredients group box
        ingredientsTextBrowser = QTextBrowser(ingredients_group_box)
        ingredientsTextBrowser.setGeometry(0, 0, 251, 411)
        ingredientsTextBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        return ingredientsTextBrowser

    @staticmethod
    def getInstructionsTextBrowser(instructions_group_box: object) -> object:
        """
        Creates instructionsBrowser to put the ingredients text and sets its location.
        :param instructions_group_box: QGroupBox object to wrap all instructions
        :return: QTextBrowser added to the given group box
        """
        # create a text browser with given instructions group box
        instructionsTextBrowser = QTextBrowser(instructions_group_box)
        instructionsTextBrowser.setGeometry(0, 0, 641, 411)
        instructionsTextBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        return instructionsTextBrowser

    @staticmethod
    def handleIngredients(ingredients: str) -> str:
        """
        Modifies the given ingredients text style to show it appropriately on the screen.
        :param ingredients: ingredients text with a list format
        :return: modified ingredients text
        """
        # remove '[' and ']' signs at the beginning and end and split it
        split_list = ingredients[1:-1].split("', '")

        # to handle ' sign at the beginning of the first element and at the end of the last element
        first = split_list.pop(0)
        last = split_list.pop()

        # add emoji at the beginning of each element and add the first and last element
        res_list = ["✔️ " + s for s in split_list]
        res_list.insert(0, "✔️ " + first[1:])
        res_list.append("✔️ " + last[:-1])

        return "\n\n".join(res_list)

    @staticmethod
    def handleInstructions(instructions: str) -> str:
        """
        Modifies the given instructions text style to show it appropriately on the screen.
        :param instructions: instructions text with a list format
        :return: modified instructions text
        """
        # split given instructions and add the number at the beginning of each element
        split_list = instructions.split("\n")
        res_list = [f"{idx + 1}.  {s}" for idx, s in enumerate(split_list)]

        return "\n\n".join(res_list)

    @staticmethod
    def handleSubtitleStyle(label: object):
        """
        Modifies the style of the given QLabel object.
        :param label: QLabel object which is either ingredientsTitle or instructionsTitle
        :return: None
        """
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 20, QFont.Bold))
        label.setStyleSheet("color: #B22222;"
                            "padding: 0; margin: 0;")

    @staticmethod
    def handleGroupBoxStyle(group_box: object):
        """
        Modifies the style of the given QGroupBox object.
        :param group_box: QGroupBox object which is either ingredientsGroupBox or instructionsGroupBox
        :return: None
        """
        # set a drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 5)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor("#dddddd"))
        group_box.setGraphicsEffect(shadow)

        group_box.setStyleSheet("border-radius: 15px;"
                                "padding: 20px;"
                                "background-color: white;")
