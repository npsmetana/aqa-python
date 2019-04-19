from files import *


def test_files():
    in_file = "./samples/xml/test_data.xml"
    out_file = "./samples/json/updated_test_data.json"

    print("\n\n=== Start 'test_file' test ===")

    print("\n\nStart 'test_file' test")

    print("\n\nClean-up")
    clean_up(out_file)

    print("\n\nCheck if file source XML file exists\nFile: ", in_file)
    result = is_file_exist(in_file)
    if result:
        print("\nSource XML file", in_file, "found")
    else:
        print("\nSource XML file", in_file, "absent")
    assert result

    print("\n\nCheck if file source XML structure is correct")
    result = check_xml_structure(in_file)
    if result:
        print("\nXML file structure is correct")
    else:
        print("\nXML file structure is broken")
    assert result

    print("\n\nImport XML-file content and save it to data structure")
    data = import_xml_to_data(in_file)

    print("\n\nUpdate imported data structure")
    data_upd = replace_data(data)

    print("\n\nCheck if update is correct")
    result = is_everything_replaced(data_upd)
    if result:
        print("\nUpdate passed")
    else:
        print("\nUpdate failed")
    assert result

    print("\n\nSave data structure to JSON file\nFile: ", out_file)
    save_data_to_json_file(out_file, data_upd)

    print("\n\nCheck if JSON file was created")
    result = is_file_exist(out_file)
    if result:
        print("\nTarget JSON file", out_file, "found")
    else:
        print("\nTarget JSON file", out_file, "absent")
    assert result

    print("\n\nCheck data structure was saved correctly into JSON file")
    result = is_data_saved_correctly(out_file, data_upd)
    if result:
        print("\nData saved correctly in JSON file", out_file)
    else:
        print("\nData saved incorrectly in JSON file", out_file)
    assert result

    print("\n\n=== End 'test_file' test ===")
