"""
Test classes that should be shared between test scenarios.
"""
import os
import shutil
from tempfile import mkdtemp

REQUIRED_ROLE = "user@bx.psu.edu"
REQUIRED_GROUP = "fs_test_group"


def get_posix_file_source_config(root_dir: str, roles: str, groups: str) -> str:
    return f"""
- type: posix
  id: posix_test
  label: Posix
  doc: Files from local path
  root: {root_dir}
  writable: true
  requires_roles: {roles}
  requires_groups: {groups}

"""


def create_file_source_config_file_on(temp_dir, root_dir):
    file_contents = get_posix_file_source_config(root_dir, REQUIRED_ROLE, REQUIRED_GROUP)
    file_path = os.path.join(temp_dir, "file_sources_conf_posix.yml")
    with open(file_path, "w") as f:
        f.write(file_contents)
    return file_path


class PosixFileSourceSetup:

    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        temp_dir = os.path.realpath(mkdtemp())
        cls._test_driver.temp_directories.append(temp_dir)
        cls.root_dir = os.path.join(temp_dir, "root")

        file_sources_config_file = create_file_source_config_file_on(temp_dir, cls.root_dir)
        config["file_sources_config_file"] = file_sources_config_file

        # Disable all stock plugins
        config["ftp_upload_dir"] = None
        config["library_import_dir"] = None
        config["user_library_import_dir"] = None

    def _write_file_fixtures(self):
        root = self.root_dir
        if os.path.exists(root):
            shutil.rmtree(root)
        os.mkdir(root)

        with open(os.path.join(root, "a"), "w") as f:
            f.write("a\n")

        subdir1 = os.path.join(root, "subdir1")
        os.mkdir(subdir1)
        with open(os.path.join(subdir1, "b"), "w") as f:
            f.write("b\n")

        return root

    def setUp(self):
        super().setUp()
        self._write_file_fixtures()
