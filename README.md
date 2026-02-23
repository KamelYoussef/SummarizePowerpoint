import pytest
from unittest.mock import MagicMock, patch
# Replace 'your_module' with the actual module name
from your_module import process_pdf

class TestProcessPdf:

    @patch("your_module.is_valid_pdf")
    @patch("your_module.pymupdf4llm.to_markdown")
    @patch("your_module.ProcesseurLangChain")
    @patch("your_module.st")
    def test_process_pdf_success(self, mock_st, mock_langchain, mock_to_md, mock_is_valid):
        """Test the full successful processing pipeline."""
        # 1. Setup Mocks
        mock_is_valid.return_value = True
        mock_to_md.return_value = [
            {"metadata": {"page": 1}, "text": "Hello World"},
            {"metadata": {"page": 2}, "text": "Streamlit is great"}
        ]
        
        # Mock the LangChain processor and its return value
        mock_instance = MagicMock()
        mock_instance.traiter_chaine.return_value = "This is a summary."
        mock_langchain.return_value = mock_instance

        # 2. Execute
        config = MagicMock(execution_locale=False)
        result = process_pdf("mock_file", "test.pdf", config, "English", "Résumé long")

        # 3. Assertions
        assert result == "This is a summary."
        mock_to_md.assert_called_once_with("test.pdf", page_chunks=True)
        # Verify the text aggregation logic (Page headers should be in the text)
        args, _ = mock_instance.traiter_chaine.call_args
        assert "----- Page 1 ---" in args[0]
        assert "Hello World" in args[0]

    @patch("your_module.is_valid_pdf")
    @patch("your_module.st")
    def test_process_pdf_invalid(self, mock_st, mock_is_valid):
        """Test the 'if not is_valid_pdf' branch."""
        mock_is_valid.return_value = False
        
        result = process_pdf("bad_file", "bad.pdf", MagicMock(), "English", "Résumé court")

        assert result is None
        mock_st.error.assert_called_once_with("Veuillez sélectionner un fichier PDF valide.")

    @patch("your_module.is_valid_pdf")
    @patch("your_module.st")
    @patch("your_module.logging")
    def test_process_pdf_exception(self, mock_logging, mock_st, mock_is_valid):
        """Test the 'except Exception' block for SonarQube error coverage."""
        mock_is_valid.side_effect = Exception("System Crash")

        result = process_pdf("file", "filename", MagicMock(), "English", "Résumé long")

        assert result is None
        mock_logging.exception.assert_called_once()
        mock_st.error.assert_called_with("Une erreur est survenue lors du traitement du fichier PDF.")

    @patch("your_module.is_valid_pdf")
    @patch("your_module.rq_ia")
    @patch("your_module.ProcesseurLangChain")
    def test_process_pdf_execution_locale(self, mock_langchain, mock_rq_ia, mock_is_valid):
        """Test the conditional logic for config.execution_locale."""
        mock_is_valid.return_value = True
        # Mocking to skip the middle logic
        with patch("your_module.pymupdf4llm.to_markdown", return_value=[]):
            config = MagicMock(execution_locale=True, palier="test_palier")
            process_pdf("file", "name", config)
            
            # Verify the authentifier call inside the if block
            mock_rq_ia.authentifier.assert_called_once()
