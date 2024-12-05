
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tutorials.forms import LogInForm, PasswordForm, UserForm, SignUpForm, BookingForm
from tutorials.helpers import login_prohibited
from tutorials.models import Booking_requests, Confirmed_booking
from django.db.models import Q
from tutorials.models import Confirmed_booking, Student, Tutor
from tutorials.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateBookingRequest, BookingForm
from tutorials.helpers import login_prohibited
from tutorials.models import Student, Tutor, Booking_requests, Confirmed_booking
from django.http import HttpResponse, HttpResponseRedirect



@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get_form_kwargs(self):
        """Pass `POST` data to the form for dynamic field updates so that it can change the form
        if user selects that they are a tutor"""
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    

class ViewBookingsView(LoginRequiredMixin, ListView):
    """Display the confirmed bookings as a table."""
    
    model = Confirmed_booking
    template_name = 'view_bookings.html'
    context_object_name = 'bookingData'

    def delete_booking(request, id):
        # used with delete button in manage table
        obj = Confirmed_booking.objects.get(id=id)
        obj.booking.delete() #delete Booking_requests object too
        obj.delete()
        return redirect('view_bookings')


#UPDATE BELOW TO A CLASS
#needs import model and the data when merged 
"""
@login_required
def ViewInvoices(request): 
    ''' UNCOMMENT BELOW WHEN ADMIN USERS ARE IMPLEMENTED
    #Block permission if the user is not an Admin
    if not request.user.is_superuser == True:
        return render(request, 'permission_denied.html') '''

    invoice_data = Invoice.objects.get( ) #Fetch all invoices that are outstanding
    context = {'invoiceData':invoice_data}
    return render(request, 'invoices.html', context) """

#task 5 booking searching
#this function is to be assinged to the search button and takes the input of the search bar
#depending on what results are needed, call the respective booking function
def search_booking_requests(query):
    if not query:
        # If query is empty or None, return all bookings or handle as needed
        return Booking_requests.objects.all()

    bookings = Booking_requests.objects.filter(
        Q(student__full_name__icontains=query) |
        Q(subject__icontains=query)
    )
    return bookings

def search_confirmed_requests(query):
    if not query:
        # If query is empty or None, return no results
        return Confirmed_booking.objects.all()

    bookings = Confirmed_booking.objects.filter(
        Q(tutor__full_name__icontains=query) |
        Q(booking__student__full_name__icontains=query) |
        Q(booking_date__icontains=query)
    )
    return bookings

#"MyForm" palceholder for the create a confirmed booking form
#i changed ^ to booking form - izzy
def create_multiple_objects(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #can add to the form if we want them to have ana option fo how many bookings they want
            #number_of_objects = int(request.POST.get('number_of_objects', 1))  # Get the number from the request
            objects = []
            #number of bookings can be changed set to 10 for a term
            for i in range(10):
                obj = Confirmed_booking(tutor=data['tutorid'],booking_date=[i*7+form.date])#fill according to form make it work
                objects.append(obj)
            Confirmed_booking.objects.bulk_create(objects)
            return redirect('view_bookings.url')#repalce with correct url if wrong?
    else:
        form = BookingForm()
    #replace splitscreen.html with actual name
    return render(request, 'splitscreen.html', {'form': form})


# displaying the form to create a new booking request
def CreatingBookingRequest(request):
    
    model = Booking_requests
    form_class = CreateBookingRequest()
    template_name = "create_booking_requests.html"
    return render(request, template_name,  context = {'form':form_class})


def createBooking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            studentuser = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            tutoruser = form.cleaned_data['tutor']
            #search for bookingrequest object, search for tutor object
            try:
                ()
                student = Student.objects.get(username=studentuser)
                tutor = Tutor.objects.get(username=tutoruser)
                bookingrequest = Booking_requests.objects.get(student=student, subject=subject)
                booking = Confirmed_booking(booking=bookingrequest, tutor=tutor, booking_date=date, booking_time=time)
                booking.save()
            except:
                form.add_error(None, "This request is not possible")
            else:
                path = reverse('dashboard')
                return HttpResponseRedirect(path)
    else:
        form = BookingForm()
    return render(request, 'create_booking.html', {'form': form})


def updateBooking(request, bookingid):

    booking = Confirmed_booking.objects.get(id=bookingid)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking) 
        if form.is_valid():
            try:
                ()
                booking.save()
            except:
                form.add_error(None, "Changes NOT saved - error occured.")
            else:
                path = reverse('dashboard')
                return HttpResponseRedirect(path)
            
    else:
        form = BookingForm(instance=booking)
    return render(request, 'update_booking.html', {'form': form})

def display_all_booking_requests(request):
    data = Booking_requests.objects.all()
    data2 = Tutor.objects.all()
    return render(request, "view_requests.html", {"data": data, "data2": data2})
