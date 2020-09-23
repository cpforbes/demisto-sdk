from pathlib import Path

import pytest
from demisto_sdk.commands.lint import linter
from demisto_sdk.tests.constants_test import (
    GIT_ROOT, XSOAR_LINTER_PY3_INVALID, XSOAR_LINTER_PY3_INVALID_WARNINGS,
    XSOAR_LINTER_PY3_INVALID_WARNINGS_PARTNER, XSOAR_LINTER_PY3_VALID)

files = [
    (Path(f"{XSOAR_LINTER_PY3_VALID}"), 3.8, 'base', False, 0, []),
    (Path(f"{XSOAR_LINTER_PY3_VALID}"), 3.8, 'base', True, 0, []),
    (Path(f"{XSOAR_LINTER_PY3_INVALID}"), 3.8, 'base', True, 1, [
        'Print is found, Please remove all prints from the code.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID}"), 3.8, 'base', False, 1, [
        'Print is found, Please remove all prints from the code.',
        'Sleep is found, Please remove all sleep statements from the code.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID_WARNINGS}"), 3.8, 'certified partner', False, 0,
     ['Demisto.log is found, Please remove all demisto.log usage and exchange it with',
      'Main function wasnt found in the file, Please add main()',
      'Do not use return_outputs function. Please return CommandResults object instead.',
      'Do not use demisto.results function.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID}"), 3.8, 'certified partner', False, 1,
     ['Sys.exit use is found, Please use return instead.',
      'Sleep is found, Please remove all sleep statements from the code.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID}"), 3.8, 'certified partner', True, 1,
     ['Sys.exit use is found, Please use return instead.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID}"), 3.8, 'community', False, 1,
     ['Print is found, Please remove all prints from the code.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID_WARNINGS_PARTNER}"), 3.8, 'partner', False, 0,
     ['try and except statements were not found in main function.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID_WARNINGS_PARTNER}"), 3.8, 'community', False, 0,
     []),
    (Path(f"{XSOAR_LINTER_PY3_INVALID_WARNINGS_PARTNER}"), 3.8, 'partner', False, 0,
     ['return_error should be used in main function. Please add it.',
      'return_error used too many times, should be used only once in the code, in main function.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID_WARNINGS_PARTNER}"), 3.8, 'xsoar', False, 0,
     ['return_error should be used in main function. Please add it.',
      'return_error used too many times, should be used only once in the code, in main function.']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID}"), 3.8, '', False, 1,
     ['exit is found, Please remove all exit()', 'quit is found, Please remove all quit()']),
    (Path(f"{XSOAR_LINTER_PY3_INVALID}"), 3.8, 'xsoar', False, 1,
     ['exit is found, Please remove all exit()', 'quit is found, Please remove all quit()']),

]


@pytest.mark.parametrize('file, python_version,support_level,long_running,exit_code,error_msgs', files)
def test_xsoar_linter_errors(mocker, file, python_version, support_level, long_running, exit_code, error_msgs):
    """
    Given
    - file to run the linter on.
    - Python version of the file.
    - expected exit code of the xsoar linter function.
    - expected error messages of the xosar linter.

    When
    - Running xsoar linter using demisto lint.

    Then
    - Ensure valid files pass with the correct exit code.
    - Ensure valid files pass with no error messages.
    - Ensure invalid files fail with the correct exit code.
    - Ensure invalid files fail with the correct error messages.
    """

    mocker.patch.object(linter.Linter, '_docker_login')
    mocker.patch.object(linter.Linter, '_update_support_level')
    linter.Linter._docker_login.return_value = False
    test_path = Path(f"{GIT_ROOT}/demisto_sdk/tests/test_files")

    runner = linter.Linter(content_repo=test_path,
                           pack_dir=test_path,
                           req_2=[],
                           req_3=[],
                           docker_engine=True)
    runner._facts['support_level'] = support_level
    runner._facts['is_long_running'] = long_running
    exit_code_actual, output = runner._run_xsoar_linter(python_version, [file])
    assert exit_code == exit_code_actual
    for msg in error_msgs:
        assert msg in output
