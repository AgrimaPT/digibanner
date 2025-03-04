from django import forms
from django.forms.widgets import DateInput, TimeInput
from datetime import datetime
from .models import Banner

class BannerForm(forms.ModelForm):
    is_scheduled = forms.BooleanField(required=False, label="Scheduled Banner", initial=False)
    
    # Extra fields for separate date and time input
    start_date = forms.DateField(
        required=False,
        widget=DateInput(attrs={'type': 'date'}),
        label="Start Date"
    )
    start_time_input = forms.TimeField(
        required=False,
        widget=TimeInput(attrs={'class': 'timepicker', 'placeholder': 'hh:mm AM/PM'}),
        label="Start Time",
        input_formats=['%I:%M %p'],
        error_messages={'invalid': 'Please enter a valid time in hh:mm AM/PM format.'}
    )
    end_date = forms.DateField(
        required=False,
        widget=DateInput(attrs={'type': 'date'}),
        label="End Date"
    )
    end_time_input = forms.TimeField(
        required=False,
        widget=TimeInput(attrs={'class': 'timepicker', 'placeholder': 'hh:mm AM/PM'}),
        label="End Time",
        input_formats=['%I:%M %p'],
        error_messages={'invalid': 'Please enter a valid time in hh:mm AM/PM format.'}
    )
    
    class Meta:
        model = Banner
        # Only include model fields (title, image, active).
        fields = ['title', 'media', 'active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].widget.attrs.update({'accept': 'image/*,video/*'})
        # Prefill extra fields if editing an existing instance.
        if self.instance and self.instance.start_time:
            self.fields['start_date'].initial = self.instance.start_time.date()
            self.fields['start_time_input'].initial = self.instance.start_time.strftime('%I:%M %p')
        if self.instance and self.instance.end_time:
            self.fields['end_date'].initial = self.instance.end_time.date()
            self.fields['end_time_input'].initial = self.instance.end_time.strftime('%I:%M %p')
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time_input = cleaned_data.get('start_time_input')
        end_date = cleaned_data.get('end_date')
        end_time_input = cleaned_data.get('end_time_input')
        is_scheduled = cleaned_data.get('is_scheduled')
        
        # If any date/time value is provided, assume scheduled.
        if start_date or start_time_input or end_date or end_time_input:
            cleaned_data['is_scheduled'] = True
        
        if cleaned_data.get('is_scheduled'):
            # Only raise an error if scheduled is checked and fields are missing.
            if not (start_date and start_time_input and end_date and end_time_input):
                raise forms.ValidationError("All date and time fields are required for scheduled banners.")
            else:
                cleaned_data['start_time'] = datetime.combine(start_date, start_time_input)
                cleaned_data['end_time'] = datetime.combine(end_date, end_time_input)
        else:
            cleaned_data['start_time'] = None
            cleaned_data['end_time'] = None
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_time = self.cleaned_data.get('start_time')
        instance.end_time = self.cleaned_data.get('end_time')
        if commit:
            instance.save()
        return instance
