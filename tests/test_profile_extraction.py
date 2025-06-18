import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrape_to_sql import extract_profile_data_from_html

SAMPLES = [
    'sample_profile_Bell-Angela.html',
    'sample_profile_Bergman-Beth.html',
]

@pytest.mark.parametrize('filename', SAMPLES)
def test_profile_extraction(filename):
    path = os.path.join(os.path.dirname(__file__), '..', filename)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    data = extract_profile_data_from_html(html)
    # At least one of these fields should be present and non-empty
    assert any(data.get(field) for field in ['company', 'job_title', 'email', 'phone']), f"No profile data extracted from {filename}"
    # Email, if present, should look like an email
    if data.get('email'):
        assert '@' in data['email'], f"Email field not valid in {filename}: {data['email']}" 