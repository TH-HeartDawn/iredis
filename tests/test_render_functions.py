from iredis import renders


def strip_formatted_text(formatted_text):
    return "".join(text[1] for text in formatted_text)


def test_render_list_index():
    from iredis.config import config

    config.raw = False
    raw = ["hello", "world", "foo"]
    out = renders.render_list([item.encode() for item in raw], raw)
    out = strip_formatted_text(out)
    assert isinstance(out, str)
    assert "3)" in out
    assert "1)" in out
    assert "4)" not in out


def test_render_list_index_const_width():
    from iredis.config import config

    config.raw = False
    raw = ["hello"] * 100
    out = renders.render_list([item.encode() for item in raw], raw)
    out = strip_formatted_text(out)
    assert isinstance(out, str)
    assert "  1)" in out
    assert "\n100)" in out

    raw = ["hello"] * 1000
    out = renders.render_list([item.encode() for item in raw], raw)
    out = strip_formatted_text(out)
    assert "   1)" in out
    assert "\n 999)" in out
    assert "\n1000)" in out

    raw = ["hello"] * 10
    out = renders.render_list([item.encode() for item in raw], raw)
    out = strip_formatted_text(out)
    assert " 1)" in out
    assert "\n 9)" in out
    assert "\n10)" in out


def test_render_list_while_config_raw():
    from iredis.config import config

    config.raw = True
    raw = ["hello", "world", "foo"]
    out = renders.render_list([item.encode() for item in raw], raw)
    assert b"hello\nworld\nfoo" == out


def test_ensure_str_bytes():
    assert renders._ensure_str(b"hello world") == r"hello world"
    assert renders._ensure_str(b"hello'world") == r"hello'world"
    assert renders._ensure_str("你好".encode()) == r"\xe4\xbd\xa0\xe5\xa5\xbd"


def test_double_quotes():
    assert renders._double_quotes('hello"world') == r'"hello\"world"'
    assert renders._double_quotes('"hello\\world"') == '"\\"hello\\world\\""'

    assert renders._double_quotes("'") == '"\'"'
    assert renders._double_quotes("\\") == '"\\"'
    assert renders._double_quotes('"') == '"\\""'
