import sys
import os
import unittest
import requests

# Appending the directory path where routes.py is located
sys.path.append(os.path.abspath("/home/ubuntu/microblog_EC2_deployment/app/main/routes.py"))

# importing routes
from app.main.routes import explore

def test_explore_page():
    response = request.get('/explore')
    assertEqual(response.status_code, 200)  # OK

if __name__ == '__main__':
    unittest.main()
