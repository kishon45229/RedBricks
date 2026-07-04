from xquik_import import parse_xquik_export


def test_parse_xquik_json_export():
    tweets = parse_xquik_export('{"tweets": [{"tweet": " Great launch "}, {"text": ""}]}')

    assert tweets == ["Great launch"]


def test_parse_xquik_jsonl_export():
    tweets = parse_xquik_export('{"full_text":"First tweet"}\n{"content":"Second tweet"}', "tweets.jsonl")

    assert tweets == ["First tweet", "Second tweet"]


def test_parse_xquik_csv_export():
    tweets = parse_xquik_export("id,body\n1,Needs faster support\n2,Works well\n", "tweets.csv")

    assert tweets == ["Needs faster support", "Works well"]


def test_reject_csv_without_text_column():
    try:
        parse_xquik_export("id,url\n1,https://example.com\n", "tweets.csv")
    except ValueError as exc:
        assert "CSV export needs" in str(exc)
    else:
        raise AssertionError("expected missing text column to fail")
