#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
from typing import Dict

import paramiko


class HDFSCluster:
    """This is a class that can operate on an HDFS cluster."""
    _client = None
    _client_host = None

    def __init__(self, host: str = "10.212.1.67", username: str = "root", password: str = "KGwydata!@#"):
        """Initialize the HDFS cluster by connecting to the host."""
        self._client = paramiko.SSHClient()
        self._client_host = host
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(host, username=username, password=password)

    def exec_command(self, command: str, host: str = None, timeout: int = 5) -> Dict:
        if host == None or self._client_host == host:
            stdin, stdout, stderr = self._client.exec_command(command)
        else:
            if host.find(":") != -1:
                host = host.split(":")[0]
            stdin, stdout, stderr = self._client.exec_command("ssh " + host + " '" + command + "'")

        stdout.channel.settimeout(timeout)
        retcode = 999

        try:
            output_stdout = stdout.read().decode('utf-8')
            output_stderr = stderr.read().decode('utf-8')
            retcode = stdout.channel.recv_exit_status()
        except socket.timeout as e:
            output_stdout = ""
            output_stderr = ""
            while True:
                try:
                    output_stdout += stdout.readline() + "\n"
                except socket.timeout as e:
                    break
            while True:
                try:
                    output_stderr += stderr.readline() + "\n"
                except socket.timeout as e:
                    break

        stdin = None
        stdout = None
        stderr = None

        return {"stdout": output_stdout, "stderr": output_stderr, "exitStatus": retcode}

    def get_namenodes(self) -> str:
        """
        Retrieves the list of NameNodes in the HDFS cluster.

        This method executes the 'hdfs haadmin -getAllServiceState' command to obtain the current state of all NameNodes
        in the Hadoop Distributed File System (HDFS) cluster. It is useful for checking the status and health of the NameNodes.

        :return: A string containing the standard output of the command execution, which includes the NameNode list.
        :rtype: str
        """
        res = self.exec_command("hdfs haadmin -getAllServiceState")
        return res['stdout']

    def hdfs_touchz(self) -> str:
        """ Creates a test file in HDFS.

        This method utilizes the 'hdfs dfs -touchz' command to create an empty file named 'test-file' within the Hadoop Distributed File System (HDFS).
        It is commonly used for testing write permissions on HDFS or checking the status of the file system.

        :return: A dictionary containing the result of the executed command.
        :rtype: str
        """
        res = self.exec_command("hdfs dfs -touchz test-file")
        return res

    # def hdfs_cat(self, path: str) -> str:
    #    """Read the file in HDFS and delete the test file."""
    #    res = self.exec_command("hdfs dfs -cat " + path)
    #    self.exec_command("hdfs dfs -rm " + path)
    #    return res['stdout']

    def namenode_log(self, host: str) -> str:
        """Retrieves the last portion of the NameNode logs from a specified host in an HDFS cluster.
        This method executes a command to change the directory to the Hadoop logs folder and 
        then uses the 'tail' command to fetch the last 30 lines of the NameNode log files. 
        It is useful for getting the most recent log entries which can be critical for troubleshooting.

        :param host: The hostname or IP address of the host where the NameNode is running.
        :type host: str
        :return: A string containing the last 2000 characters of the NameNode log output.
        :rtype: str
        """

        res = self.exec_command("cd /opt/datasophon/hadoop-3.3.3/logs && tail -n 30 hadoop-hdfs-namenode-*.log", host)
        return res['stdout'][-2000:]

    def get_local_disk_free(self, host: str):
        """
        Retrieves the local disk free space information from a specified host.

        This method uses the 'df' command to get the disk space information and
        returns the output related to the free disk space available on the
        given host within the HDFS cluster.

        :param host: The hostname or IP address of the host to check disk space.
        :type host: str
        :return: A string containing the output of the 'df' command.
        """

        res = self.exec_command("df", host)
        return res['stdout']

if __name__ == "__main__":
    class_instance = HDFSCluster("10.212.1.67")
    resp = class_instance.namenode_log("10.212.1.67")
    print(resp)
