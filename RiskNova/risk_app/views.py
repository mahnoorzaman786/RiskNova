from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render

from .forms import RiskPredictionForm
from .ml_service import predict_risk, save_prediction_record
from .models import ProjectRiskPrediction


def _prediction_context(prediction):
    return {
        'prediction': prediction,
        'risk_level': prediction.risk_level.upper(),
        'risk_probability': round(float(prediction.risk_probability), 2),
        'confidence': round(float(prediction.confidence), 2),
        'main_factors': prediction.main_contributing_factors,
        'recommendations': prediction.recommendations,
    }


def home(request):
    return render(request, 'home.html')


def predict_form(request):
    if request.method == 'POST':
        form = RiskPredictionForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['estimated_cost'] = Decimal(str(form_data['estimated_cost']))
            prediction_result = predict_risk(form_data)
            prediction = save_prediction_record(form_data, prediction_result)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return render(request, '_prediction_result.html', _prediction_context(prediction))

            return redirect('result', prediction_id=prediction.id)
    else:
        form = RiskPredictionForm()

    return render(request, 'predict_form.html', {'form': form})


def result(request, prediction_id):
    prediction = get_object_or_404(ProjectRiskPrediction, id=prediction_id)
    return render(request, 'result.html', _prediction_context(prediction))


def dashboard(request):
    predictions = ProjectRiskPrediction.objects.all()[:10]
    total = ProjectRiskPrediction.objects.count()
    high = ProjectRiskPrediction.objects.filter(risk_level__iexact='HIGH').count()
    medium = ProjectRiskPrediction.objects.filter(risk_level__iexact='MEDIUM').count()
    low = ProjectRiskPrediction.objects.filter(risk_level__iexact='LOW').count()

    risk_distribution = {
        'High Risk': high,
        'Medium Risk': medium,
        'Low Risk': low,
    }

    high_percent = round((high / total) * 100, 1) if total else 0
    medium_percent = round((medium / total) * 100, 1) if total else 0
    low_percent = round((low / total) * 100, 1) if total else 0

    context = {
        'predictions': predictions,
        'total_predictions': total,
        'high_risk_projects': high,
        'medium_risk_projects': medium,
        'low_risk_projects': low,
        'risk_distribution': risk_distribution,
        'high_percent': high_percent,
        'medium_percent': medium_percent,
        'low_percent': low_percent,
    }
    return render(request, 'dashboard.html', context)
