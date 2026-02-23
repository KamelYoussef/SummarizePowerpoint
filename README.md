import pytest
from unittest.mock import MagicMock, patch
# Replace 'your_module' with the actual name of your python file
from your_module import pdf_num_pages

class TestPdfNumPages:

    @patch("your_module.fitz.open")
    def test_pdf_num_pages_success(self, mock_fitz_open):
        """Test successful page count retrieval and stream reset."""
        # 1. Mock the Streamlit UploadedFile
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.read.return_value = b"fake pdf content"
        
        # 2. Mock the fitz context manager and its page_count attribute
        mock_pdf_doc = MagicMock()
        mock_pdf_doc.page_count = 5
        # This handles the 'with fitz.open(...) as file:' pattern
        mock_fitz_open.return_value.__enter__.return_value = mock_pdf_doc

        # Execute
        result = pdf_num_pages(mock_uploaded_file)

        # 3. Assertions
        assert result == 5
        # Verify fitz.open was called with correct byte data
        mock_fitz_open.assert_called_once_with("pdf", b"fake pdf content")
        # Verify doc.seek(0) was called to reset the stream for future use
        mock_uploaded_file.seek.assert_called_once_with(0)

    @patch("your_module.fitz.open")
    def test_pdf_num_pages_empty_file(self, mock_fitz_open):
        """Test behavior when the PDF has 0 pages or is empty."""
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.read.return_value = b""
        
        mock_pdf_doc = MagicMock()
        mock_pdf_doc.page_count = 0
        mock_fitz_open.return_value.__enter__.return_value = mock_pdf_doc

        result = pdf_num_pages(mock_uploaded_file)

        assert result == 0
        mock_uploaded_file.seek.assert_called_once_with(0)

    @patch("your_module.fitz.open")
    def test_pdf_num_pages_exception_handling(self, mock_fitz_open):
        """Ensure seek(0) is called even if fitz raises an error (if applicable)."""
        # Note: In your current code, if fitz.open fails, it won't hit seek(0).
        # This test checks if the function crashes as expected on corrupt data.
        mock_uploaded_file = MagicMock()
        mock_fitz_open.side_effect = Exception("Corrupt PDF")

        with pytest.raises(Exception, match="Corrupt PDF"):
            pdf_num_pages(mock_uploaded_file)
