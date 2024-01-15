import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect,
                             QHBoxLayout, QLineEdit, QListWidget, QScrollArea)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt
import pandas as pd
from RecipeDetail import RecipeDetail
from functools import partial


class RecipeList(QWidget):
    """
    Class that controls the main GUI and manages layout, taking user input, filtering the data, and updating the UI
    """

    def __init__(self, width, height):
        """
        Initializes the class given a width and height
        Contains variables involving widget layouts, display, and list contents
        :param width of window
        :param height of window
        """
        super().__init__()
        self.width, self.height = width, height  # sets the width and height of the window
        self.user_ingredients = []  # an empty list to hold the user-input ingredients

        # main widget layout and properties
        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(0, 0, 1000, 700)  # sets the area for widgets (within the area of the window)
        self.mainWidget.setStyleSheet("background-color: rgb(248, 248, 248);")  # sets the background color

        # initializing background image
        self.backgroundLabel = QLabel(self.mainWidget)

        # initializing the input line and buttons
        self.inputLine = QLineEdit(self.mainWidget)
        self.addButton = QPushButton('Add', self.mainWidget)
        self.submitButton = QPushButton('Submit', self.mainWidget)
        self.clearButton = QPushButton('Clear All', self.mainWidget)

        # initializing the list of ingredients
        self.ingredientList = QListWidget(self.mainWidget)

        # initializing the recipe details by calling the class RecipeDetail
        self.detailWidget = RecipeDetail(None, None, None, None)

        # initializing the scrolling area that contains the list of ingredients
        self.scrollArea = QScrollArea(self.mainWidget)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # initializing a layout to organize content within the scrolling area
        self.recipeLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        # allows for setting up the layout with the setup_ui function
        self.setup_ui()

        # displays the main page
        self.show_recipe_list()

    def setup_ui(self):
        """
        Organizes the main layout of the page
        :return:
        """
        # background image: default image behind user input line
        # setting the dimensions and color
        self.backgroundLabel.setGeometry(0, 0, 1000, 121)
        self.backgroundLabel.setStyleSheet("background-color: #cccccc;")
        # uses pixmap to map the image from the statics folder
        pixmap = QPixmap("statics/images/default.jpg")
        # scales the image to match the defined area
        scaled_pixmap = pixmap.scaled(self.backgroundLabel.width(), self.backgroundLabel.height(),
                                      Qt.KeepAspectRatioByExpanding)
        self.backgroundLabel.setPixmap(scaled_pixmap)

        # input line: box where the user inputs ingredients
        self.inputLine.setPlaceholderText("Enter your ingredient here")  # text that goes away once user types
        # styling the input line
        self.inputLine.setGeometry(40, 40, 811, 41)
        self.inputLine.setStyleSheet("border: None;"
                                     "padding: 10px;"
                                     "background-color: white;")
        # adds drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 1)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("black"))
        self.inputLine.setGraphicsEffect(shadow)
        # allow user to press "return" in order to call the handle_input function
        self.inputLine.returnPressed.connect(self.handle_input)

        # add button: button clicked to add that ingredient to the user list
        self.addButton.clicked.connect(self.handle_input)  # clicking the add button calls the handle_input function
        # styling the button
        self.addButton.setGeometry(870, 40, 91, 41)
        self.addButton.setStyleSheet("background-color: #333333;"  # gives it dark gray color
                                     "color: white;"  # white font color
                                     "border: None;"
                                     "border-radius: 7px;")  # curved edges
        self.addButton.setFont(QFont("Arial", 16, QFont.Bold))
        # change cursor style on button
        self.addButton.setCursor(Qt.PointingHandCursor)
        # adds drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 1)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor("black"))
        self.addButton.setGraphicsEffect(shadow)

        # ingredients list: the compiled list of ingredients input by the user
        # styling the list and container
        self.ingredientList.setGeometry(40, 140, 811, 91)
        self.ingredientList.setStyleSheet("border: None;"
                                          "border-radius: 10px;"
                                          "background-color: #eeeeee;"
                                          "padding: 15px;")
        self.ingredientList.setFont(QFont("Arial", 14))
        # styling the scroll bar to be hidden
        self.ingredientList.verticalScrollBar().setStyleSheet("""
                            QScrollBar:vertical {
                                background: None;
                                width:10px; 
                                margin: 0px 0px 0px 0px;
                            }""")

        # clear button: button clicked when the user wants to remove all ingredient inputs from the list
        self.clearButton.clicked.connect(self.clear_ing_list)  # calls the clear_ing_list function when clicked
        # styling the button
        self.clearButton.setGeometry(870, 140, 91, 41)
        self.clearButton.setStyleSheet("color: #B22222;"  # makes the font maroon
                                       "border: 1px solid #B22222;"  # makes the border maroon
                                       "border-radius: 7px;")
        self.clearButton.setFont(QFont("Arial", 16, QFont.Bold))
        # change cursor style on button
        self.clearButton.setCursor(Qt.PointingHandCursor)

        # submit button: button clicked when the user is ready to filter the recipe list with their ingredients
        self.submitButton.clicked.connect(self.submit_ing_list)  # calls the submit_ing_list function when clicked
        # styling the button
        self.submitButton.setGeometry(870, 190, 91, 41)
        self.submitButton.setStyleSheet("background-color: #B22222;"  # makes the button maroon
                                        "color: white;"
                                        "border: None;"
                                        "border-radius: 7px;")
        self.submitButton.setFont(QFont("Arial", 16, QFont.Bold))
        # changes cursor style on button
        self.submitButton.setCursor(Qt.PointingHandCursor)

        # scroll area: a scrollable area containing widgets including the list of original recipes (before filter)
        # styling the area
        self.scrollArea.setGeometry(40, 250, 921, 401)
        # styling the scroll bar
        self.scrollArea.verticalScrollBar().setStyleSheet("""
                    QScrollBar:vertical {
                        background: None;
                        width:10px; 
                        margin: 0px 0px 0px 0px;
                    }""")
        self.scrollAreaWidgetContents.setGeometry(0, 0, 919, 399)

    def show_recipe_list(self):
        """
        Displays the original list of recipes in default order prior to the user inputting ingredients
        """
        # loading the data
        data = self.load_data()
        # calling a function to break up the data columns
        titles, images, ingredients, instructions = self.convert_df(data)

        # iterate through each row of the recipe data
        for idx in range(50):  # shows 50 recipes by default for application efficiency
            # gets the item at each index in each feature
            title, ingredient, instruction, image = titles[idx], ingredients[idx], instructions[idx], images[idx]

            # create button with the title of recipe and connect it with a details page
            btn = QPushButton(str(title))
            btn.clicked.connect(
                # opens the corresponding information for the recipe
                lambda _, t=title, ing=ingredient, ins=instruction, img=image: self.open_detail_page(t, ing, ins, img)
            )
            # set button style and dimensions
            btn.setFixedSize(871, 40)
            self.set_button_style(btn)  # calls set_button_style function

            # adds the button to the recipe layout (vertical layout box inside the scrollable area)
            self.recipeLayout.addWidget(btn)
            self.recipeLayout.update()  # updates the layout for clarity

    def handle_input(self):
        """
        Retrieves the text input by the user
        :return: None
        """
        ing = self.inputLine.text()  # gets the text from the input line (from the user)
        # if it exists, add the ingredient to the ingredient list which will be displayed and stored
        if ing:
            self.ingredientList.addItem(ing)
            self.inputLine.clear()  # clear the input line for new ingredient

    def submit_ing_list(self):
        """
        Function for the submit ingredient button
        Iterates through the list of user ingredients
        Calls a function to filter the data
        Calls a function to update the list of recipes in the UI
        :return: None
        """
        # creates a python and pandas interpretable list
        self.user_ingredients = [self.ingredientList.item(i).text() for i in range(self.ingredientList.count())]
        # calls filter function on the user ingredients
        filtered_df = self.filter_data(self.user_ingredients)
        # calls the updateList function on the filtered dataset of recipes
        self.update_list(filtered_df)

    def filter_data(self, user_ingredients):
        """
        Filters the data set so only recipes with the user ingredients appears
        Sort the list of recipes from most user ingredients to least
        :param user_ingredients:
        :return: the filtered dataset
        """
        # loads the dataset
        data = self.load_data()
        # gets each word from the ingredients column of the dataset to compare with the user list
        data['Cleaned_Ingredients'] = data['Cleaned_Ingredients'].apply(lambda x: x.split(' '))

        # create a column to list out the ingredients that overlap
        data['Target_Ingredients'] = data['Cleaned_Ingredients'].apply(
            lambda x: list(set([item for item in x if item in user_ingredients])))
        # create a score column to keep track of the amount of ingredients that overlap
        data['score'] = data['Target_Ingredients'].apply(lambda x: len(list(x)))

        # sort by score in descending order
        df_sorted = data.sort_values('score', ascending=False)

        # remove rows that do not contain any matching ingredients
        df_filtered = df_sorted[df_sorted['score'] > 0].copy()
        # make list of ingredients in the dataset a list again for proper handling
        df_filtered['Cleaned_Ingredients'] = df_filtered['Cleaned_Ingredients'].apply(lambda x: ' '.join(x))

        # return the new filtered dataset
        return df_filtered

    def update_list(self, filtered_df):
        """
        Takes the filtered dataset to update the UI to display the new correct list of recipes that contain their
        ingredients
        :param filtered_df:
        :return: None
        """
        # clears the existing layout
        self.clear_layout()

        # obtains the last column of target ingredients to display to the user
        target_ings = filtered_df['Target_Ingredients'].reset_index(drop=True)
        # abstracts the other columns from the dataframe via the convert_df function
        titles, images, ingredients, instructions = self.convert_df(filtered_df)

        # creating headers for the layout
        # makes a horizontal box layout to put the recipes on the left and the user ingredients on the right
        labelTitles = QHBoxLayout()
        # header for recipe column
        recipeLabel = QLabel("Recipes:", self.scrollAreaWidgetContents)
        # sets style for the header
        recipeLabel.setFixedSize(700, 40)
        recipeLabel.setStyleSheet("border: None;"
                                  "color: #333333;")
        recipeLabel.setFont(QFont("Arial", 16, QFont.Bold))
        # header for the ingredients column
        ingTitle = QLabel("Ingredients:", self.scrollAreaWidgetContents)
        # sets style for the header
        ingTitle.setFixedSize(187, 40)
        ingTitle.setStyleSheet("border: None;"
                               "color: #333333;")
        ingTitle.setFont(QFont("Arial", 16, QFont.Bold))

        # adds each label header to the horizontal box layout
        labelTitles.addWidget(recipeLabel)
        labelTitles.addWidget(ingTitle)

        # adds the box layout to the top of the scrollable area
        self.recipeLayout.addLayout(labelTitles)

        # iterates through each row of the filtered data frame by column
        for idx in range(len(titles)):
            # gets the specifics at each index of the filtered data frame
            title, ingredient, instruction, image, target_ing = titles[idx], ingredients[idx], instructions[idx], \
                                                                images[idx], target_ings[idx]

            # creates a new horizontal layout for each recipe to also include list of user ingredients
            recipeHLayout = QHBoxLayout()

            # creates button for each recipe
            btn = QPushButton(str(title), self.scrollAreaWidgetContents)
            # opens the detail page if user presses the recipe button
            btn.clicked.connect(partial(self.open_detail_page, title, ingredient, instruction, image))
            # sets the button dimensions and style
            btn.setFixedSize(700, 40)
            self.set_button_style(btn)
            # adds the button to be the left side of the horizontal layout
            recipeHLayout.addWidget(btn)

            # adds a list of the user ingredients next to each recipe button
            # displays the list and makes it readable to user by removing [] and '
            ingredientLabel = QLabel(str(target_ing).replace("'", "").strip("[]"), self.scrollAreaWidgetContents)
            # styles the ingredients to be red
            ingredientLabel.setStyleSheet("border: None;"
                                          "color: #B22222")
            ingredientLabel.setFont(QFont("Arial", 15))
            # adds it to the horizontal layout
            recipeHLayout.addWidget(ingredientLabel)

            # adds each horizontal layout to the overall vertical layout
            self.recipeLayout.addLayout(recipeHLayout)

    def clear_layout(self):
        """
        Removes all widgets from the recipe list layout
        """
        # remove widget until all widgets are removed
        while self.recipeLayout.count():
            # get the first item from the layout
            layoutItem = self.recipeLayout.takeAt(0)
            if layoutItem.widget():
                layoutItem.widget().deleteLater()  # delete if the widget exists
            elif layoutItem.layout():
                self.clear_nested_layout(layoutItem.layout())  # call function to remove nested widget

    def clear_nested_layout(self, layout):
        """
        Removes all widgets from a nested layout (e.g. horizontal or vertical layouts)
        :param: type of layout
        :return: None
        """
        # iterate until no layouts left
        while layout.count():
            # get first layout
            item = layout.takeAt(0)
            # get the widget in the layout
            widget = item.widget()
            if widget:
                widget.deleteLater()  # delete widget if it exists
            elif item.layout():  # check for layout within layout and call function again
                self.clear_nested_layout(item.layout())

    def clear_ing_list(self):
        """
        Remove all items in the user ingredient list
        :return:
        """
        self.ingredientList.clear()

    def open_detail_page(self, title, ingredient, instruction, image):
        """
        Opens the detail page associated with the clicked on recipe
        :param title:
        :param ingredient:
        :param instruction:
        :param image:
        :return: None
        """
        # connect RecipeDetail class
        self.detailWidget = RecipeDetail(title, ingredient, instruction, image)
        # style detail background
        self.detailWidget.setStyleSheet("background-color: white;")

        # make the title of the window the recipe title
        self.detailWidget.setWindowTitle(title)
        # open window to the same size as the main page
        self.detailWidget.resize(self.width, self.height)
        # display the details
        self.detailWidget.show()

    @staticmethod
    def load_data():
        """
        Loads data from statics folder
        :return: the dataset as a pandas dataframe
        """
        # load data from statics folder
        data = pd.read_csv("statics/data/Food Ingredients and Recipe Dataset with Image Name Mapping.csv")
        return data

    @staticmethod
    def convert_df(data):
        """
        Extracts the columns from the data for easier code manipulation
        :param data:
        :return: Title, Image_Name, Cleaned_Ingredients, and Instructions columns as individual lists
        """
        titles = data["Title"].tolist()
        images = data["Image_Name"].tolist()
        ingredients = data["Cleaned_Ingredients"].tolist()
        instructions = data["Instructions"].tolist()

        return titles, images, ingredients, instructions

    @staticmethod
    def set_button_style(btn):
        """
        Sets the style of the recipe button
        :param btn:
        :return: None
        """
        # calls setStyleSheet to set the color of the button
        btn.setStyleSheet("border: None;"
                          "border-radius: 10px;"
                          "color: #333333;"
                          "background-color: white;")
        # sets button font
        btn.setFont(QFont("Arial", 15, QFont.Bold))

        # changes cursor style when on button
        btn.setCursor(Qt.PointingHandCursor)

        # adds drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 1)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#dddddd"))
        btn.setGraphicsEffect(shadow)
