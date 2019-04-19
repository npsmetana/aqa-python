from files import *


def test_files():
    in_file = "./samples/xml/test_data.xml"
    out_file = "./samples/json/updated_test_data.json"

    clean_up(out_file)

    assert is_file_exist(in_file)

    assert check_xml_structure(in_file)

    data = import_xml_to_data(in_file)

    data_upd = replace_data(data)

    assert is_everything_replaced(data_upd)

    save_data_to_json_file(out_file, data_upd)

    assert is_file_exist(out_file)

    assert is_data_saved_correctly(out_file, data_upd)
