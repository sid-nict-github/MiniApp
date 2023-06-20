from django.shortcuts import render, redirect
# import Forms
from Project.Forms import UserForm, UserProfileInfoForm
# import authenticate and login and logout
from django.contrib.auth import authenticate, login, logout
# for Restrict the opening of all post-login pages if the user 
# has not logged in, import
from django.contrib.auth.decorators import login_required
# for sending email, import the following for sending email
from django.core.mail import send_mail
from django.conf import settings

@login_required(login_url='signin')
def userpage2(request):
    # retrieve data from session in code
    suname = request.session.get("session_uname")
    print("Session data = " , suname)

    # initialize a result
    res = -1
    
    # check if the form has been submitted
    if request.method == 'POST':
        # form is submitted
        # fetch the data from the form
        # var = request.POST['input_type_name']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        fmessage = request.POST['message']
        # initi. variables for sending email
        subject = 'Message sent via DJANGO Application'
        message = 'New Contact on the Website'
        message = message + "<br>"
        message = message + "Name: " + name + "<br>"
        message = message + "Email: " + email + "<br>"
        message = message + "Phone: " + phone + "<br>"
        message = message + "Message: " + fmessage + "<br>"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['siddharth@nictchd.in']
        # send the email
        res = send_mail(subject, message, email_from, recipient_list)

    return render(request, 'Project/userpage2.html' , {'res':res})


# Create your views here.
def signup(request):

    # check if the user is already logged in using "is_authenticated" property of user
    if request.user.is_authenticated:
        # user is already logged in
        # redirect the user to the userhome page
        return redirect('userhome')
    else:
        # user is already not logged in
        # declare and initialize a boolean variable for signup success
        isSignupSuccess = False
        # check if the form is submitted or not
        if request.method == 'POST':
            # form submitted
            # get the form object with the User data
            userform = UserForm(data = request.POST)
            userprofileinfoform = UserProfileInfoForm(data = request.POST)
            # check if the form is valid
            if userform.is_valid() and userprofileinfoform.is_valid():
                # forms are valid
                # save the user_form data to the model
                user = userform.save()
                # hash the password field
                user.set_password(user.password)
                # save the user_form data to the model with the password
                user = userform.save()
                # save the profile_form data to the model
                profile = userprofileinfoform.save()
                # set the profile's user object
                profile.user = user
                # save the profile data again
                profile.save()

                # reset the signup success variable to True
                isSignupSuccess = True
            else:
                # forms are invalid
                # display the errors
                print(userform.errors)
                print(userprofileinfoform.errors)
        else:
            # form not submitted
            # for the 1st time load, create an empty form
            # create object of UserForm
            userform = UserForm()
            # create object of UserProfileInfoForm
            userprofileinfoform = UserProfileInfoForm()
        
        # render the template and pass the forms & the signup success boolean variable
        return render(request, 'Project/signup.html',{'userform':userform , 'userprofileinfoform': userprofileinfoform , 'isSignupSuccess' : isSignupSuccess})



def signin(request):
    # check if the user is already logged in using "is_authenticated" property of user
    if request.user.is_authenticated:
        # user is already logged in
        # redirect the user to the userhome page
        return redirect('userhome')
    else:
        # user is already not logged in
        # declare a variable for signin success
        isSigninSuccess = 0     # form not submitted

        # check if the form was submitted or not
        if request.method == 'POST':
            # form submitted
            # get the data from the textboxes
            uname = request.POST.get('username')
            passw = request.POST.get('password')
            # check if the username, password are correct
            # using authenticate()
            user = authenticate(request, username=uname, password=passw)
            # check if user data is correct
            if user:
                # user data is correct
                # reset isSigninSuccess variable
                isSigninSuccess = 1         # user autenticated
                # check if the checkbox is checked or not
                if request.POST.get('chk' , 'NA') == 'Remeber Me':
                    ###### Cookie Creation #######
                    # Step 1: prepare an HttpResponse object:
                    response = render(request,"userhome")
                    # Step 2: create the cookie:
                    response.set_cookie("cookie_key_uname" , uname, 3*60)   # max_age in seconds
                    response.set_cookie("cookie_key_pass" , passw, 3*60)
                    # store data in the session
                    request.session["session_uname"] = uname
                    # login the user using login()
                    login(request, user)
                    # Step 3: save the cookie file on the client device
                    return response
                    ##############################
                # store data in the session
                request.session["session_uname"] = uname
                # login the user using login()
                login(request, user)
                # redirect to userhome page
                return redirect('userhome')
            else:
                # user data is incorrect
                # reset isSigninSuccess variable
                isSigninSuccess = 2     # user unauthenticated
                # display empty form & pass some message
                return render(request, 'Project/signin.html', context={'isSigninSuccess':isSigninSuccess})
        else:
            # form not submitted
            # check if the cookie is created or not
            if request.COOKIES.get('cookie_key_uname' , 'NA') != 'NA':
                # cookie is already created
                # create an empty dictionary
                mydata = {}
                # retrieve cookie values and insert in the dictionary
                mydata['cookie_uname_value'] = request.COOKIES['cookie_key_uname']
                mydata['cookie_passw_value'] = request.COOKIES['cookie_key_pass']
                # display the form and send the dictionary with retrieved username and password
                return render(request, 'Project/signin.html' , mydata)
            else:
                # cookie is not created
                # display the empty form
                return render(request, 'Project/signin.html', context={'isSigninSuccess':isSigninSuccess})
    
# to Restrict the opening of all post-login pages if the user has not logged in, 
# type the following on top of all post-login pages
@login_required(login_url='signin')
def userhome(request):
    # retrieve data from session in code
    suname = request.session.get("session_uname")
    print("Session data = " , suname)
    return render(request, 'Project/userhome.html')

def signout_user(request):
    # destroy the session
    del request.session["session_uname"]
    request.session.flush()
    # destroy the session - call the built-in function - logout()
    logout(request)
    # redirect the user to the home page
    return redirect('signin')