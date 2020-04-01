from django import forms

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='New Password', max_length=255, 
        widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', max_length=255, 
        widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )