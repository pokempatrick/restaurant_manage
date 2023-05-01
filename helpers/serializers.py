from rest_framework import serializers


class TrackingSerializer(serializers.ModelSerializer):

    RootObject = None

    NestedObject = None

    nested_attribut = None

    def create(self, validated_data):
        nested_object_list = validated_data.pop(self.nested_attribut)
        root_object = self.RootObject.objects.create(**validated_data)
        for nested_object in nested_object_list:
            getattr(root_object, self.nested_attribut).create(**nested_object)

        return root_object

    def update(self, instance, validated_data):

        nested_objects_list = validated_data.pop(self.nested_attribut)
        super().update(instance, validated_data)

        """getting list of nested_object id with same root_object instance"""
        nested_objects_with_same_root_object_instance = self.NestedObject.objects.filter(
            root_object=instance.id).values_list('id', flat=True)

        nested_objects_id_pool = []

        for nested_object in nested_objects_list:
            if "id" in nested_object.keys():
                if self.NestedObject.objects.filter(id=nested_object['id']).exists():
                    nested_object_instance = self.NestedObject.objects.get(
                        id=nested_object['id'])
                    super().update(nested_object_instance, dict(nested_object))
                    nested_objects_id_pool.append(
                        nested_object_instance.id)
                else:
                    continue
            else:
                # nested_object_instance = instance.itemingredients_set.create(
                #     **nested_object)
                nested_object_instance = getattr(
                    instance, self.nested_attribut).create(**nested_object)
                nested_objects_id_pool.append(nested_object_instance.id)

            for nested_object_id in nested_objects_with_same_root_object_instance:
                if nested_object_id not in nested_objects_id_pool:
                    self.NestedObject.objects.filter(
                        pk=nested_object_id).delete()
        return instance
