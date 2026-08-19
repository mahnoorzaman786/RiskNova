from django.db import models


class ProjectRiskPrediction(models.Model):
    project_name = models.CharField(max_length=200, default='Unnamed Project')
    project_size = models.CharField(max_length=50)
    team_size = models.IntegerField()
    project_duration = models.IntegerField()
    estimated_cost = models.DecimalField(max_digits=14, decimal_places=2)
    project_complexity = models.CharField(max_length=50)
    requirements_stability = models.CharField(max_length=50)
    requirement_changes = models.IntegerField()
    communication_level = models.CharField(max_length=50)
    project_management_quality = models.CharField(max_length=50)
    resource_availability = models.CharField(max_length=50)
    team_experience = models.CharField(max_length=50)
    technical_expertise = models.CharField(max_length=50)
    testing_level = models.CharField(max_length=50)
    quality_factors = models.CharField(max_length=50)
    previous_defects = models.IntegerField()

    risk_level = models.CharField(max_length=30)
    risk_category = models.CharField(max_length=30)
    risk_probability = models.FloatField()
    confidence = models.FloatField()
    main_contributing_factors = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.project_name} - {self.risk_level}'
