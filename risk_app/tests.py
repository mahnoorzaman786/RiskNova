from django.test import TestCase


class PredictFormAjaxFlowTests(TestCase):
    def test_ajax_prediction_returns_result_html(self):
        data = {
            'project_name': 'Demo Project',
            'project_size': 'medium',
            'team_size': '12',
            'project_duration': '8',
            'estimated_cost': '200000',
            'project_complexity': 'high',
            'requirements_stability': 'moderate',
            'requirement_changes': '20',
            'communication_level': 'good',
            'project_management_quality': 'average',
            'resource_availability': 'adequate',
            'team_experience': 'good',
            'technical_expertise': 'good',
            'testing_level': 'moderate',
            'quality_factors': 'good',
            'previous_defects': '10',
        }

        response = self.client.post(
            '/predict/',
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Risk Level')
        self.assertContains(response, 'LOW')
