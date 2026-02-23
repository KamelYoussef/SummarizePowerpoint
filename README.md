import pytest
from unittest.mock import MagicMock, patch
# Replace 'your_module' with the actual name of your python file
from your_module import summary_options

class TestSummaryOptions:

    @patch("your_module.pdf_num_pages")
    @patch("your_module.st")
    def test_summary_options_multi_page(self, mock_st, mock_pdf_num):
        """Test with a multi-page PDF to ensure the slider is triggered."""
        # Setup mocks
        mock_pdf_doc = MagicMock()
        mock_pdf_num.return_value = 10
        mock_st.radio.return_value = "Résumé long"
        mock_st.selectbox.return_value = "Francais"
        mock_st.slider.return_value = (1, 5)

        # Execute
        res_type, res_lang, res_pages = summary_options(mock_pdf_doc)

        # Assertions
        assert res_type == "Résumé long"
        assert res_lang == "French"
        assert res_pages == (1, 5)
        
        # Ensure slider was called because num_pages > 1
        mock_st.slider.assert_called_once_with(
            "Selection des pages ", 1, 10, (1, 10)
        )

    @patch("your_module.pdf_num_pages")
    @patch("your_module.st")
    def test_summary_options_single_page(self, mock_st, mock_pdf_num):
        """Test with a single-page PDF to ensure the slider is skipped."""
        # Setup mocks
        mock_pdf_doc = MagicMock()
        mock_pdf_num.return_value = 1
        mock_st.radio.return_value = "Résumé court"
        mock_st.selectbox.return_value = "Anglais"

        # Execute
        res_type, res_lang, res_pages = summary_options(mock_pdf_doc)

        # Assertions
        assert res_type == "Résumé court"
        assert res_lang == "English"
        assert res_pages == (1, 1) # Default value from the code
        
        # Ensure slider was NOT called because num_pages is not > 1
        mock_st.slider.assert_not_called()

    @patch("your_module.pdf_num_pages")
    @patch("your_module.st")
    def test_summary_options_mapping(self, mock_st, mock_pdf_num):
        """Verify the language dictionary mapping is working correctly."""
        mock_pdf_num.return_value = 1
        mock_st.selectbox.return_value = "Anglais"
        
        _, res_lang, _ = summary_options(MagicMock())
        
        # Confirms "Anglais" correctly maps to "English"
        assert res_lang == "English"
