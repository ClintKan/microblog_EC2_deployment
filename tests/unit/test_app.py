import sys
import os
import unittest

# Appending the directory path where routes.py is located
sys.path.append(os.path.abspath("/home/ubuntu/microblog_EC2_deployment/app/main/routes.py"))

# importing routes
from app.main.routes import explore
from app.main import routes

def test_explore_page():
    response = routes.test_client().get('/explore')
    assertEqual(response.status_code, 200)  # OK

if __name__ == '__main__':
    unittest.main()
