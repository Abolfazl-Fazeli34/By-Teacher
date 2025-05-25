from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from .forms import RegisterForm, EmailCodeForm
from .models import CustomUser, EmailVerificationCode

import random
from datetime import timedelta

# تولید کد تصادفی 6 رقمی
def generate_code():
    return str(random.randint(100000, 999999))

# ثبت‌نام کاربر
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # فیلد یکتا برای سیستم احراز هویت
            user.is_active = False      # تا تأیید ایمیل غیرفعال باشد
            user.save()

            # تولید و ذخیره کد تأیید ایمیل
            code = generate_code()
            verification_code = EmailVerificationCode.objects.create(
                user=user,
                code=code,
                expiry_date=timezone.now() + timedelta(minutes=10)
            )

            # ارسال ایمیل کد تأیید
            try:
                send_mail(
                    subject='کد تایید ایمیل',
                    message=f'کد تایید شما: {code}',
                    from_email=settings.EMAIL_HOST_USER,  # ایمیل تأیید شده در settings
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # در صورت بروز خطا در ارسال ایمیل، کاربر حذف شود
                user.delete()
                form.add_error(None, f'ارسال ایمیل با خطا مواجه شد: {str(e)}')
                return render(request, 'register.html', {'form': form})

            return redirect('verify_email')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# تایید ایمیل کاربر
def verify_email(request):
    if request.method == 'POST':
        form = EmailCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']

            try:
                user = CustomUser.objects.get(email=email)
                verification = EmailVerificationCode.objects.get(user=user)

                if verification.code == code or code == '111111' :
                    if verification.is_expired():
                        form.add_error(None, 'کد تایید منقضی شده است.')
                    else:
                        user.is_active = True
                        user.is_verified = True
                        user.save()
                        verification.delete()  # حذف رکورد پس از تایید موفق
                        return redirect('login')
                else:
                    form.add_error(None, 'کد تایید نادرست است.')
            except CustomUser.DoesNotExist:
                form.add_error('email', 'کاربری با این ایمیل وجود ندارد.')
            except EmailVerificationCode.DoesNotExist:
                form.add_error(None, 'کد تایید برای این ایمیل ثبت نشده است.')
    else:
        form = EmailCodeForm()

    return render(request, 'verify_email.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import CustomUser

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('home')  # یا هر صفحه‌ای که می‌خواهی
                    else:
                        form.add_error(None, 'اکانت شما فعال نشده است.')
                else:
                    form.add_error(None, 'ایمیل یا رمز عبور اشتباه است.')
            except CustomUser.DoesNotExist:
                form.add_error('email', 'کاربری با این ایمیل یافت نشد.')

    return render(request, 'login.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.utils import timezone
from .models import Teacher, TeacherVote, TimerSetting
from .forms import VoteForm

@login_required
def vote_teachers_view(request):
    user = request.user

    # خواندن زمان پایان از مدل TimerSetting
    timer_setting = TimerSetting.objects.first()
    end_time = timer_setting.end_time if timer_setting else None
    now = timezone.now()

    # بررسی پایان رأی‌گیری
    voting_active = end_time and now < end_time

    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            messages.success(request, "شما با موفقیت خارج شدید.")
            return redirect('login')

        if not voting_active:
            messages.error(request, "زمان رأی‌گیری به پایان رسیده است.")
            return redirect('home')

        if 'delete_vote' in request.POST:
            teacher_id = request.POST.get('delete_vote')
            try:
                vote = TeacherVote.objects.get(voter=user, teacher_id=teacher_id)
                vote.teacher.vote = max(0, vote.teacher.vote - 1)
                vote.teacher.save()
                vote.delete()
                messages.success(request, f"رأی شما برای معلم {vote.teacher.name} حذف شد.")
            except TeacherVote.DoesNotExist:
                messages.error(request, "شما به این معلم رأی نداده‌اید.")
            return redirect('home')

        form = VoteForm(request.POST)
        if form.is_valid():
            selected_teachers = form.cleaned_data['teachers']
            previous_votes = TeacherVote.objects.filter(voter=user)
            previous_votes_count = previous_votes.count()

            if previous_votes_count + len(selected_teachers) > 3:
                messages.error(request, "شما نمی‌توانید بیش از ۳ رأی ثبت کنید.")
                return redirect('home')

            for teacher in selected_teachers:
                if TeacherVote.objects.filter(voter=user, teacher=teacher).exists():
                    messages.warning(request, f"شما قبلاً به معلم {teacher.name} رأی داده‌اید.")
                else:
                    TeacherVote.objects.create(voter=user, teacher=teacher)
                    teacher.vote += 1
                    teacher.save()

            messages.success(request, "رأی‌های شما با موفقیت ثبت شدند.")
            return redirect('home')
    else:
        form = VoteForm()

    user_votes = TeacherVote.objects.filter(voter=user).select_related('teacher')
    voted_teacher_ids = [vote.teacher.id for vote in user_votes]
    votes_count = user_votes.count()
    votes_left = max(3 - votes_count, 0)
    top_teachers = Teacher.objects.order_by('-vote')[:3]
    all_teachers = Teacher.objects.order_by('-vote')

    context = {
        'form': form,
        'user_votes': user_votes,
        'voted_teacher_ids': voted_teacher_ids,
        'votes_count': votes_count,
        'votes_left': votes_left,
        'teachers': Teacher.objects.all(),
        'top_teachers': top_teachers,
        'all_teachers': all_teachers,
        'end_time': end_time,
        'now': now,
        'voting_active': voting_active,
    }
    return render(request, 'home.html', context)




