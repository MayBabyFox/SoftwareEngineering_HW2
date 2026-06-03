import pytest

from Ingredient import Ingredient
from Recipe import Recipe
from ShoppingList import ShoppingList


class TestIngredient():
    def test_initialization(self):
        ingredient = Ingredient("Яблоки", 600.0, "г")
        assert ingredient.name == "Яблоки"
        assert ingredient.quantity == 600.0
        assert ingredient.unit == "г"

    def test_wrong_initialization(self):
        ingredient = Ingredient("Яблоки", 600.0, "г")
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            ingredient.quantity = -600.0

    def test_str_formatting(self):
        ingredient = Ingredient("Цедра", 10.0, "г")
        assert str(ingredient) == "Цедра: 10.0 г"

    def test_equality(self):
        ingredient1 = Ingredient("Корица", 5.0, "г")
        ingredient2 = Ingredient("Корица", 10.0, "г")
        assert ingredient1 == ingredient2
        assert ingredient2 == ingredient1

    def test_dif_name(self):
        ingredient1 = Ingredient("Корица", 5.0, "г")
        ingredient2 = Ingredient("Молоко", 10.0, "г")
        assert ingredient1 != ingredient2

    def test_dif_unit(self):
        ingredient1 = Ingredient("Корица", 5.0, "г")
        ingredient2 = Ingredient("Корица", 10.0, "мг")
        assert ingredient1 != ingredient2


class TestRecipe():
    def test_initialization(self):
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        ingredient2 = Ingredient("Корица", 10.0, "г")
        recipe = Recipe("Шарлотка", [ingredient1, ingredient2])
        assert recipe.title == "Шарлотка"
        assert recipe.ingredients == [ingredient1, ingredient2]

    def test_add_ingredient(self):
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        ingredient2 = Ingredient("Корица", 10.0, "г")
        recipe = Recipe("Шарлотка", [ingredient1, ingredient2])
        ingredient3 = Ingredient("Мука", 500.0, "г")
        recipe.add_ingredient(ingredient3)
        assert recipe.ingredients == [ingredient1, ingredient2, ingredient3]

    def test_eq_add(self):
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        recipe = Recipe("Шарлотка", [ingredient1])
        ingredient2 = Ingredient("Яблоки", 2.0, "кг")
        recipe.add_ingredient(ingredient2)
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].quantity == 3.0

    def test_object_recipe(self):
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        recipe = Recipe("Шарлотка", [ingredient1])
        new = recipe.scale(2)
        assert recipe.ingredients[0].quantity == 1.0
        assert new is not recipe

    def test_scaled(self):
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        ingredient2 = Ingredient("Корица", 10.0, "г")
        recipe = Recipe("Шарлотка", [ingredient1, ingredient2])
        new = recipe.scale(2)
        assert new.ingredients[0].quantity == 2.0
        assert new.ingredients[1].quantity == 20.0
        assert recipe.ingredients[0].quantity == 1.0
        assert recipe.ingredients[1].quantity == 10.0

    def test_scale_error(self):
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        recipe = Recipe("Шарлотка", [ingredient1])
        with pytest.raises(ValueError):
            recipe.scale(0)
        with pytest.raises(ValueError):
            recipe.scale(-2)

    def test_len(self):
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        ingredient2 = Ingredient("Корица", 10.0, "г")
        ingredient3 = Ingredient("Корица", 10.0, "г")
        recipe = Recipe("Шарлотка", [ingredient1, ingredient2, ingredient3])
        assert len(recipe) == 2


class TestShoppingList:
    def test_add_recipe(self):
        shopping_list = ShoppingList()
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        recipe = Recipe("Шарлотка", [ingredient1])
        shopping_list.add_recipe(recipe, 2)
        assert len(shopping_list._items) == 1
        assert shopping_list._items[0][1] == "Шарлотка"
        assert shopping_list._items[0][0].quantity == 2.0

    def test_add_error(self):
        shopping_list = ShoppingList()
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        recipe = Recipe("Шарлотка", [ingredient1])
        with pytest.raises(ValueError):
            shopping_list.add_recipe(recipe, 0)
        with pytest.raises(ValueError):
            shopping_list.add_recipe(recipe, -5)

    def test_remove_recipe(self):
        shopping_list = ShoppingList()
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        ingredient2 = Ingredient("Мука", 500, "г")
        recipe1 = Recipe("Шарлотка", [ingredient1])
        recipe2 = Recipe("Хлеб", [ingredient2])
        shopping_list.add_recipe(recipe1, 1)
        shopping_list.add_recipe(recipe2, 1)
        assert len(shopping_list._items) == 2
        shopping_list.remove_recipe("Шарлотка")
        assert len(shopping_list._items) == 1
        assert shopping_list._items[0][1] == "Хлеб"

    def test_remove_nonexistent(self):
        shopping_list = ShoppingList()
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        recipe = Recipe("Шарлотка", [ingredient1])
        shopping_list.add_recipe(recipe, 1)
        old_length = len(shopping_list._items)
        shopping_list.remove_recipe("Наполеон")
        assert len(shopping_list._items) == old_length

    def test_get_list_sums(self):
        shopping_list = ShoppingList()
        ingredient1 = Ingredient("Мука", 300, "г")
        ingredient2 = Ingredient("Мука", 500, "г")
        recipe1 = Recipe("Пицца", [ingredient1])
        recipe2 = Recipe("Шарлотка", [ingredient2])
        shopping_list.add_recipe(recipe1, 1)
        shopping_list.add_recipe(recipe2, 1)
        result = shopping_list.get_list()
        assert len(result) == 1
        assert result[0].name == "Мука"
        assert result[0].quantity == 800.0

    def test_get_list_sorted(self):
        shopping_list = ShoppingList()
        ingredient1 = Ingredient("Яблоки", 100, "г")
        ingredient2 = Ingredient("Мука", 500, "г")
        ingredient3 = Ingredient("Корица", 3, "шт")
        recipe = Recipe("Шарлотка", [ingredient1, ingredient2, ingredient3])
        shopping_list.add_recipe(recipe, 1)
        result = shopping_list.get_list()
        names = [ing.name for ing in result]
        assert names == ["Корица", "Мука", "Яблоки"]

    def test_add_shopping_lists(self):
        shopping_list1 = ShoppingList()
        shopping_list2 = ShoppingList()
        ingredient1 = Ingredient("Яблоки", 1.0, "кг")
        ingredient2 = Ingredient("Мука", 500, "г")
        recipe1 = Recipe("Шарлотка", [ingredient1])
        recipe2 = Recipe("Хлеб", [ingredient2])
        shopping_list1.add_recipe(recipe1, 1)
        shopping_list2.add_recipe(recipe2, 1)
        combined = shopping_list1 + shopping_list2
        assert len(combined._items) == 2
        assert len(shopping_list1._items) == 1
        assert len(shopping_list2._items) == 1

