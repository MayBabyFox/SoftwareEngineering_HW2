from Recipe import Recipe


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self._diet_type = diet_type

    def scale(self, ratio: float):
        new_ingredients = super().scale(ratio).ingredients
        return DietaryRecipe(self.title, self._diet_type, new_ingredients)

    def __str__(self):
        return f"[{self._diet_type}] {super().__str__()} "