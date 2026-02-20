import pytest
from unittest.mock import MagicMock
import front_functions  # Assuming this is the filename

@pytest.fixture
def mock_dependencies(mocker):
    """Fixture to mock all external libraries and classes."""
    # Mocking Streamlit components
    mocker.patch("streamlit.error")
    
    # Mocking PDF processing library
    mock_to_markdown = mocker.patch("pymupdf4llm.to_markdown")
    
    # Mocking internal validation
    mock_valid = mocker.patch("front_functions.is_valid_pdf")
    
    # Mocking dot-env loading to avoid file system errors in SonarQube
    mocker.patch("front_functions.load_dotenv")
    
    # Mocking the Backend Processor
    mock_processor_cls = mocker.patch("front_functions.ProcesseurLangChain")
    mock_processor_instance = mock_processor_cls.return_value
    mock_processor_instance.traiter_chaine.return_value = "Résumé généré avec succès"
    
    # Mocking Authentication
    mocker.patch("front_functions.rq_ia.authentifier")
    
    return {
        "to_markdown": mock_to_markdown,
        "is_valid": mock_valid,
        "processor": mock_processor_instance
    }

def test_process_pdf_success(mock_dependencies, mocker):
    """Tests the full successful path of the function."""
    # Setup
    mock_dependencies["is_valid"].return_value = True
    mock_dependencies["to_markdown"].return_value = [
        {"metadata": {"page": 1}, "text": "Contenu page 1"},
        {"metadata": {"page": 2}, "text": "Contenu page 2"}
    ]
    
    config = MagicMock()
    config.execution_locale = True
    config.palier = "test_palier"
    
    # Act
    result = front_functions.process_pdf(
        file="mock_file", 
        _pdf_filename="test.pdf", 
        config=config
    )
    
    # Assert
    assert result == "Résumé généré avec succès"
    assert mock_dependencies["processor"].traiter_chaine.called

def test_process_pdf_invalid_file(mock_dependencies):
    """Tests the 'if not is_valid_pdf' branch to ensure coverage."""
    # Setup
    mock_dependencies["is_valid"].return_value = False
    
    # Act
    result = front_functions.process_pdf("bad_file", "bad.pdf", MagicMock())
    
    # Assert
    import streamlit as st
    assert result is None
    st.error.assert_called_with("Veuillez sélectionner un fichier PDF valide.")

def test_process_pdf_exception_handling(mock_dependencies):
    """Tests the 'except Exception' block for full SonarQube coverage."""
    # Setup: Force an error during PDF processing
    mock_dependencies["is_valid"].return_value = True
    mock_dependencies["to_markdown"].side_effect = Exception("Crash test")
    
    # Act
    result = front_functions.process_pdf("file", "file.pdf", MagicMock())
    
    # Assert
    assert result is None
    import streamlit as st
    st.error.assert_called()
