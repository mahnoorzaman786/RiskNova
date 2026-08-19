# 📊 RiskNova – AI-Driven Project Risk Assessment

RiskNova is an AI-powered web application that estimates the risk level of software projects using a trained Deep Neural Network (DNN). The model is a supervised machine learning classifier that learns from structured project attributes such as complexity, team size, communication, cost, testing quality, and previous defects to classify the project as Low, Medium, or High risk.

## ✅ Accuracy

Accuracy 95.29%

## 🏗️ Built With

Built With Django 6.1, TensorFlow, Keras, scikit-learn, NumPy, Joblib

## 📜 License

License MIT

## 📌 Project Highlights

- 🔍 Predicts project risk from structured project metadata
- 🧠 Uses a trained 15-feature DNN (Deep Neural Network) for multiclass risk classification
- 📈 Provides risk probability, confidence score, and mitigation recommendations
- 🗃️ Saves historical predictions in SQLite for dashboard tracking
- 🌐 Deployed as a Django web application with a responsive UI
- 📊 Includes a dashboard for recent predictions and risk distribution
- 🧪 Supports evaluation of model performance and decision support for project managers

## 🎯 Demo

RiskNova evaluates a project’s risk using a trained AI model and returns an actionable result with contributing factors and mitigation strategies.

You can test it using the Django-based web app.

## 🔍 Screenshot

Upload project information and click predict to receive the risk result.

- ➡ Get predicted risk level
- ➡ Get probability and confidence
- ➡ View top contributing factors
- ➡ Receive recommendations

<<<<<<< HEAD
## 🎥 Video Demo

📺 [Click here to view the demo]  
=======
## 🎥 RiskNova Demo

[▶️ Watch Full Demo](https://www.youtube.com/watch?v=7qFIUv3s0K8&t=3s) 
>>>>>>> eb1c72c107d59fa31e1b7b7f67d4f2dee8e5f420
▶ Watch Demo

## 🗂️ Dataset

Size: 15 engineered project attributes for risk classification  
Labels: Low, Medium, High risk  
Features include:
- Project size
- Team size
- Project duration
- Estimated cost
- Project complexity
- Requirements stability
- Requirement changes
- Communication level
- Project management quality
- Resource availability
- Team experience
- Technical expertise
- Testing level
- Quality factors
- Previous defects

The model is trained on historical project data and saved as a reusable artifact for prediction.

## 🔧 Tools & Technologies

| Category | Tools / Frameworks |
| --- | --- |
| Programming | Python |
| Web Framework | Django 6.1 |
| Deep Learning | TensorFlow, Keras |
| Data Processing | NumPy, Pandas |
| ML Utilities | scikit-learn, Joblib |
| Database | SQLite |
| Frontend | HTML, CSS, Bootstrap |
| IDE | VS Code, Jupyter Notebook |

## 📈 Performance Summary

| Model | Risk Accuracy | Notes |
| --- | --- | --- |
| DNN Project Risk Model | 95.29% | Deep neural network trained for 15-feature project risk classification |
| Baseline Logistic Model | Lower | Simple traditional baseline |
| Rule-based scoring | Lower | Less robust for nonlinear patterns |

## 📊 Risk Mapping

| Risk Level | Meaning |
| --- | --- |
| LOW | Healthy project with manageable risk |
| MEDIUM | Needs active monitoring and mitigation |
| HIGH | Requires immediate planning and risk control |

## 🧪 Evaluation Metrics

- Accuracy: 95.29%
- Model Type: DNN (Deep Neural Network), a machine learning model based on neural networks
- Output: Probability scores for each class (LOW, MEDIUM, HIGH) with confidence value
- Inference Speed: Fast enough for web-based use after warm-up
- Output includes important factors and recommendations

## 🌐 Web Interface Pages

- 🏠 Home: Introduction and project overview
- 🔍 Predict: Fill in project data and generate risk score
- 📊 Dashboard: View historical predictions and distribution
- 📄 Result: Show risk level, probabilities, factors, and recommendations

## 🛠️ Installation Guide

```bash
git clone <your-repository-url>
cd New folder
```

### Create virtual environment

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install django tensorflow scikit-learn joblib numpy
```

### Run the application

```powershell
python manage.py migrate
python manage.py runserver
```

Open the browser at:

```text
http://127.0.0.1:8000/
```

## ✨ Future Work

- Expand dataset with more real-world project records
- Add explainable AI for each prediction factor
- Deploy as a cloud-hosted production app
- Add project team recommendations and risk alerts
- Improve forecasting for large enterprise project portfolios

## 👥 Authors

- Developer / Researcher: Mahnoor Zaman
- Project Team: RiskNova Research Group
- Institution: NFC-IET University / Organization

## 📜 License

This project is licensed under the MIT License — see the LICENSE file for details.

## 🌟 Acknowledgements

- Project stakeholders who provided domain knowledge
- Academic and research advisors
- Open-source libraries and ML communities
- Team members who contributed to model validation and testing
