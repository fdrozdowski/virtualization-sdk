#
# Copyright (c) 2019 by Delphix. All rights reserved.
#

import mock
import pytest

from dlpx.virtualization import libs_pb2
from dlpx.virtualization import libs
from dlpx.virtualization.libs.exceptions import LibraryError
from dlpx.virtualization import common_pb2

class TestLibs:

  @staticmethod
  def test_run_bash():
      expected_run_bash_response = libs_pb2.RunBashResponse()
      expected_run_bash_response.return_value.exit_code = 0
      expected_run_bash_response.return_value.stdout = "stdout"
      expected_run_bash_response.return_value.stderr = "stderr"

      expected_remote_connection = common_pb2.RemoteConnection()
      expected_remote_connection.environment.name = "RemoteConnectionEnv"
      expected_remote_connection.environment.reference = "remoteConnectionReference"
      expected_command = "command"
      expected_variables = None
      expected_use_login_shell = False

      def mock_run_bash(actual_run_bash_request):
          assert actual_run_bash_request.command == expected_command
          assert actual_run_bash_request.use_login_shell == expected_use_login_shell
          assert (actual_run_bash_request.remote_connection.environment.name ==
                  expected_remote_connection.environment.name)
          assert (actual_run_bash_request.remote_connection.environment.reference ==
                  expected_remote_connection.environment.reference)
          return expected_run_bash_response

      with mock.patch("dlpx.virtualization._engine.libs.run_bash",
                      side_effect=mock_run_bash, create=True):
          actual_run_bash_result = libs.run_bash(expected_remote_connection, expected_command, expected_variables,
                                                      expected_use_login_shell)

          assert actual_run_bash_result.exit_code == expected_run_bash_response.return_value.exit_code
          assert actual_run_bash_result.stdout == expected_run_bash_response.return_value.stdout
          assert actual_run_bash_result.stderr == expected_run_bash_response.return_value.stderr

  @staticmethod
  def test_run_bash_with_actionable_error():
      expected_id = 15
      expected_message = "Some message"

      response = libs_pb2.RunBashResponse()
      response.error.actionable_error.id = expected_id
      response.error.actionable_error.message = expected_message

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_bash",
                      return_value=response, create=True):
          with pytest.raises(LibraryError) as info:
              response = libs.run_bash(connection, "command")
          assert info.value._id == expected_id
          assert info.value.message == expected_message

  @staticmethod
  def test_run_bash_with_nonactionable_error():
      response = libs_pb2.RunBashResponse()
      na_error = libs_pb2.NonActionableLibraryError()
      response.error.non_actionable_error.CopyFrom(na_error)

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_bash",
                      return_value=response, create=True):
          with pytest.raises(SystemExit):
              response = libs.run_bash(connection, "command")

  @staticmethod
  def test_run_powershell():
      expected_run_powershell_response = libs_pb2.RunPowerShellResponse()
      expected_run_powershell_response.return_value.exit_code = 0
      expected_run_powershell_response.return_value.stdout = "stdout"
      expected_run_powershell_response.return_value.stderr = "stderr"

      expected_remote_connection = common_pb2.RemoteConnection()
      expected_remote_connection.environment.name = "RemoteConnectionEnv"
      expected_remote_connection.environment.reference = "remoteConnectionReference"
      expected_command = "command"
      expected_variables = None

      def mock_run_powershell(actual_run_powershell_request):
          assert actual_run_powershell_request.command == expected_command
          assert (actual_run_powershell_request.remote_connection.environment.name ==
                  expected_remote_connection.environment.name)
          assert (actual_run_powershell_request.remote_connection.environment.reference ==
                  expected_remote_connection.environment.reference)
          return expected_run_powershell_response

      with mock.patch("dlpx.virtualization._engine.libs.run_powershell",
                      side_effect=mock_run_powershell, create=True):
          actual_run_powershell_result = libs.run_powershell(expected_remote_connection,
                                                            expected_command, expected_variables)

          assert actual_run_powershell_result.exit_code == expected_run_powershell_response.return_value.exit_code
          assert actual_run_powershell_result.stdout == expected_run_powershell_response.return_value.stdout
          assert actual_run_powershell_result.stderr == expected_run_powershell_response.return_value.stderr

  @staticmethod
  def test_run_powershell_with_actionable_error():
      expected_id = 15
      expected_message = "Some message"

      response = libs_pb2.RunPowerShellResponse()
      response.error.actionable_error.id = expected_id
      response.error.actionable_error.message = expected_message

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_powershell",
                      return_value=response, create=True):
          with pytest.raises(LibraryError) as info:
              response = libs.run_powershell(connection, "command")
          assert info.value._id == expected_id
          assert info.value.message == expected_message

  @staticmethod
  def test_run_powershell_with_nonactionable_error():
      response = libs_pb2.RunPowerShellResponse()
      na_error = libs_pb2.NonActionableLibraryError()
      response.error.non_actionable_error.CopyFrom(na_error)

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_powershell",
                      return_value=response, create=True):
          with pytest.raises(SystemExit):
              response = libs.run_powershell(connection, "command")

  @staticmethod
  def test_run_sync_with_actionable_error():
      expected_id = 15
      expected_message = "Some message"

      response = libs_pb2.RunSyncResponse()
      response.error.actionable_error.id = expected_id
      response.error.actionable_error.message = expected_message

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_sync",
                      return_value=response, create=True):
          with pytest.raises(LibraryError) as info:
             response = libs.run_sync(connection, "dir")
          assert info.value._id == expected_id
          assert info.value.message == expected_message

  @staticmethod
  def test_run_sync_with_nonactionable_error():

      response = libs_pb2.RunSyncResponse()
      na_error = libs_pb2.NonActionableLibraryError()
      response.error.non_actionable_error.CopyFrom(na_error)

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_sync",
                      return_value=response, create=True):
          with pytest.raises(SystemExit):
              response = libs.run_sync(connection, "dir")

  @staticmethod
  def test_run_sync():

      expected_run_sync_response = libs_pb2.RunSyncResponse()

      expected_remote_connection = common_pb2.RemoteConnection()
      expected_remote_connection.environment.name = "RemoteConnectionEnv"
      expected_remote_connection.environment.reference = "remoteConnectionReference"
      expected_source_directory = "sourceDirectory"
      expected_rsync_user = "rsyncUser"
      expected_exclude_paths = { "/path1", "/path2" }
      expected_sym_links_to_follow = { "/path3", "/path4" }

      def mock_run_sync(actual_run_sync_request):
          assert actual_run_sync_request.source_directory == expected_source_directory
          assert (actual_run_sync_request.remote_connection.environment.name ==
                  expected_remote_connection.environment.name)
          assert (actual_run_sync_request.remote_connection.environment.reference ==
                  expected_remote_connection.environment.reference)
          assert actual_run_sync_request.rsync_user == expected_rsync_user
          assert list(actual_run_sync_request.exclude_paths) == list(expected_exclude_paths)
          assert list(actual_run_sync_request.sym_links_to_follow) == list(expected_sym_links_to_follow)

          return expected_run_sync_response

      with mock.patch("dlpx.virtualization._engine.libs.run_sync",
                      side_effect=mock_run_sync, create=True):
          actual_runsync_response = libs.run_sync(expected_remote_connection, expected_source_directory,
                                                  expected_rsync_user, expected_exclude_paths,
                                                  expected_sym_links_to_follow)

          assert actual_runsync_response is None

  @staticmethod
  def test_run_expect():
      expected_run_expect_response = libs_pb2.RunExpectResponse()

      expected_remote_connection = common_pb2.RemoteConnection()
      expected_remote_connection.environment.name = "RemoteConnectionEnv"
      expected_remote_connection.environment.reference = "remoteConnectionReference"
      expected_command = "command"
      expected_variables = None

      def mock_run_expect(actual_run_expect_request):
          assert actual_run_expect_request.command == expected_command
          assert (actual_run_expect_request.remote_connection.environment.name ==
                  expected_remote_connection.environment.name)
          assert (actual_run_expect_request.remote_connection.environment.reference ==
                  expected_remote_connection.environment.reference)
          return expected_run_expect_response

      with mock.patch("dlpx.virtualization._engine.libs.run_expect",
                      side_effect=mock_run_expect, create=True):
          actual_run_expect_response = libs.run_expect(expected_remote_connection,
                                                       expected_command, expected_variables)

          assert actual_run_expect_response is None

  @staticmethod
  def test_run_expect_with_actionable_error():
      expected_id = 15
      expected_message = "Some message"

      response = libs_pb2.RunExpectResponse()
      response.error.actionable_error.id = expected_id
      response.error.actionable_error.message = expected_message

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_expect",
                      return_value=response, create=True):
          with pytest.raises(LibraryError) as info:
             response = libs.run_expect(connection, "command")
          assert info.value._id == expected_id
          assert info.value.message == expected_message

  @staticmethod
  def test_run_sync_with_nonactionable_error():

      response = libs_pb2.RunExpectResponse()
      na_error = libs_pb2.NonActionableLibraryError()
      response.error.non_actionable_error.CopyFrom(na_error)

      connection = common_pb2.RemoteConnection()
      connection.environment.name = "name"
      connection.environment.reference = "ref"

      with mock.patch("dlpx.virtualization._engine.libs.run_expect",
                      return_value=response, create=True):
          with pytest.raises(SystemExit):
              response = libs.run_expect(connection, "command")