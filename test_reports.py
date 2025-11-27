import pytest
import os
import tempfile

from main import stream_employee_data, calculate_average_performance_streaming

def create_test_csv(content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        return f.name

def test_stream_employee_data_basic():
    content = """name,position,performance
John,Dev,4.5
Jane,Design,4.8
"""
    filename = create_test_csv(content)
    try:
        rows = list(stream_employee_data([filename]))
        assert len(rows) == 2
        assert rows[0]["name"] == "John"
        assert rows[1]["position"] == "Design"
    finally:
        os.unlink(filename)

def test_stream_employee_data_missing_file():
    rows = list(stream_employee_data(["no_file.csv"]))
    assert rows == []

def test_stream_employee_data_unicode_error():
    bad_bytes = b'\xff\xfe\xfa\xfb'
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(bad_bytes)
        filename = f.name

    try:
        row = list(stream_employee_data([filename]))
        assert row == []
    finally:
        os.unlink(filename)

def test_average_streaming():
    content = """position,performance
Dev,4.5
Dev,5.5
Design,4.0
"""
    filename = create_test_csv(content)
    try:
        result = calculate_average_performance_streaming([filename])
        assert len(result) == 2
        dev = next(r for r in result if r[0] == "Dev")
        design = next(r for r in result if r[0] == "Design")
        assert dev[1] == 5.0
        assert design[1] == 4.0
    finally:
        os.unlink(filename)

def test_invalid_performance_handled():
    content = """position,performance
Dev,4.5
Dev,invalid
"""
    filename = create_test_csv(content)
    try:
        result = calculate_average_performance_streaming([filename])
        assert len(result) == 1
        assert result[0][0] == "Dev"
        assert result[0][1] == 4.5
    finally:
        os.unlink(filename)

def test_header_only_file():
    content = "name,position,performance"
    filename = create_test_csv(content)
    try:
        rows = list(stream_employee_data([filename]))
        assert rows == []
    finally:
        os.unlink(filename)