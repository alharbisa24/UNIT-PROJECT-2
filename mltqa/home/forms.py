from django import forms

class RegisterForm(forms.Form):
    full_name =forms.CharField(max_length=50,
                error_messages={
                    "required":"يرجى ادخال الاسم الكامل",
                    "max_length":"يرجى ادخال الايميل",
                })
    email = forms.EmailField(max_length=50,
                             error_messages={
            'required': 'يجب ادخال الايميل',
            'max_length': 'يجب ادخال الايميل بشكل صحيح',
        },)
    phone = forms.CharField(max_length=50,
                             error_messages={
            'required': 'يجب ادخال رقم الجوال',
            'max_length': 'يجب ادخال رقم الجوال بشكل صحيح',
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