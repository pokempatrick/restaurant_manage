from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from budgets.models import Budgets, DishBudgets, ItemIngredientRoots, ItemIngredients


class ItemIngredientsSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemIngredients
        fields = '__all__'


class ItemIngredientRootsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemIngredientRoots
        fields = ('ingredient_name', 'quantity')


class BudgetsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Budgets
        fields = ('id', 'statut', 'total_price',
                  'start_date', 'end_date', 'added_by', 'created_at', 'description')


class DishBudgetsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = DishBudgets
        fields = ('id', 'dish_name', 'dish_quantity',
                  'total_price', 'created_at', 'added_by')


class BudgetsDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    dishbudgets_set = DishBudgetsSerializer(
        read_only=True, default=None, many=True)

    class Meta:
        model = Budgets
        fields = '__all__'


class DishBudgetsDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    budget = BudgetsSerializer(
        read_only=True, default=None)

    itemingredients_set = ItemIngredientsSerializer(many=True)

    class Meta:
        model = DishBudgets
        fields = '__all__'


class DishBudgetsPostSerializer(serializers.ModelSerializer):

    itemingredients_set = ItemIngredientsSerializer(many=True)

    class Meta:
        model = DishBudgets
        fields = '__all__'

    def create(self, validated_data):
        item_ingredient_list = validated_data.pop("itemingredients_set")
        dish_budget = DishBudgets.objects.create(**validated_data)
        for item_ingredient in item_ingredient_list:
            dish_budget.itemingredients_set.create(**item_ingredient)
        return dish_budget

    def update(self, instance, validated_data):

        item_ingredients_list = validated_data.pop("itemingredients_set")
        super().update(instance, validated_data)

        """getting list of item_ingredient id with same dish_budget instance"""
        item_ingredients_with_same_dish_budget_instance = ItemIngredients.objects.filter(
            dish_budget=instance.id).values_list('id', flat=True)

        item_ingredients_id_pool = []

        for item_ingredient in item_ingredients_list:
            if "id" in item_ingredient.keys():
                if ItemIngredients.objects.filter(id=item_ingredient['id']).exists():
                    item_ingredient_instance = ItemIngredients.objects.get(
                        id=item_ingredient['id'])
                    super().update(item_ingredient_instance, dict(item_ingredient))
                    item_ingredients_id_pool.append(
                        item_ingredient_instance.id)
                else:
                    continue
            else:
                item_ingredient_instance = instance.itemingredients_set.create(
                    **item_ingredient)
                item_ingredients_id_pool.append(item_ingredient_instance.id)

            for item_ingredient_id in item_ingredients_with_same_dish_budget_instance:
                if item_ingredient_id not in item_ingredients_id_pool:
                    ItemIngredients.objects.filter(
                        pk=item_ingredient_id).delete()
        return instance


class DishBudgetsOtherSerializer(serializers.ModelSerializer):

    itemingredients_set = ItemIngredientsSerializer(many=True)

    class Meta:
        model = DishBudgets
        exclude = ['budget']
