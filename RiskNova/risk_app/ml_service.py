from __future__ import annotations

from pathlib import Path

import json
import joblib
import numpy as np

try:
    import keras
except Exception:
    keras = None

from .models import ProjectRiskPrediction


# ================================================================
# PATHS
# ================================================================

BASE_DIR = Path(__file__).resolve().parent

# ------------------------------------------------
# Your actual model location
# ------------------------------------------------
ROOT_MODEL_DIR = (
    BASE_DIR
    / "models"
    / "trained_15_feature_model"
)

MODEL_PATH = ROOT_MODEL_DIR / "DNN_Project_Risk_Model.keras"
SCALER_PATH = ROOT_MODEL_DIR / "project_risk_scaler.joblib"
FEATURE_NAMES_PATH = ROOT_MODEL_DIR / "feature_names.json"
LABELS_PATH = ROOT_MODEL_DIR / "labels.json"


# ================================================================
# 15 FEATURES
# ================================================================

FEATURE_NAMES = [
    "project_size",
    "team_size",
    "project_duration",
    "estimated_cost",
    "project_complexity",
    "requirements_stability",
    "requirement_changes",
    "communication_level",
    "project_management_quality",
    "resource_availability",
    "team_experience",
    "technical_expertise",
    "testing_level",
    "quality_factors",
    "previous_defects",
]


# ================================================================
# LABELS
# ================================================================

LABELS = [
    "LOW",
    "MEDIUM",
    "HIGH",
]


# ================================================================
# CATEGORY MAPPINGS
# ================================================================

SIZE_MAP = {
    "small": 1,
    "medium": 2,
    "large": 3,
    "enterprise": 4,
}


COMPLEXITY_MAP = {
    "low": 1,
    "moderate": 2,
    "high": 3,
    "critical": 4,
}


STABILITY_MAP = {
    "unstable": 1,
    "moderate": 2,
    "stable": 3,
    "highly_stable": 4,
}


COMMUNICATION_MAP = {
    "poor": 1,
    "average": 2,
    "good": 3,
    "very_good": 4,
    "excellent": 5,
}


PM_MAP = {
    "poor": 1,
    "average": 2,
    "good": 3,
    "very_good": 4,
    "excellent": 5,
}


RESOURCE_MAP = {
    "scarce": 1,
    "limited": 2,
    "adequate": 3,
    "strong": 4,
    "abundant": 5,
}


EXPERIENCE_MAP = {
    "low": 1,
    "moderate": 2,
    "good": 3,
    "high": 4,
    "expert": 5,
}


EXPERTISE_MAP = {
    "low": 1,
    "moderate": 2,
    "good": 3,
    "high": 4,
    "expert": 5,
}


TESTING_MAP = {
    "minimal": 1,
    "basic": 2,
    "moderate": 3,
    "strong": 4,
    "comprehensive": 5,
}


QUALITY_MAP = {
    "poor": 1,
    "average": 2,
    "good": 3,
    "very_good": 4,
    "excellent": 5,
}


# ================================================================
# DISPLAY LABELS
# ================================================================

FEATURE_LABELS = {
    "project_size": "Project Size",
    "team_size": "Team Size",
    "project_duration": "Project Duration",
    "estimated_cost": "Estimated Cost",
    "project_complexity": "Project Complexity",
    "requirements_stability": "Requirements Stability",
    "requirement_changes": "Requirement Changes",
    "communication_level": "Communication Level",
    "project_management_quality": "Project Management Quality",
    "resource_availability": "Resource Availability",
    "team_experience": "Team Experience",
    "technical_expertise": "Technical Expertise",
    "testing_level": "Testing Level",
    "quality_factors": "Quality Factors",
    "previous_defects": "Previous Defects",
}


# ================================================================
# CACHED MODEL
# ================================================================

_MODEL = None
_SCALER = None


# ================================================================
# LOAD MODEL
# ================================================================

def load_model():
    """
    Load the trained 15-feature DNN model and scaler.

    The model is loaded only once and then cached in memory.
    This prevents loading the Keras model on every prediction.
    """

    global _MODEL
    global _SCALER

    # ------------------------------------------------------------
    # Return cached model
    # ------------------------------------------------------------

    if _MODEL is not None and _SCALER is not None:
        return _MODEL, _SCALER

    print("\n" + "=" * 70)
    print("LOADING 15-FEATURE PROJECT RISK MODEL")
    print("=" * 70)

    print("\nModel path:")
    print(MODEL_PATH)

    print("\nScaler path:")
    print(SCALER_PATH)

    # ------------------------------------------------------------
    # Check model
    # ------------------------------------------------------------

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"\nDNN model was not found:\n{MODEL_PATH}"
        )

    # ------------------------------------------------------------
    # Check scaler
    # ------------------------------------------------------------

    if not SCALER_PATH.exists():

        raise FileNotFoundError(
            f"\nScaler was not found:\n{SCALER_PATH}"
        )

    # ------------------------------------------------------------
    # Check Keras
    # ------------------------------------------------------------

    if keras is None:

        raise ImportError(
            "Keras could not be imported. "
            "Please use the environment where the model was trained."
        )

    # ------------------------------------------------------------
    # Load Keras model
    # ------------------------------------------------------------

    print("\nLoading DNN model...")

    _MODEL = keras.models.load_model(
        MODEL_PATH,
        compile=False
    )

    print("MODEL LOADED SUCCESSFULLY")

    print(
        "Input shape :",
        _MODEL.input_shape
    )

    print(
        "Output shape:",
        _MODEL.output_shape
    )

    # ------------------------------------------------------------
    # Verify model input
    # ------------------------------------------------------------

    if _MODEL.input_shape[-1] != 15:

        raise ValueError(
            f"Model expects {_MODEL.input_shape[-1]} features, "
            f"but application expects 15."
        )

    # ------------------------------------------------------------
    # Load scaler
    # ------------------------------------------------------------

    print("\nLoading scaler...")

    _SCALER = joblib.load(
        SCALER_PATH
    )

    print("SCALER LOADED SUCCESSFULLY")

    # ------------------------------------------------------------
    # Verify scaler
    # ------------------------------------------------------------

    if not hasattr(_SCALER, "transform"):

        raise ValueError(
            "Loaded scaler does not have a transform() method."
        )

    if hasattr(_SCALER, "n_features_in_"):

        if _SCALER.n_features_in_ != 15:

            raise ValueError(
                f"Scaler expects {_SCALER.n_features_in_} "
                f"features, but application provides 15."
            )

    return _MODEL, _SCALER


# ================================================================
# CONVERT DATA TO 15 FEATURES
# ================================================================

def _to_feature_vector(data):
    """
    Convert Django form data into exactly 15 numerical features.

    IMPORTANT:
    The order must be identical to the order used during training.
    """

    def clean(value):
        return str(value or "").strip().lower()

    # ------------------------------------------------------------
    # Create vector
    # ------------------------------------------------------------

    vector = [

        # 1. Project Size
        SIZE_MAP.get(
            clean(data.get("project_size")),
            2
        ),

        # 2. Team Size
        float(
            data.get("team_size", 0) or 0
        ),

        # 3. Project Duration
        float(
            data.get("project_duration", 0) or 0
        ),

        # 4. Estimated Cost
        float(
            data.get("estimated_cost", 0) or 0
        ),

        # 5. Project Complexity
        COMPLEXITY_MAP.get(
            clean(data.get("project_complexity")),
            2
        ),

        # 6. Requirements Stability
        STABILITY_MAP.get(
            clean(data.get("requirements_stability")),
            2
        ),

        # 7. Requirement Changes
        float(
            data.get("requirement_changes", 0) or 0
        ),

        # 8. Communication Level
        COMMUNICATION_MAP.get(
            clean(data.get("communication_level")),
            3
        ),

        # 9. Project Management Quality
        PM_MAP.get(
            clean(data.get("project_management_quality")),
            3
        ),

        # 10. Resource Availability
        RESOURCE_MAP.get(
            clean(data.get("resource_availability")),
            3
        ),

        # 11. Team Experience
        EXPERIENCE_MAP.get(
            clean(data.get("team_experience")),
            3
        ),

        # 12. Technical Expertise
        EXPERTISE_MAP.get(
            clean(data.get("technical_expertise")),
            3
        ),

        # 13. Testing Level
        TESTING_MAP.get(
            clean(data.get("testing_level")),
            3
        ),

        # 14. Quality Factors
        QUALITY_MAP.get(
            clean(data.get("quality_factors")),
            3
        ),

        # 15. Previous Defects
        float(
            data.get("previous_defects", 0) or 0
        ),
    ]

    # ------------------------------------------------------------
    # Convert to numpy
    # ------------------------------------------------------------

    vector = np.asarray(
        vector,
        dtype=np.float32
    )

    # ------------------------------------------------------------
    # Verify 15 features
    # ------------------------------------------------------------

    if vector.shape[0] != 15:

        raise ValueError(
            f"Expected 15 features, "
            f"but received {vector.shape[0]}"
        )

    # ------------------------------------------------------------
    # Return shape (1, 15)
    # ------------------------------------------------------------

    return vector.reshape(1, 15)


# ================================================================
# TOP CONTRIBUTING FACTORS
# ================================================================

def get_top_factors(cleaned_data):

    scores = {}

    try:

        def clean(value):
            return str(value or "").strip().lower()

        # --------------------------------------------------------
        # Project Complexity
        # --------------------------------------------------------

        scores["Project Complexity"] = (
            COMPLEXITY_MAP.get(
                clean(
                    cleaned_data.get(
                        "project_complexity"
                    )
                ),
                2
            )
        )

        # --------------------------------------------------------
        # Requirements Stability
        # --------------------------------------------------------

        stability = STABILITY_MAP.get(
            clean(
                cleaned_data.get(
                    "requirements_stability"
                )
            ),
            2
        )

        scores["Requirements Stability"] = (
            5 - stability
        )

        # --------------------------------------------------------
        # Requirement Changes
        # --------------------------------------------------------

        scores["Requirement Changes"] = float(
            cleaned_data.get(
                "requirement_changes",
                0
            ) or 0
        )

        # --------------------------------------------------------
        # Communication
        # --------------------------------------------------------

        communication = COMMUNICATION_MAP.get(
            clean(
                cleaned_data.get(
                    "communication_level"
                )
            ),
            3
        )

        scores["Communication Level"] = (
            6 - communication
        )

        # --------------------------------------------------------
        # Project Management
        # --------------------------------------------------------

        pm = PM_MAP.get(
            clean(
                cleaned_data.get(
                    "project_management_quality"
                )
            ),
            3
        )

        scores["Project Management Quality"] = (
            6 - pm
        )

        # --------------------------------------------------------
        # Resources
        # --------------------------------------------------------

        resources = RESOURCE_MAP.get(
            clean(
                cleaned_data.get(
                    "resource_availability"
                )
            ),
            3
        )

        scores["Resource Availability"] = (
            6 - resources
        )

        # --------------------------------------------------------
        # Team Experience
        # --------------------------------------------------------

        experience = EXPERIENCE_MAP.get(
            clean(
                cleaned_data.get(
                    "team_experience"
                )
            ),
            3
        )

        scores["Team Experience"] = (
            6 - experience
        )

        # --------------------------------------------------------
        # Technical Expertise
        # --------------------------------------------------------

        expertise = EXPERTISE_MAP.get(
            clean(
                cleaned_data.get(
                    "technical_expertise"
                )
            ),
            3
        )

        scores["Technical Expertise"] = (
            6 - expertise
        )

        # --------------------------------------------------------
        # Testing
        # --------------------------------------------------------

        testing = TESTING_MAP.get(
            clean(
                cleaned_data.get(
                    "testing_level"
                )
            ),
            3
        )

        scores["Testing Level"] = (
            6 - testing
        )

        # --------------------------------------------------------
        # Quality
        # --------------------------------------------------------

        quality = QUALITY_MAP.get(
            clean(
                cleaned_data.get(
                    "quality_factors"
                )
            ),
            3
        )

        scores["Quality Factors"] = (
            6 - quality
        )

        # --------------------------------------------------------
        # Previous Defects
        # --------------------------------------------------------

        scores["Previous Defects"] = float(
            cleaned_data.get(
                "previous_defects",
                0
            ) or 0
        )

        # --------------------------------------------------------
        # Sort highest risk contribution first
        # --------------------------------------------------------

        ranking = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            name
            for name, value
            in ranking[:3]
        ]

    except Exception:

        return [
            "Project Complexity",
            "Requirements Stability",
            "Technical Expertise",
        ]


# ================================================================
# RECOMMENDATIONS
# ================================================================

def get_recommendations(risk_label):

    if risk_label == "HIGH":

        return [
            "Review project requirements",
            "Increase resource allocation",
            "Improve communication",
            "Increase testing activities",
            "Monitor project schedule",
            "Review estimated project cost",
        ]

    elif risk_label == "MEDIUM":

        return [
            "Refine scope and requirements",
            "Strengthen team coordination",
            "Increase milestone reviews",
            "Improve quality assurance coverage",
            "Rebalance allocation of effort",
            "Validate cost assumptions",
        ]

    else:

        return [
            "Maintain current delivery discipline",
            "Continue periodic risk reviews",
            "Monitor scope changes",
            "Preserve communication cadence",
            "Track quality thresholds",
            "Keep resource planning visible",
        ]


# ================================================================
# PREDICT RISK
# ================================================================

def predict_risk(raw_data):
    """
    Run project risk prediction.

    Returns:
        dict containing:
            risk_label
            risk_category
            risk_level
            risk_probability
            confidence
            main_contributing_factors
            recommendations
            probability_by_class
    """

    print("\n" + "=" * 70)
    print("PROJECT RISK PREDICTION")
    print("=" * 70)

    # ------------------------------------------------------------
    # Load model
    # ------------------------------------------------------------

    model, scaler = load_model()

    # ------------------------------------------------------------
    # Create feature vector
    # ------------------------------------------------------------

    feature_vector = _to_feature_vector(
        raw_data
    )

    print("\nFeature vector:")
    print(feature_vector)

    print(
        "Feature shape:",
        feature_vector.shape
    )

    # ------------------------------------------------------------
    # Scale features
    # ------------------------------------------------------------

    scaled_features = scaler.transform(
        feature_vector
    )

    print("\nScaled features:")
    print(scaled_features)

    # ------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------

    print("\nRunning DNN prediction...")

    raw_prediction = model.predict(
        scaled_features,
        verbose=0
    )

    # ------------------------------------------------------------
    # Convert prediction
    # ------------------------------------------------------------

    probabilities = np.asarray(
        raw_prediction[0],
        dtype=np.float64
    ).flatten()

    print(
        "\nRaw model output:",
        probabilities
    )

    # ------------------------------------------------------------
    # Verify 3 outputs
    # ------------------------------------------------------------

    if len(probabilities) != 3:

        raise ValueError(
            f"Expected 3 class probabilities, "
            f"but model returned {len(probabilities)}."
        )

    # ------------------------------------------------------------
    # Normalize probabilities
    # ------------------------------------------------------------

    probability_sum = probabilities.sum()

    if probability_sum <= 0:

        raise ValueError(
            "Model returned invalid probabilities."
        )

    probabilities = (
        probabilities / probability_sum
    )

    # ------------------------------------------------------------
    # Predicted class
    # ------------------------------------------------------------

    predicted_index = int(
        np.argmax(probabilities)
    )

    risk_label = LABELS[
        predicted_index
    ]

    # ------------------------------------------------------------
    # Confidence
    # ------------------------------------------------------------

    confidence = float(
        probabilities[predicted_index] * 100
    )

    risk_probability = confidence

    # ------------------------------------------------------------
    # Top factors
    # ------------------------------------------------------------

    factors = get_top_factors(
        raw_data
    )

    # ------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------

    recommendations = get_recommendations(
        risk_label
    )

    # ------------------------------------------------------------
    # Probability dictionary
    # ------------------------------------------------------------

    probability_by_class = {

        label: round(
            float(probability) * 100,
            2
        )

        for label, probability

        in zip(
            LABELS,
            probabilities
        )
    }

    # ------------------------------------------------------------
    # Print result
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("PREDICTION RESULT")
    print("=" * 70)

    print(
        f"\nPredicted Risk : {risk_label}"
    )

    print(
        f"Confidence     : {confidence:.2f}%"
    )

    print("\nProbability by class:")

    for label, probability in (
        probability_by_class.items()
    ):

        print(
            f"{label:<8}: "
            f"{probability:.2f}%"
        )

    print("\nMain contributing factors:")

    for factor in factors:

        print(
            f"- {factor}"
        )

    print("\nRecommendations:")

    for recommendation in recommendations:

        print(
            f"- {recommendation}"
        )

    print("\n" + "=" * 70)

    # ------------------------------------------------------------
    # Return result
    # ------------------------------------------------------------

    return {

        "risk_label": risk_label,

        "risk_category": risk_label,

        "risk_level": risk_label,

        "risk_probability": risk_probability,

        "confidence": confidence,

        "main_contributing_factors": factors,

        "recommendations": recommendations,

        "probability_by_class": (
            probability_by_class
        ),
    }


# ================================================================
# SAVE PREDICTION RECORD
# ================================================================

def save_prediction_record(
    form_data,
    prediction_result
):
    """
    Save prediction and submitted project information
    into the Django database.
    """

    prediction = ProjectRiskPrediction.objects.create(

        project_name=form_data.get(
            "project_name",
            "Unnamed Project"
        ),

        project_size=form_data.get(
            "project_size",
            ""
        ),

        team_size=form_data.get(
            "team_size",
            0
        ),

        project_duration=form_data.get(
            "project_duration",
            0
        ),

        estimated_cost=form_data.get(
            "estimated_cost",
            0
        ),

        project_complexity=form_data.get(
            "project_complexity",
            ""
        ),

        requirements_stability=form_data.get(
            "requirements_stability",
            ""
        ),

        requirement_changes=form_data.get(
            "requirement_changes",
            0
        ),

        communication_level=form_data.get(
            "communication_level",
            ""
        ),

        project_management_quality=form_data.get(
            "project_management_quality",
            ""
        ),

        resource_availability=form_data.get(
            "resource_availability",
            ""
        ),

        team_experience=form_data.get(
            "team_experience",
            ""
        ),

        technical_expertise=form_data.get(
            "technical_expertise",
            ""
        ),

        testing_level=form_data.get(
            "testing_level",
            ""
        ),

        quality_factors=form_data.get(
            "quality_factors",
            ""
        ),

        previous_defects=form_data.get(
            "previous_defects",
            0
        ),

        risk_level=prediction_result[
            "risk_level"
        ],

        risk_category=prediction_result[
            "risk_category"
        ],

        risk_probability=prediction_result[
            "risk_probability"
        ],

        confidence=prediction_result[
            "confidence"
        ],

        main_contributing_factors=prediction_result[
            "main_contributing_factors"
        ],

        recommendations=prediction_result[
            "recommendations"
        ],
    )

    return prediction