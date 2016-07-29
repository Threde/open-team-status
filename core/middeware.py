from django.conf import settings


class OpenTeamStatusSettingsMiddleware:
    def process_template_response(self, request, response):
        response.context_data['team_name'] = settings.OPEN_TEAM_STATUS_NAME
        response.context_data['team_logo'] = settings.OPEN_TEAM_STATUS_LOGO
        return response
