import pytest
from unittest.mock import MagicMock

def test_summary_options_multi_page(mocker):
    # 1. Mock the PDF utility to return more than 1 page
    mocker.patch("front_functions.pdf_num_pages", return_value=5)
    
    # 2. Mock Streamlit widgets to return specific user choices
    mocker.patch("streamlit.radio", return_value="Résumé court")
    mocker.patch("streamlit.selectbox", return_value="Anglais")
    # This mock ensures the slider branch is executed and covered
    mocker.patch("streamlit.slider", return_value=(1, 3))
    
    # 3. Create a dummy file object
    mock_pdf = MagicMock()
    
    # 4. Call the function
    from front_functions import summary_options
    types, language, pages = summary_options(mock_pdf)
    
    # 5. Assertions
    assert types == "Résumé court"
    assert language == "English"  # Because options["Anglais"] == "English"
    assert pages == (1, 3)

def test_summary_options_single_page(mocker):
    mocker.patch("front_functions.pdf_num_pages", return_value=1)
    mocker.patch("streamlit.radio", return_value="Résumé long")
    mocker.patch("streamlit.selectbox", return_value="Francais")
    
    mock_pdf = MagicMock()
    types, language, pages = summary_options(mock_pdf)
    
    assert language == "French"
    assert pages == (1, 1) # Default value when slider isn't called
