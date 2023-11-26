from rest_framework import serializers
from .models import Questions, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name',)
from rest_framework import serializers
from .models import Questions
class QuestionsSerializer(serializers.ModelSerializer):
    choices = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Questions
        fields = ('id', 'questions', 'category', 'mark_type', 'question_status', 'time_limit', 'choices')

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        question = Questions.objects.create(**validated_data)

        # Assuming 'choices' is a TextField in the Questions model
        question.choices = choices_data
        question.save()

        return question
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Questions
        fields='__all__'