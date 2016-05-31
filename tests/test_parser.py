from utils import compare_lists_of_dict
from zvm_exporter.parser import Parser
from data import (page_data, spool_data, cpu_memory_data, disk_def_data,
                  disk_free_data, emptyData1, emptyData2)


def test_make_snake_case():
    p = Parser()
    assert p.make_snake_case("UPPER CASES") == "upper_cases"
    assert p.make_snake_case("lower cases") == "lower_cases"
    assert p.make_snake_case("nospaces") == "nospaces"


def test_parse_get_data():
    p = Parser()
    assert len(p.get_data(page_data)) == 11
    assert len(p.get_data(spool_data)) == 11
    assert len(p.get_data(cpu_memory_data)) == 19
    assert len(p.get_data(disk_def_data)) == 3
    assert len(p.get_data(disk_free_data)) == 4
    assert len(p.get_data(emptyData1)) == 0
    assert len(p.get_data(emptyData2)) == 0


def test_parse_page():
    p = Parser()
    parse = p.parse_page('zhcpos2', page_data)
    assert len(parse) == 1
    assert parse[0]["total_allocated"] == 93920
    assert parse[0]["available_percentage"] == 1
    assert parse[0]["total_used"] == 33106


def test_parse_spool():
    p = Parser()
    parse = p.parse_page('zhcpos2', spool_data)
    assert len(parse) == 1
    assert parse[0]["total_allocated"] == 12001
    assert parse[0]["available_percentage"] == 40
    assert parse[0]["total_used"] == 4837


def test_parse_cpu_memory():
    p = Parser()
    parse = p.parse_cpu_memory('zhcpos2', cpu_memory_data)
    assert len(parse) == 1
    assert parse[0]["cpu_count"] == 32
    assert parse[0]["cpu_average_use"] == 0.02125
    assert parse[0]["memory_in_use"] == 4219345.0
    assert parse[0]["memory_total"] == 78643200.0


def test_parse_disk():
    p = Parser()
    parse = p.parse_disk('zhcpos2', disk_def_data, disk_free_data)
    assert len(parse) == 3
    assert compare_lists_of_dict(
        parse,
        [{'space_free': 58843, 'space_total': 65520, 'status': 0,
          'volume': 'OS2P01'},
         {'space_free': 65519, 'space_total': 65520, 'status': 1,
          'volume': 'OS2P02'},
         {'space_free': 0,     'space_total': 65520, 'status': 0,
          'volume': 'OS2P03'}],
        key='volume')
