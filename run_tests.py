#!/usr/bin/env python
"""
Test runner script for DormitoriesPlus project.

This script runs all tests with proper Django configuration.
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests():
    """Run the test suite."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DormitoriesPlus_project.test_settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Discover and run tests
    failures = test_runner.run_tests([
        'DormitoriesPlus.tests',
    ])
    
    return failures

if __name__ == '__main__':
    failures = run_tests()
    sys.exit(bool(failures)) 