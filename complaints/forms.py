from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["title", "department", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "e.g., Leaking tap in Washroom 2"}
        )
        self.fields["department"].widget.attrs.update({"class": "form-select"})
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "rows": 5,
                "placeholder": "Provide more details here (optional)",
            }
        )


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["department", "status", "staff_remarks"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].widget.attrs.update({"class": "form-select"})
        self.fields["status"].widget.attrs.update({"class": "form-select"})
        self.fields["staff_remarks"].widget.attrs.update(
            {
                "class": "form-control",
                "rows": 4,
                "placeholder": "Add notes for the student or other staff members here...",
            }
        )
