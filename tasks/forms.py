from django import forms
from tasks.models import Task,TaskDetail,Project

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label='Task Title')
    description = forms.CharField(widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label='Due Date')
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple ,choices=[], label='Assigned To')

    def __init__(self, *args, **kwargs): 
        # print(args,kwargs)
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id,  emp.name) for emp in employees]




class StyledFormMixin:
    """mixin to apply in form feild"""

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-md focus:border-red-400 focus:ring-rose-500 focus:outline-none"

    def apply_styled_widget(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}",
                    'rows':5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 border-gray-300 p-3 rounded-lg shadow-md focus:border-red-400 focus:ring-rose-500 focus:outline-none"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'space-y-2'
                })

            else:
                field.widget.attrs.update({
                    'class' : self.default_classes
                })

#django model form

class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model= Task
        fields = ['title', 'description', 'due_date','assigned_to']

        widgets = {
            'due_date' : forms.SelectDateWidget,
            'assigned_to' : forms.CheckboxSelectMultiple
        }

        # exclude = ('is_completed','project','created_at','updated_at')

        """"using mixin widgets"""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()   
            
class TaskDetailModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes', 'asset']

    
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.apply_styled_widget()




class CreateProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date']

        widgets = {
            'description' : forms.Textarea,
            'start_date' : forms.SelectDateWidget
        }