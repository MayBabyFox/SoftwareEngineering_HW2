from Ingredient import Ingredient


class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient: Ingredient):
        for component in self.ingredients:
            if component == ingredient:
                component.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if ratio > 0:
            return True
        return False

    def scale(self, ratio: float):
        new_ingredients = []
        for component in self.ingredients:
            new_component = (Ingredient(component.name, component.quantity * ratio, component.unit))
            new_ingredients.append(new_component)
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        unique_components = []
        for component in self.ingredients:
            if (component.name, component.unit) not in unique_components:
                unique_components.append((component.name, component.unit))
        return len(unique_components)

    def __str__(self):
        ingredients_reader = []
        for component in self.ingredients:
            ingredients_reader.append(f"{component.name}: {component.quantity} {component.unit}")
        return f"Блюдо: {self.title}\nИнгредиенты:\n" + "\n".join(ingredients_reader)