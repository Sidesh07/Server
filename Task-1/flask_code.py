from flask import Flask, jsonify
import django
from django.conf import settings
from django.urls import path
from django.http import HttpResponse

# Initialize Django settings
django.setup()

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.setup_django()

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return jsonify(message="Welcome to the Flask server!")

    def setup_django(self):
        # Django-specific URL routing
        def django_home(request):
            return HttpResponse("Welcome to the Django server!")

        # Django URLs setup
        django_urls = [
            path('django/', django_home),
        ]

        settings.configure(
            ROOT_URLCONF=django_urls,
        )

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    server = Server()
    server.run()
