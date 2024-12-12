
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
from django.urls import reverse_lazy
from tutorials.forms import CreateBookingRequest, LogInForm, PasswordForm, UserForm, SignUpForm, BookingForm, CreateNewAdminForm, ConfirmedBookingForm
from tutorials.helpers import login_prohibited
from tutorials.forms import LogInForm, PasswordForm, UserForm, SignUpForm, BookingForm, UpdateBookingForm
from tutorials.helpers import login_prohibited

from tutorials.models import Student, Tutor, Booking_requests, Confirmed_booking
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from tutorials.models import Student, Tutor, Booking_requests, Confirmed_booking, User
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.db.models import Q, F, Sum
from tutorials.models import *



@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user

    # load the correct dashboard based on user type

    # if the user is an admin user
    if hasattr(current_user, 'admin'):
        return render(request, 'dashboard.html', {'user': current_user})

    # if the user is a student user
    if hasattr(current_user, 'student'):
        return render(request, 'student_dashboard.html', {'user': current_user})

    # if the user is a tutor user
    if hasattr(current_user, 'tutor'):
        return render(request, 'tutor_dashboard.html', {'user': current_user})
    


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

            if hasattr(user, 'admin'):
                return render(request, 'dashboard.html', {'user': user})

            # if the user is a student user
            if hasattr(user, 'student'):
                return render(request, 'student_dashboard.html', {'user': user})

            # if the user is a tutor user
            if hasattr(user, 'tutor'):
                return render(request, 'tutor_dashboard.html', {'user': user})

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
    

class CreateNewAdminView(LoginRequiredMixin, FormView):

    form_class = CreateNewAdminForm
    template_name = "create_new_admin.html"
    # Redirects to a reset version of the same page after creating a new admin
    success_url = reverse_lazy('create_new_admin')
    success_message = "Yes, a new admin has been made!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        admin_user = form.save(commit=False)
        admin_user.save()
        return super().form_valid(form)

class ViewBookingsView(LoginRequiredMixin, ListView):
    """Display the confirmed bookings as a table."""
    
    model = Confirmed_booking
    template_name = 'view_bookings.html'
    context_object_name = 'bookingData'

    def get_queryset(self): #override to include sorting / filtering functionality
        '''SORTING'''
        queryset = super().get_queryset() #unsorted query
        sortby = self.request.GET.get('sortby', 'booking_date') #obtain sort through url (default to booking_date)

        #maps table headers to the respective model data
        sort_keymap = {
            'date' : 'booking_date',
            'time' : 'booking_time',
            'tutor' : 'tutor__first_name',
            'student' : 'booking__student__first_name',
            'subject' : 'booking__subject',
            'difficulty' : 'booking__difficulty',
        }

        '''FILTERING'''
        filterby = self.request.GET.get('filterby', '') #obtain filter through url (default to nothing)
        searchfor = self.request.GET.get('search', '').strip() #get text to filter by, uses .strip for formatting

        if not (filterby == '' or searchfor == ''):
            #student and tutor models have first and last names as seperate fields
            #the code below allows both to be searched based on the input
            if filterby == 'tutor':
                queryset = queryset.filter(
                    Q(tutor__first_name__icontains=searchfor) | #first name
                    Q(tutor__last_name__icontains=searchfor) | #last name
                    Q(tutor__first_name__icontains=searchfor.split()[0], #first and last name together
                    tutor__last_name__icontains=" ".join(searchfor.split()[1:])) #uses .split to parse the user input
                )
            elif filterby == 'student':
                queryset = queryset.filter(
                    Q(booking__student__first_name__icontains=searchfor) | #first name
                    Q(booking__student__last_name__icontains=searchfor) | #last name
                    Q(booking__student__first_name__icontains=searchfor.split()[0], #first and last name together
                    booking__student__last_name__icontains=" ".join(searchfor.split()[1:]))
                )
            else:
                filter_keymap = {
                    'subject': 'booking__subject__icontains',
                    'difficulty': 'booking__difficulty__icontains',
                }
                queryset = queryset.filter(**{filter_keymap.get(filterby): searchfor})

        return queryset.order_by(sort_keymap.get(sortby, 'booking_date'))

    def delete_booking(request, id):
        # used with delete button in manage table
        obj = Confirmed_booking.objects.get(id=id)
        obj.delete()
        return redirect('view_bookings')
    
    def get(self, request, *args, **kwargs): #override to ensure forced sort
        if 'sortby' not in request.GET:
            return redirect(request.path + '?sortby=date')
        
        return super().get(request, *args, **kwargs)
    
class ViewMyBookings(LoginRequiredMixin, ListView):
    """Display the user's associated bookings as a table."""
    
    model = Confirmed_booking
    template_name = 'my_bookings.html'
    context_object_name = 'bookingData'

    def get_queryset(self): #override to include sorting / filtering functionality
        queryset = super().get_queryset() #unsorted query
        sortby = self.request.GET.get('sortby', 'booking_date') #obtain sort through url (default to booking_date)
        usertype = self.request.GET.get('user', 'student') #obtain user type through url (default to student)
        current_username = self.request.user.username #obtain logged in username

        #maps table headers to the respective model data
        keymap = {
            'date' : 'booking_date',
            'time' : 'booking_time',
            'tutor' : 'tutor__first_name',
            'student' : 'booking__student__first_name',
            'subject' : 'booking__subject',
            'difficulty' : 'booking__difficulty',
        }

        #filter only bookings related to current user
        if usertype == 'student': 
            queryset = queryset.filter(booking__student__username=current_username) 
        elif usertype == 'tutor': 
            queryset = queryset.filter(tutor__username=current_username)

        return queryset.order_by(keymap.get(sortby, 'booking_date'))
    
    def get(self, request, *args, **kwargs): #override to ensure forced sort
        current_user = request.user #obtain user info
        attempted_user_type = request.GET.get('user') #to prevent loading the wrong page

        # if the user is a admin user
        if hasattr(current_user, 'admin'): 
            #if an admin happens to load the page, send them to the correct version
            return redirect('view_bookings')
        
        # if the user is a student user
        if hasattr(current_user, 'student'):
            if attempted_user_type == 'tutor' or 'user' not in request.GET:
                return redirect(request.path + '?user=student')

        # if the user is a tutor user
        if hasattr(current_user, 'tutor'):
            if attempted_user_type == 'studentr' or 'user' not in request.GET:
                return redirect(request.path + '?user=tutor')
        
        return super().get(request, *args, **kwargs)

class ViewInvoicesView(LoginRequiredMixin, ListView):
    """Display all invoices as a table."""
    
    model = Invoices
    template_name = 'invoices.html'
    context_object_name = 'invoiceData'

    def get_queryset(self): #override to include sorting / filtering functionality
        '''SORTING'''
        queryset = super().get_queryset() #unsorted query
        sortby = self.request.GET.get('sortby', 'year') #obtain filter through url (default to booking_date)

        #maps table headers to the respective model data
        keymap = {
            'student' : 'student__first_name',
            'year' : 'year',
            'amount' : 'amount',
        }

        '''FILTERING'''
        filterby = self.request.GET.get('filterby', '') #obtain filter through url (default to nothing)
        searchfor = self.request.GET.get('search', '').strip() #get text to filter by, uses .strip for formatting

        if not (filterby == '' or searchfor == ''):
            #student models have first and last names as seperate fields
            #the code below allows both to be searched based on the input (same as above in view_bookings)
            if filterby == 'student':
                queryset = queryset.filter(
                    Q(student__first_name__icontains=searchfor) | #first name
                    Q(student__last_name__icontains=searchfor) | #last name
                    Q(student__first_name__icontains=searchfor.split()[0], #first and last name together
                    student__last_name__icontains=" ".join(searchfor.split()[1:]))
                )
            else:
                filter_keymap = {
                    'year': 'year__icontains',
                    'amount': 'amount__icontains',
                }
                queryset = queryset.filter(**{filter_keymap.get(filterby): searchfor})

        return queryset.order_by(keymap.get(sortby, 'year'))
    
    def mark_as_paid(request, id):
        # sets 'paid' to true for a specific entry
        obj = Invoices.objects.get(id=id)
        obj.paid = True
        obj.save() # commit change to db

        return redirect('invoices') #refresh
    
    def mark_as_unpaid(request, id):
        # sets 'paid' to false for a specific entry
        obj = Invoices.objects.get(id=id)
        obj.paid = False
        obj.save() # commit change to db
        
        return redirect('invoices') #refresh
    
    def get(self, request, *args, **kwargs): #override to ensure forced sort
        if 'showpaid' not in request.GET or 'sortby' not in request.GET:
            return redirect(request.path + '?showpaid=false&sortby=year')
        
        return super().get(request, *args, **kwargs)
    
class ViewMyPayments(LoginRequiredMixin, ListView):
    """Display the user's associated invoices as a table."""
    
    model = Invoices
    template_name = 'my_payments.html'
    context_object_name = 'invoiceData'

    def get_queryset(self): #override to include sorting / filtering functionality
        queryset = super().get_queryset() #unsorted query
        sortby = self.request.GET.get('sortby', 'year') #obtain sort through url (default to year)

        #maps table headers to the respective model data
        keymap = {
            'year' : 'year',
            'amount' : 'amount',
        }

        #filter only bookings related to current student
        current_username = self.request.user.username #obtain logged in username
        queryset = queryset.filter(student__username=current_username) 

        return queryset.order_by(keymap.get(sortby, 'year'))
    
    def get_context_data(self, **kwargs): #override to pass the sum of outstanding payments
        context = super().get_context_data(**kwargs) 
        current_username = self.request.user.username 
        total_payments = self.model.objects.filter(student__username=current_username).aggregate(Sum('amount'))['amount__sum'] 
        context['total_payments'] = total_payments 
        return context

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
from datetime import timedelta

def create_multiple_objects(request):
    if request.method == 'POST':
        form = ConfirmedBookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                # Extract details from the form
                booking_request = data['booking']
                tutor = data['tutor']
                start_date = data['booking_date']
                booking_time = data['booking_time']

                # Create 10 weekly bookings starting from the selected date
                objects = []
                for i in range(10):
                    booking_date = start_date + timedelta(weeks=i)
                    obj = Confirmed_booking(
                        booking=booking_request,
                        tutor=tutor,
                        booking_date=booking_date,
                        booking_time=booking_time
                    )
                    objects.append(obj)

                # Bulk create the bookings
                Confirmed_booking.objects.bulk_create(objects)

                # Mark the booking request as confirmed
                booking_request.isConfirmed = True
                booking_request.save()

                # Redirect to the view bookings page with a success message
                messages.success(request, "10 weekly bookings created successfully")
                return redirect('view_requests')
            except Exception as e:
                messages.error(request, f"Error creating bookings: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = ConfirmedBookingForm()

    return render(request, 'splitscreen.html', {'form': form})



# displaying the form to create a new booking request
@login_required
def creatingBookingRequest(request):
    if request.method == 'POST':
        form = CreateBookingRequest(request.POST)
        print("DEBUG: Form is bound:", form.is_bound)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                student = Student.objects.get(username=request.user.username)
                instance.student = student
                instance.save()
            else:
                print("no user logged in")
            print("DEBUG: Form is valid")
            form.save()
            return redirect("dashboard")
        else:
            print("DEBUG: Form errors:", form.errors)
    else:
        form = CreateBookingRequest()

    template_name = "create_booking_requests.html"
    return render(request, template_name, context={'form': form})
    

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


def updateBooking(request, booking_id):
    try:
        booking = Confirmed_booking.objects.get(id=booking_id)
    except Confirmed_booking.DoesNotExist:
        raise Http404(f"Could not find booking with ID {booking_id}") 
    
    if request.method == "POST":
        form = UpdateBookingForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, "It was not possible to update these booking details to the database.")
            else:
                return redirect("view_bookings")
    else:
        form = UpdateBookingForm(instance=booking)
    return render(request, 'update_booking.html', {'booking_id': booking_id, 'form': form})


def display_all_booking_requests(request, booking_id=None):
    # Get all unconfirmed booking requests
    data = Booking_requests.objects.filter(isConfirmed=False)

    selected_booking = None
    form = None
    data2 = Tutor.objects.all()  # Default to show all tutors

    if booking_id:
        # Fetch the selected booking
        selected_booking = get_object_or_404(Booking_requests, id=booking_id)

        # Filter tutors by the skill required for the selected booking
        data2 = Tutor.objects.filter(skills=selected_booking.subject)

        # Initialize the form for the Confirmed Booking
        if request.method == 'POST':
            form = ConfirmedBookingForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('view_requests')  # Redirect to prevent resubmission
        else:
            form = ConfirmedBookingForm(initial={'booking': selected_booking})

    return render(
        request,
        "view_requests.html",
        {
            "data": data,
            "data2": data2,
            "selected_booking": selected_booking,
            "form": form,
        },
    )


# view function to display all users in one page
def display_all_users(request):
   admin = User.objects.values('id','username', 'first_name', 'last_name', 'email').exclude(student__isnull=False).exclude(tutor__isnull=False)
   students = Student.objects.values('id','username', 'first_name', 'last_name', 'email')
   tutors = Tutor.objects.values('id','username', 'first_name', 'last_name', 'email')
   return render(request, "view_users.html", {"admin" : admin, 'students': students, 'tutors': tutors})

# view function to be able to delete a user when logged in as an admin
def delete_user(request, id):
    obj = User.objects.get(id=id)
    obj.delete()
    return redirect('view_users')

# view function to update a user's details when logged in as an admin
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404(f"Could not find user with ID {user_id}") 
    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, "It was not possible to update these user details to the database.")
            else:
                return redirect("view_users")
    else:
        form = UserForm(instance=user)
    return render(request, 'update_user_details.html', {'user_id': user_id, 'form': form})
