from django import forms


class AdminForm(forms.Form):
    full_name= forms.CharField(max_length=50,
            error_messages={
            'required': 'يجب ادخال الاسم',
            'max_length': 'يجب ادخال الاسم بشكل صحيح',
        },)
    email = forms.EmailField(max_length=50,
                             error_messages={
            "invalid": "يرجى ادخال بريد الكتروني صحيح",
            'required': 'يجب ادخال الايميل',
            'max_length': 'يجب ادخال الايميل بشكل صحيح',
        },)
    password = forms.CharField(min_length=8,
        widget=forms.PasswordInput,
        error_messages={
            'required': 'يجب ادخال كلمة المرور',
            'min_length': 'يجب ادخال كلمة المرور بشكل صحيح',
        },
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
            error_messages={
            'required': 'يجب ادخال تاكيد كلمة المرور',
            'min_length': 'يجب ادخال تاكيد كلمة المرور بشكل صحيح',
        },
    )

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50,
                             error_messages={
            'required': 'يجب ادخال الايميل',
            'max_length': 'يجب ادخال الايميل بشكل صحيح',
        },)
    password = forms.CharField(min_length=8,
        widget=forms.PasswordInput,
        error_messages={
            'required': 'يجب ادخال كلمة المرور',
            'min_length': 'يجب ادخال كلمة المرور بشكل صحيح',
        },
    )


class EventForm(forms.Form):
    title = forms.CharField(max_length=50,
                             error_messages={
            'required': 'يجب ادخال العنوان',
            'max_length': 'يجب ادخال العنوان بشكل صحيح',
        },)

    description = forms.CharField(max_length=500,
                             error_messages={
            'required': 'يجب ادخال الوصف',
            'max_length': 'يجب ادخال الوصف بشكل صحيح',
        },)
    location = forms.URLField(
        validators=[],
        error_messages={
            'required': 'يجب ادخال الرابط',
            'invalid': 'يجب ادخال رابط صالح',
        },
    )

    available_seats = forms.IntegerField(
                             error_messages={
            'required': 'يجب ادخال عدد المقاعد',
        },)
    
    start_datetime = forms.DateTimeField(
        error_messages={
            'required': 'يجب ادخال تاريخ ووقت البداية',
            'invalid': 'يرجى إدخال تاريخ ووقت صالحين',
        },
    )
    
    end_datetime = forms.DateTimeField(
        error_messages={
            'required': 'يجب ادخال تاريخ ووقت النهاية',
            'invalid': 'يرجى إدخال تاريخ ووقت صالحين',
        },
    )
  
    image = forms.ImageField(required=False)