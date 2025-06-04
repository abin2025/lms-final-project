
from django import forms

from .models import Course,Categorychoice,Levelchoice,Typechoice

class CourseCreateForm(forms.ModelForm):

    class Meta:

        model = Course

        # fields = ['title','description','image','category','level','fee','offer_fee']     # to include specific fields in the form
        # fields = '__all__'          # to include all fields in the form
        exclude = ['instructor','uuid','active_status']      # Exclude the instructors field from the form

        widgets = {          # widgets --- to customize the form fields
            
            'title': forms.TextInput(attrs={'class' : 'form-control',
                                            'placeholder' : 'Enter Course Name',
                                            'required' : 'required'}),

            'image': forms.FileInput(attrs={'class' : 'form-control',
                                            }),

            'description': forms.Textarea(attrs={'class' : 'form-control',
                                                 'placeholder' : 'Enter Course Description',
                                                 'required' : 'required'}),

            'fee' : forms.NumberInput(attrs= {'class' : 'form-control',
                                            'placeholder' : 'Enter Course Fee',
                                            'required' : 'required'}),

            'offer_fee' : forms.NumberInput(attrs= {'class' : 'form-control',
                                            'placeholder' : 'Enter Offer Fee'}),

        }

    category = forms.ChoiceField(choices=Categorychoice.choices,widget=forms.Select(attrs={
                                                                                            'class' : 'form-select',
                                                                                            'required' : 'required'
                                                                                            }))
        
    level = forms.ChoiceField(choices=Levelchoice.choices,widget=forms.Select(attrs={
                                                                                    'class' : 'form-select',
                                                                                    'required' : 'required'
                                                                                    }))
        
    type = forms.ChoiceField(choices=Typechoice.choices,widget=forms.Select(attrs={
                                                                                    'class' : 'form-select',
                                                                                    'required' : 'required'
                                                                                    }))

    def clean(self):

        validated_data = super().clean()

        if validated_data.get('fee') <0:

            self.add_error('fee','course fee must be gretaer than 0')
            
        if validated_data.get('fee') <0:

            self.add_error('fee','course fee must be gretaer than 0')

        return validated_data 

    def __init__(self, *args, **kwargs):

        super(CourseCreateForm,self).__init__(*args, **kwargs)

        if not self.instance :

            self.fields.get('image').widget.attrs['required'] = 'required'
