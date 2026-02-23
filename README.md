import pytest
from unittest.mock import MagicMock, patch, mock_open
# Replace 'your_module' with the actual module name
from your_module import init_streamlit

class TestInitStreamlit:

    @patch("your_module.st")
    def test_init_streamlit_unauthorized(self, mock_st):
        """Test that execution stops if the user is not authorized."""
        # Setup mock authorization object
        mock_auth = MagicMock()
        mock_auth.est_autorise.return_value = False
        
        # Streamlit's st.stop() usually raises an exception to halt the script
        mock_st.stop.side_effect = Exception("Streamlit Stopped")

        with pytest.raises(Exception, match="Streamlit Stopped"):
            init_streamlit(mock_auth)

        # Verify error message was shown
        mock_st.error.assert_called_once_with(
            body="Vous n'êtes pas autorisé à accéder cette page.", 
            icon="🚨"
        )
        # Ensure layout columns were never created
        mock_st.columns.assert_not_called()

    @patch("your_module.st")
    def test_init_streamlit_authorized_success(self, mock_st):
        """Test full initialization when user is authorized."""
        # 1. Mock Authorization
        mock_auth = MagicMock()
        mock_auth.est_autorise.return_value = True
        
        # 2. Mock CSS file reading
        fake_css = "body { background-color: red; }"
        
        # 3. Mock columns return values
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        # Use mock_open to simulate the external CSS file
        with patch("builtins.open", mock_open(read_data=fake_css)):
            c1, c2 = init_streamlit(mock_auth)

        # Assertions
        mock_st.set_page_config.assert_called_once_with(
            page_title="Résumé PDF", page_icon=":books:", layout="wide"
        )
        mock_st.markdown.assert_called_with(
            f"<style>{fake_css}</style>", unsafe_allow_html=True
        )
        assert c1 == mock_col1
        assert c2 == mock_col2
