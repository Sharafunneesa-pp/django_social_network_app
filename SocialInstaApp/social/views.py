from functools import wraps
from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView,ListView
from django.contrib.auth.models import User
from social.forms import RegistrationForm,LoginForm,UserProfileForm,PostForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from social.models import UserProfile,Posts,Comments
# for class based decoration there is decorater :-method_decorator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.

# to check whether the user is login or not-for that create a function to authenticate.

def signin_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request, *args, **kwargs)
        
    return wrapper

decs=[signin_required,never_cache]

# def signin_required(fn):
#     def wrapper(request,*args,**kwargs):
#         if not request.user.is_authenticated:
#             return redirect("signin")
#         else:
#             return fn(request,*args,**kwargs)
        
#     return wrapper    








#View,CreateView,ListView,UpdateView,DetailView,FormView
class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")    

class SignInView(FormView):
    form_class=LoginForm
    template_name="signin.html"
# check whether username and password are correct then session start
    def post(self,request,*args,**kwargs):
       form=LoginForm(request.POST)
       if form.is_valid():
           
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})
    
# listview also seen in the same page itself so no need of new class listview can inherit
@method_decorator(decs,name="dispatch")             
class IndexView(CreateView,ListView):
    model=Posts
    form_class=PostForm
    template_name="home.html"
    success_url=reverse_lazy("home")
    context_object_name="posts"
    
    
    # at the time of saving, mention the user to save that in database.
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
   
   
    # we want to list all in the order , last pposted first one. so for that we have to sort it descending order
    # we can use get_queryset for that
    def get_queryset(self):
        return Posts.objects.all().order_by("-created_date")

    

    # to add extra context in an already context data.
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        userprofiles=UserProfile.objects.all()
        lst=[]
        for pro in userprofiles:
            for u in pro.followings.all():
                lst.append(u)
        print("followers count of loggined user",lst.count(self.request.user))
        context['fwsc']=lst.count(self.request.user)
        return context
        










#localhost:8000/posts/<int:pk>/comments/add
@method_decorator(decs,name="dispatch")             
class AddCoomentView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=Posts.objects.get(id=id)
        usr=request.user
        cmnt=request.POST.get("comment")
        Comments.objects.create(user=usr,post=pst,comment=cmnt)
        return redirect("home")
    






@method_decorator(decs,name="dispatch")             
class ProfileCreateView(CreateView):
    form_class=UserProfileForm
    template_name="profile_add.html"
    success_url=reverse_lazy("home")

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
        


# No need of override this much like below code  instead use above code  
    # def post(self,request,*args,**kwargs):
    #    form=UserProfileForm(request.POST,files=request.FILES)
    #    if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         return redirect("home")
    #    else:
    #         return render(request,self.template_name,{"form":form})

  
@method_decorator(decs,name="dispatch")             
class MyProfileView(TemplateView):
    template_name='profile.html'


@method_decorator(decs,name="dispatch")             
class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile_edit.html"
    success_url=reverse_lazy("myprofile")


@method_decorator(decs,name="dispatch")             
class PostCreateView(CreateView):
    model=Posts
    form_class=PostForm
    template_name="home.html"
    success_url=reverse_lazy("home")



# post1/<int:pk>/likes/add
@method_decorator(decs,name="dispatch")                 
class AddLikeView(View):
    def get(self,request,*args,**kwargs):
        # taking id from url
        id=kwargs.get("pk")
        # taking the post having this id
        pst=Posts.objects.get(id=id)
        # like that post-many to mny field
        pst.liked_by.add(request.user)
        pst.save()
        return redirect("home")

@signin_required
@never_cache
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")    

# localhost:8000/users/<int:pk>/following/add

def following_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    usr=User.objects.get(id=id)
    request.user.profile.followings.add(usr)
    return redirect("home")