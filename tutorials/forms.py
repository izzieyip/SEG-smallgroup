
"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Confirmed_booking, Student, Tutor, Admin
from .models import Booking_requests, User, Student, Confirmed_booking

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""
    userType = forms.ChoiceField(choices=[('S', 'Student'), ('T', 'Tutor')], required=True, label="Type of User")

    class Meta:
        model = Student
        fields = ['userType', 'first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        # Retrieve the data passed to the form
        data = kwargs.get('data', {})
        userType = data.get('userType')
        super().__init__(*args, **kwargs)

        # Dynamically update fields based on userType
        if userType == 'T':
            self.fields.update(forms.models.fields_for_model(
                Tutor,
                fields=['first_name', 'last_name', 'username', 'email', 'skills', 'experience_level', 'available_days', 'available_times']
            ))
        elif userType == 'S':
            self.fields.update(forms.models.fields_for_model(
                Student,
                fields=['first_name', 'last_name', 'username', 'email']
            ))

    def save(self):
        """Create a new user of the selected type."""
        if self.is_valid():
            userType = self.cleaned_data.get('userType')
            if userType == 'T':
                tutor = Tutor.objects.create_user(
                    username= self.cleaned_data.get('username'),
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get("last_name"),
                    email=self.cleaned_data.get('email'),
                    password=self.cleaned_data.get('new_password'),
                    skills=self.cleaned_data.get('skills'),
                    experience_level=self.cleaned_data.get('experience_level'),
                    available_days=self.cleaned_data.get('available_days'),
                    available_times=self.cleaned_data.get('available_times')
                )
                return tutor
            elif userType == 'S':
                student = Student.objects.create_user(
                    username = self.cleaned_data.get('username'),
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get("last_name"),
                    email=self.cleaned_data.get('email'),
                    password=self.cleaned_data.get('new_password'))
                return student



class CreateNewAdminForm(forms.ModelForm, NewPasswordMixin):
    """Form enabling admins to create NEW admins once logged in"""
    class Meta:
        model = Admin
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        # Retrieve the data passed to the form
        data = kwargs.get('data', {})
        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        """Create a new admin user with this data."""
        if self.is_valid():
            admin = Admin.objects.create_user(
                username = self.cleaned_data.get('username'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get('new_password'),
            )
        return admin

      
class CreateBookingRequest(forms.ModelForm):
    """Form for a student to create a new booking request"""

    class Meta:
        model = Booking_requests
        fields = ['subject', 'difficulty']




skills = [
    ("CPP", "C++"),
    ("JA", "JAVA"),
    ("PY", "PYTHON"),
    ("DJ", "DJANGO")
]


class BookingForm(forms.Form):
    #form to create a insert a new booking into the table
    student = forms.CharField(label="Student username", max_length=255)
    subject = forms.ChoiceField(choices=skills)
    date = forms.DateField(label="Date")
    time = forms.TimeField(label = "Time")
    tutor = forms.CharField(label="Tutor username", max_length=255)


class ConfirmedBookingForm(forms.ModelForm):
    class Meta:
        model = Confirmed_booking
        fields = ['booking', 'tutor', 'booking_date', 'booking_time']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'booking': forms.Select(attrs={'class': 'form-select'}),
            'tutor': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'booking': 'Booking Request',
            'tutor': 'Tutor',
            'booking_date': 'Date',
            'booking_time': 'Time',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict booking choices to only unconfirmed bookings
        self.fields['booking'].queryset = Booking_requests.objects.filter(isConfirmed=False)



class UpdateBookingForm(forms.ModelForm):
    # a form to aid in the updating of bookings
    class Meta:
        model = Confirmed_booking
        fields = ["booking_date", "booking_time", "tutor"]

