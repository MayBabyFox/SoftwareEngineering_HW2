from Ingredient import Ingredient
from Recipe import Recipe


class ShoppingList:
    def __init__(self):
        self._items = []
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        new_recipe = recipe.scale(portions)
        for ingredient in new_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        new_recipe = []
        for ingredient, recipe_title in self._items:
            if recipe_title != title:
                new_recipe.append((ingredient, recipe_title))
        self._items = new_recipe

    def get_list(self):
        cookbook = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in cookbook:
                cookbook[key] += ingredient.quantity
            else:
                cookbook[key] = ingredient.quantity
        cookbook_list = []
        for (name, unit), quantity in cookbook.items():
            cookbook_list.append(Ingredient(name, quantity, unit))
        cookbook_list = sorted(cookbook_list, key=lambda x: x.name)
        return cookbook_list
    def __add__(self, other: ShoppingList):
        doubleList = ShoppingList()
        for ingredient, recipe_title in self._items:
            doubleList._items.append((ingredient, recipe_title))
        for ingredient, recipe_title in other._items:
            doubleList._items.append((ingredient, recipe_title))
        return doubleList