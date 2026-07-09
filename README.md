# Simulates the deeply nested response body from your API
    mock_post.return_value.json.return_value = {"output": [{"content": [{"text": "Recette OK"}]}]}

    # 2. Run the code
    processor = ProcesseurLangChain(config=mock_config, autorisation=mock_auth)
    result = processor.llm.invoke("Donne-moi une recette")

    # 3. Quick assertions
    assert result == "Recette OK"
    mock_post.assert_called_once_with(
        "http://test-api/responses",
        json={"model": "gemma3:12b", "input": "Donne-moi une recette", "stream": False},
        headers={"Authorization": "Bearer faux-jeton"}
    )
