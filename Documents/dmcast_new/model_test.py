import model
import sys

def run_test_without_output(test_num, els):
    save_stdout = sys.stdout
    sys.stdout = open('trash', 'w')
    m = model.daily_weather(0, 0, True, test_num, els)
    sys.stdout = save_stdout

    return m

def test_temp():
    m = run_test_without_output(2, 0)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) == 0 and len(secondary_list) == 0
    print("passed test_temp.")

def test_prcp():
    m = run_test_without_output(3, 0)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) == 0 and len(secondary_list) == 0
    print("passed test_prcp.")

def test_els():
    m = run_test_without_output(4, 13)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) == 0 and len(secondary_list) == 0
    print("passed test_els.")


def test_temp_and_prcp():
    m = run_test_without_output(5, 0)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) == 0 and len(secondary_list) == 0
    print("passed test_temp_and_prcp.")

def test_temp_and_els():
    m = run_test_without_output(6, 13)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) == 0 and len(secondary_list) == 0
    print("passed test_temp_and_els.")

def test_prcp_and_els():
    m = run_test_without_output(7, 13)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) == 0 and len(secondary_list) == 0
    print("passed test_prcp_and_els.")

def test_all_sufficient():
    m = run_test_without_output(8, 13)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) != 0 and len(secondary_list) != 0
    print("passed test_all_sufficient.")

def test_low_values():
    m = run_test_without_output(9, 0)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) == 0 and len(secondary_list) == 0
    print("passed test_low_values.")


def test_high_values():
    m = run_test_without_output(10, 13)
    primary_list, secondary_list = m.return_lists()
    assert len(primary_list) != 0 and len(secondary_list) != 0
    print("passed test_high_values.")

def run_primary_tests():
    test_temp()
    test_prcp()
    test_els()
    test_temp_and_prcp()
    test_temp_and_els()
    test_prcp_and_els()
    test_all_sufficient()
    test_low_values()
    test_high_values()

if __name__ == "__main__":
    run_primary_tests()