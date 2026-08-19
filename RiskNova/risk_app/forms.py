from django import forms


class RiskPredictionForm(forms.Form):
    project_name = forms.CharField(
        max_length=200,
        required=False,
        label="Project Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Enterprise Resource Planning System'
        }),
        help_text="Optional project identifier for tracking and reporting."
    )

    project_size = forms.ChoiceField(
        label="Project Size",
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
            ('enterprise', 'Enterprise')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select the overall project scale based on scope and deliverables."
    )

    team_size = forms.IntegerField(
        label="Team Size",
        min_value=1,
        max_value=500,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 500,
            'placeholder': '25'
        }),
        help_text="Total number of people involved in delivery."
    )

    project_duration = forms.IntegerField(
        label="Project Duration (months)",
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 120,
            'placeholder': '12'
        }),
        help_text="Expected project completion time in months."
    )

    estimated_cost = forms.DecimalField(
        label="Estimated Cost (USD)",
        min_value=0,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'step': '1000',
            'placeholder': '150000'
        }),
        help_text="Estimated project budget in USD."
    )

    project_complexity = forms.ChoiceField(
        label="Project Complexity",
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('critical', 'Critical')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="How technically complex and interconnected the project is."
    )

    requirements_stability = forms.ChoiceField(
        label="Requirements Stability",
        choices=[
            ('unstable', 'Unstable'),
            ('moderate', 'Moderate'),
            ('stable', 'Stable'),
            ('highly_stable', 'Highly Stable')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="How likely requirements are to change during delivery."
    )

    requirement_changes = forms.IntegerField(
        label="Requirement Changes (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'max': 100,
            'placeholder': '15'
        }),
        help_text="Approximate percentage of requirements expected to change."
    )

    communication_level = forms.ChoiceField(
        label="Communication Level",
        choices=[
            ('poor', 'Poor'),
            ('average', 'Average'),
            ('good', 'Good'),
            ('very_good', 'Very Good'),
            ('excellent', 'Excellent')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Quality and frequency of communication across stakeholders."
    )

    project_management_quality = forms.ChoiceField(
        label="Project Management Quality",
        choices=[
            ('poor', 'Poor'),
            ('average', 'Average'),
            ('good', 'Good'),
            ('very_good', 'Very Good'),
            ('excellent', 'Excellent')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Overall project governance, planning, and control quality."
    )

    resource_availability = forms.ChoiceField(
        label="Resource Availability",
        choices=[
            ('scarce', 'Scarce'),
            ('limited', 'Limited'),
            ('adequate', 'Adequate'),
            ('strong', 'Strong'),
            ('abundant', 'Abundant')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Availability of people, tools, and financial backing."
    )

    team_experience = forms.ChoiceField(
        label="Team Experience",
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('good', 'Good'),
            ('high', 'High'),
            ('expert', 'Expert')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Experience of the project team in similar delivery contexts."
    )

    technical_expertise = forms.ChoiceField(
        label="Technical Expertise",
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('good', 'Good'),
            ('high', 'High'),
            ('expert', 'Expert')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Depth of technical knowledge and domain capability."
    )

    testing_level = forms.ChoiceField(
        label="Testing Level",
        choices=[
            ('minimal', 'Minimal'),
            ('basic', 'Basic'),
            ('moderate', 'Moderate'),
            ('strong', 'Strong'),
            ('comprehensive', 'Comprehensive')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Amount of verification and quality assurance coverage."
    )

    quality_factors = forms.ChoiceField(
        label="Quality Factors",
        choices=[
            ('poor', 'Poor'),
            ('average', 'Average'),
            ('good', 'Good'),
            ('very_good', 'Very Good'),
            ('excellent', 'Excellent')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Overall quality controls, standards, and engineering practices."
    )

    previous_defects = forms.IntegerField(
        label="Previous Defects",
        min_value=0,
        max_value=500,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'max': 500,
            'placeholder': '12'
        }),
        help_text="Count of defects identified in earlier phases or previous projects."
    )

    def clean_project_name(self):
        project_name = self.cleaned_data.get('project_name', '').strip()
        return project_name or 'Unnamed Project'
