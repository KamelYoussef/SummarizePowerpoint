import pytest
from unittest.mock import patch, MagicMock
import front_functions

# 1. Setup a fixture to handle all the common mocks
@pytest.fixture
def mock_pdf_env():
    with patch("front_functions.is_valid_pdf") as mock_valid, \
         patch("pymupdf4llm.to_markdown") as mock_to_md, \
         patch("front_functions.ProcesseurLangChain") as mock_langchain, \
         patch("streamlit.error") as mock_st_error, \
         patch("streamlit.sidebar") as mock_st_sidebar:
        
        yield {
            "valid": mock_valid,
            "to_md": mock_to_md,
            "langchain": mock_langchain,
            "st_error": mock_st_error,
            "st_sidebar": mock_st_sidebar
        }

# --- TEST CASES ---

def test_process_pdf_success(mock_pdf_env):
    """Tests the full successful flow of PDF processing."""
    # Setup Mocks
    mock_pdf_env["valid"].return_value = True
    mock_pdf_env["to_md"].return_value = [
        {"metadata": {"page": 1}, "text": "Page 1 content"},
        {"metadata": {"page": 2}, "text": "Page 2 content"}
    ]
    
    # Mock the LangChain processor instance and its method
    mock_processor_inst = MagicMock()
    mock_processor_inst.traiter_chaine.return_value = "This is a summary."
    mock_pdf_env["langchain"].return_value = mock_processor_inst

    # Execution
    mock_file = MagicMock()
    mock_config = MagicMock()
    mock_config.execution_locale = True # Triggers the local auth branch
    
    result = front_functions.process_pdf(mock_file, "Summary", "English", (1, 2), mock_config)

    # Assertions
    assert result == "This is a summary."
    mock_processor_inst.traiter_chaine.assert_called_once()
    # Check if text from both pages was concatenated
    assert "Page 1 content" in mock_processor_inst.traiter_chaine.call_args[0][0]

def test_process_pdf_invalid_file(mock_pdf_env):
    """Tests the 'if not is_valid_pdf' branch."""
    mock_pdf_env["valid"].return_value = False
    
    mock_file = MagicMock()
    mock_config = MagicMock()
    
    result = front_functions.process_pdf(mock_file, "Summary", "French", (1, 1), mock_config)
    
    assert result is None
    mock_pdf_env["st_error"].assert_called_with("Fichier PDF non valide.")

def test_process_pdf_exception_handling(mock_pdf_env):
    """Tests the 'except Exception' block for SonarQube coverage."""
    mock_pdf_env["valid"].return_value = True
    # Force an error during PDF parsing
    mock_pdf_env["to_md"].side_effect = Exception("Parsing Error")
    
    mock_file = MagicMock()
    mock_config = MagicMock()
    
    result = front_functions.process_pdf(mock_file, "Summary", "French", (1, 1), mock_config)
    
    assert result is None
    # Verify the error was reported to the user
    assert mock_pdf_env["st_error"].called
