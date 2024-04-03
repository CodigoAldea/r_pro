from django import forms
from .models import Questions

class DynamicQuestionForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super(DynamicQuestionForm, self).__init__(*args, **kwargs)
        self.questions = questions
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=[(question.option1, question.option1),
                         (question.option2, question.option2),
                         (question.option3, question.option3),
                         (question.option4, question.option4)],
                required=True
            )
        self.fields['current_question'] = forms.HiddenInput()