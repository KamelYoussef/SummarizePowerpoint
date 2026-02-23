import pytest
from unittest.mock import patch, MagicMock
# Replace 'your_module' with the actual name of your python file
from your_module import display_summary

class TestDisplaySummary:

    @patch("your_module.st")
    def test_display_summary_standard_text(self, mock_st):
        """Test with a standard string to ensure word count and HTML rendering."""
        sample_text = "This is a test summary."
        
        display_summary(sample_text)

        # Check if word count is calculated correctly (5 words)
        mock_st.write.assert_called_once_with("Résumé du PDF: (5 mots)")
        
        # Verify markdown was called with HTML containing the text
        args, kwargs = mock_st.markdown.call_args
        assert "This is a test summary." in args[0]
        assert "height:800px" in args[0]
        assert kwargs["unsafe_allow_html"] is True

    @patch("your_module.st")
    def test_display_summary_empty_string(self, mock_st):
        """Test with an empty string to check edge case behavior."""
        display_summary("")

        # Word count should be 0
        mock_st.write.assert_called_once_with("Résumé du PDF: (0 mots)")
        mock_st.markdown.assert_called_once()

    @patch("your_module.st")
    def test_display_summary_whitespace_only(self, mock_st):
        """Test with only spaces/newlines."""
        display_summary("   \n   ")

        # split() without arguments handles arbitrary whitespace, resulting in 0 words
        mock_st.write.assert_called_once_with("Résumé du PDF: (0 mots)")

    @patch("your_module.st")
    def test_display_summary_large_text(self, mock_st):
        """Test with a larger text input."""
        large_text = "word " * 100
        display_summary(large_text.strip())

        mock_st.write.assert_called_once_with("Résumé du PDF: (100 mots)")
