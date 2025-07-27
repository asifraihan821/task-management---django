from django.contrib.auth.models import Permission,Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
import re
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1','password2']:
            self.fields[fieldname].help_text = None


class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError('email already exists')
        
        return email

    def clean_password1(self):

        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('password must be atleast 8 charecters')
        
        if not re.search(r'[A-Z]', password1):
            errors.append('password must iclude at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            errors.append('password must include at least one lowercase letter')
        
        if not re.search(r'[0-9]', password1):
            errors.append('password must include atleast one number')

        if not re.search(r'[@#$%&*+=]', password1):
            errors.append('password must include atleast one charecter')

        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    # non-field error
    def clean(self):      
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError('password does not match')
        
        return cleaned_data
    

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AssignedRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label='Select a Role',
    )


class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name','permissions']


class CustomPasswordChangeForm(StyledFormMixin,PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyledFormMixin,PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyledFormMixin,SetPasswordForm):
    pass


"""
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta: 
        model = User
        fields = ['email', 'first_name','last_name']

    bio = forms.CharField(required=False, widget=forms.Textarea, label='bio')
    profile_image = forms.ImageField(required=False, label='profile_image')

    def __init__(self,*args,**kwargs):
        self.userprofile = kwargs.pop('userprofile',None)
        super().__init__(*args,**kwargs)
        print('forms',self.userprofile)

        # Todo: handle error

        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)

        #save userprofile jodi thake

        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')

            if commit:
                self.userprofile.save()
            
        if commit:
            user.save()

        return user
    """


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name','bio','profile_image']
