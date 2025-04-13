import os
import subprocess
import re

class SVNRepoSync:
    def __init__(self, repo1_url, repo2_path, username, password):
        """
        初始化 SVN 仓库同步器.

        Args:
            repo1_url (str): 源 SVN 仓库的 URL.
            repo2_path (str): 目标 SVN 仓库的本地路径.
            username (str): SVN 用户名.
            password (str): SVN 密码.
        """
        self.repo1_url = repo1_url
        self.repo2_path = repo2_path
        self.username = username
        self.password = password

    def run_svn_command(self, command, repo_path=None):
        """
        运行 SVN 命令行命令.

        Args:
            command (list): SVN 命令及其参数的列表.
            repo_path (str, optional): 仓库的本地路径.  如果需要认证，可以设置为仓库的路径

        Returns:
            tuple: (return_code, stdout, stderr)
        """
        cmd = ["svn"] + command
        env = os.environ.copy()
        if self.username and self.password and repo_path: #认证信息，仅在需要时添加
            env["SVN_USER"] = self.username
            env["SVN_PASSWORD"] = self.password
        try:
            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=False, env=env)
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            print("Error: svn command not found. Please ensure it is installed and in your PATH.")
            return 1, "", "svn command not found" # 返回错误码 1

    def update_repo(self, repo_path):
        """
        更新 SVN 仓库到最新版本.

        Args:
            repo_path (str): 仓库的本地路径.
        """
        print(f"Updating repository: {repo_path}")
        return_code, stdout, stderr = self.run_svn_command(["update"], repo_path)

        if return_code == 0:
            print(f"Repository updated successfully: {repo_path}")
        else:
            print(f"Error updating repository: {repo_path} - {stderr}")
            raise Exception(f"SVN update failed: {stderr}") # 抛出异常，终止程序

    def get_recent_commits(self, repo_url, limit=100):
        """
        获取最近的提交记录.

        Args:
            repo_url (str): 仓库的 URL.
            limit (int): 获取的提交记录数量限制.

        Returns:
            list: 提交记录列表，每个记录是一个字典.
        """
        print(f"Retrieving recent commits from: {repo_url}")
        return_code, stdout, stderr = self.run_svn_command(["log", repo_url, "-l", str(limit), "--xml"], repo_url)

        if return_code != 0:
            print(f"Error retrieving commits: {stderr}")
            return []

        # 解析 XML 输出 (简化版本，可以使用专业的 XML 解析库)
        commits = []
        commit_blocks = re.findall(r"<logentry.*?>(.*?)</logentry>", stdout, re.DOTALL)

        for block in commit_blocks:
            revision_match = re.search(r'revision="(\d+)"', block)
            if revision_match:
                revision = revision_match.group(1)
                paths_block = re.search(r"<paths>(.*?)</paths>", block, re.DOTALL)
                changed_paths = []

                if paths_block:
                    path_entries = re.findall(r"<path.*?>(.*?)</path>", paths_block.group(1), re.DOTALL)
                    for path_entry in path_entries:
                        action_match = re.search(r'action="(\w+)"', path_entry)
                        path_value = re.search(r">(.*?)</path>",path_entry).group(1)
                        if action_match:
                            action = action_match.group(1).upper()  # 将动作转换为大写
                            changed_paths.append({"path": path_value, "action": action})

                commits.append({"revision": revision, "changed_paths": changed_paths})

        print(f"Retrieved {len(commits)} commits.")
        return commits

    def sync_changes(self, commits):
        """
        同步提交记录到目标仓库.

        Args:
            commits (list): 提交记录列表.
        """
        for commit in commits:
            print(f"Processing commit revision: {commit['revision']}")
            for change in commit['changed_paths']:
                repo1_path = os.path.join(self.repo1_url, change['path'])
                repo2_path = os.path.join(self.repo2_path, change['path'].lstrip('/')) # 去除路径开头的斜杠
                action = change['action']

                if action in ("ADD", "MODIFY", "REPLACE"):
                    try:
                        os.makedirs(os.path.dirname(repo2_path), exist_ok=True)

                        # 使用 svn cat 下载文件
                        return_code, stdout, stderr = self.run_svn_command(["cat", repo1_path],self.repo1_url)  #需要认证
                        if return_code == 0:
                            with open(repo2_path, "w", encoding="utf-8") as f:
                                f.write(stdout)
                            print(f"Copied/Modified: {change['path']}")
                        else:
                            print(f"Error downloading {change['path']}: {stderr}")

                    except Exception as e:
                        print(f"Error copying/modifying {change['path']}: {e}")

                elif action == "DELETE":
                    try:
                        if os.path.exists(repo2_path):
                            self.svn_delete(repo2_path)
                            print(f"Deleted: {change['path']}")
                    except Exception as e:
                        print(f"Error deleting {change['path']}: {e}")
                else:
                    print(f"Skipping change type: {action} for {change['path']}")

    def svn_delete(self, path):
        """
        使用svn delete 命令删除文件或目录
        """
        try:
             return_code, stdout, stderr = self.run_svn_command(["delete", path, "--force"], self.repo2_path) #需要认证
             if return_code != 0:
                 print(f"Error deleting {path}: {stderr}")
                 raise Exception(f"SVN delete failed: {stderr}")
        except Exception as e:
            print(f"Error deleting {path}: {e}")
            raise

    def commit_changes(self, message="Sync changes from repo1"):
        """
        提交目标仓库的更改.
        """
        try:
            print(f"Committing changes to: {self.repo2_path}")
            return_code, stdout, stderr = self.run_svn_command(["add", "--force", "."], self.repo2_path)  # 添加未版本控制的文件/目录
            if return_code != 0:
                print(f"Error adding files: {stderr}")

            return_code, stdout, stderr = self.run_svn_command(["commit", "-m", message], self.repo2_path) #需要认证
            if return_code == 0:
                print(f"Changes committed successfully to: {self.repo2_path}")
            else:
                print(f"Error committing changes: {stderr}")
                raise Exception(f"SVN commit failed: {stderr}")  # 抛出异常，终止程序

        except Exception as e:
            print(f"Error committing changes: {e}")
            raise

if __name__ == '__main__':
    # 配置信息
    repo1_url = "svn://your_repo1_url"  # 替换为你的 repo1 URL
    repo2_path = "/path/to/your/repo2"  # 替换为你的 repo2 本地路径
    username = "your_svn_username"  # 替换为你的 SVN 用户名
    password = "your_svn_password"  # 替换为你的 SVN 密码

    # 创建同步器实例
    sync = SVNRepoSync(repo1_url, repo2_path, username, password)

    # 1. 更新两个仓库
    sync.update_repo(repo2_path)

    # 2. 获取最近的提交记录
    commits = sync.get_recent_commits(repo1_url)

    # 3. 同步更改
    sync.sync_changes(commits)

    # 4. 提交目标仓库的更改
    sync.commit_changes()

    print("SVN repository synchronization completed.")