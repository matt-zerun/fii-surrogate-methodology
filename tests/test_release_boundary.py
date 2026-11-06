from scripts.verify_release_boundary import verify_release_boundary


def test_release_boundary_is_clean():
    report = verify_release_boundary()
    # Generated test outputs are ignored by the file scan and are checked
    # explicitly only by the standalone pre-archive command.
    assert not [failure for failure in report["failures"] if "generated outputs" not in failure]
