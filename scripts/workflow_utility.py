import subprocess
import threading
from pynput import keyboard
import sys
import os
import re

PRINT_TAG: str = "workflow_utility"
CLANG_FORMAT_CMD: str = "clang-format --style=file -i -Werror"
SUBMODULE_LIBS: list = [
    "carrouting",
    "ctx",
    "software",
    "thirdparty",
    "traffic-software",
    "traffic-thirdparty",
    "navi-schema-registry",
    "map_matching"]

condition = threading.Condition()

class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ----------------------------------------------------------------------------------------------------------------------
# supporting functional
# ----------------------------------------------------------------------------------------------------------------------
def PrintWarning(msg: str):
    print(TerminalColors.WARNING + TerminalColors.BOLD + msg + TerminalColors.ENDC)

def PrintError(msg: str):
    print(TerminalColors.FAIL + TerminalColors.BOLD + msg + TerminalColors.ENDC)

def RunGit(git_flags: list, print_err_msg: bool = True) -> str :
    proc_args: list = ["git"] + git_flags
    process: subprocess.Popen = subprocess.Popen(proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    stdout, stderr = process.communicate()
    exit_code: int = process.returncode
    if exit_code != 0:
        if print_err_msg:
            PrintError("> error occured while executing '{}', reason: {}".format(proc_args, stderr))
            print("> stdout while error: {}".format(stdout))
        return None

    return stderr + stdout

def RunClangFormat(file_to_format: list):
    proc_args: list = ["clang-format", "--style=file", "-i", "-Werror", file_to_format]
    process: subprocess.Popen = subprocess.Popen(proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    stdout, stderr = process.communicate()
    if len(stderr) != 0:
        PrintError("> error occured while executing '{}', reason: {}".format(proc_args, stderr))

    if len(stdout) != 0:
        print("> output of clang-format: {}".format(proc_args, stdout))

g_option_idx: int = 0
g_option_chosen: bool = False

def OnRelease(key):
    global g_option_idx
    global g_option_chosen

    if key == keyboard.Key.up and g_option_idx > 0:
        g_option_idx = g_option_idx - 1
    elif key == keyboard.Key.down:
        g_option_idx = g_option_idx + 1
    elif key == keyboard.Key.space:
        g_option_chosen = True
        
    return False

def ChooseBranch(branch_name_prefix: str) -> str:
    stdout = RunGit(["branch", "--list", "--all", "*" + branch_name_prefix + "*"])
    assert(stdout != None)
        
    out_lines: list = stdout.splitlines()
    if len(out_lines) == 1:
        return out_lines[0][2:]
    elif len(out_lines) > 1:
        global g_option_idx
        global g_option_chosen

        out_lines.append("  <exit>")

        while True:    
            os.system('clear')
            print("> choose branch:")

            # add underscore to current option
            for idx in range(0, len(out_lines)):
                branch_name:str = out_lines[idx][2:]
                if idx == g_option_idx:
                    print("{} {}".format(TerminalColors.BOLD + "*" + TerminalColors.ENDC, TerminalColors.UNDERLINE + TerminalColors.BOLD + branch_name + TerminalColors.ENDC))
                else:
                    print("  {}".format(branch_name))

            # catch released key and join listening thread
            with keyboard.Listener(suppress=True, on_release=OnRelease) as listener:
                listener.join()

            if g_option_chosen:
                break

            # prevent from out-of-range
            if g_option_idx >= len(out_lines):
                g_option_idx = len(out_lines) - 1

        os.system('clear')
        chosen_options: str = out_lines[g_option_idx][2:]
        if chosen_options != "<exit>":
            return chosen_options
        else:
            return None

def PrintStatusWithHighlightedBranch(status_output: str):
    for line in status_output.splitlines():
                        if line.find("On branch") != -1:
                            print(line[:10], end = '')
                            print("{}{}{}".format(TerminalColors.OKGREEN + TerminalColors.BOLD, line[10:], TerminalColors.ENDC))
                        else:
                            print(line)

# ----------------------------------------------------------------------------------------------------------------------
# main functional
# ----------------------------------------------------------------------------------------------------------------------
def SwitchToBranch(args: list):
    # rebuild boost ? (check commit hashes before switching main branch)

    # is this super-project or sub-project
    is_superproject: bool = False
    stdout = RunGit(["rev-parse", "--show-superproject-working-tree"])
    if stdout != None and len(stdout) == 0:
        is_superproject = True

    # super-project: switch it and all sub-projects
    if is_superproject:
        stdout = RunGit(["rev-parse", "--show-toplevel"])
        root_project_top: str = stdout[:-1]
        toplevel_basename = os.path.basename(stdout)[:-1]
        os.chdir(root_project_top)

        branch_name: str = ChooseBranch(args[2])
        if branch_name == None:
            return

        print("{}[{}]{}".format(TerminalColors.OKCYAN + TerminalColors.BOLD, toplevel_basename, TerminalColors.ENDC))
        stdout = RunGit(["checkout", branch_name])
        if stdout != None:
            print(stdout)

        # TODO: remove 'remotes/origin/' from branch name

        # check boost commit hashes before...
        if os.path.exists(root_project_top + "libraries/boost"):
            compiled_regexp = re.compile("^HEAD detached at ([a-f0-9]*)")
            os.chdir("libraries/boost")

            stdout = RunGit(["status"])
            if stdout != None:
                for line in stdout.splitlines():
                    match = compiled_regexp.match(line)
                    if match != None:
                        boost_commit_hash_before: str = match.group(1)
                        break
            os.chdir(root_project_top)

        # 1st step: switch to default dependent subs
        print("> update submodules")
        stdout = RunGit(["submodule", "update", "--recursive"])
        if stdout != None:
            print(stdout)

        # ...and after update (because it builds separately)
        if os.path.exists(root_project_top + "libraries/boost"):
            os.chdir("libraries/boost")
            stdout = RunGit(["status"])
            if stdout != None:
                for line in stdout.splitlines():
                    match = compiled_regexp.match(line)
                    if match != None:
                        boost_commit_hash_after: str = match.group(1)
                        break
            os.chdir(root_project_top)

            if len(boost_commit_hash_before) != 0 and len(boost_commit_hash_after) != 0:
                if boost_commit_hash_before != boost_commit_hash_after:
                    print("> boost commit hashes differ (before {} - after {}), so rebuild it (TODO)".format(boost_commit_hash_before, boost_commit_hash_after))
                    print()
            else:
                PrintError("> boost commit hashes before or after is not found, cannot check for rebuild")
                print()
        
        # main branches is controls by RBMP
        if branch_name == "develop" or branch_name == "master":
            return

        # 2nd step: try to switch to target branch if it exists
        for submodule in SUBMODULE_LIBS:
            submodule_dir: str = root_project_top + "/libraries/" + submodule
            if os.path.exists(submodule_dir):
                os.chdir(submodule_dir)
                stdout = RunGit(["checkout", branch_name], False)
                if stdout != None:
                    print("{}[{}]{}".format(TerminalColors.WARNING + TerminalColors.BOLD, submodule, TerminalColors.ENDC))
                    print(stdout)

    # sub-project: just switch one branch
    else:
        branch_name: str = ChooseBranch(args[2])
        if branch_name == None:
            return

        stdout = RunGit(["checkout", branch_name])
        if stdout != None:
            print(stdout)

def UpdateCurrentRepo():
    print("> update from remote")
    stdout = RunGit(["remote", "update", "origin", "--prune"])
    if stdout != None:
        print(stdout)
    else:
        return

    # pull changes only they exists
    stdout = RunGit(["status"])
    if stdout.find("can be fast-forwarded") != -1:
        print("> apply changes to workdir")
        stdout = RunGit(["pull", "--rebase", "origin"])
        if stdout != None:
            print(stdout)

    # update submodules only if it's a super-project
    stdout = RunGit(["rev-parse", "--show-superproject-working-tree"])
    if len(stdout) == 0:
        print("> update submodules")
        stdout = RunGit(["submodule", "update", "--recursive"])
        if stdout != None:
            print(stdout)

def PrintInfo():    
    stdout = RunGit(["remote", "-v"])
    if stdout != None:
        print(stdout)
    stdout = RunGit(["branch", "--show-current"])
    if stdout != None:
        print(stdout)
    stdout = RunGit(["log", "-n", "10", "--oneline", "--decorate=short"])
    if stdout != None:
        print(stdout)

def PrintStatus(args: list):
    # simple output of current repo
    if len(args) == 2:
        stdout = RunGit(["status"])
        if stdout != None:
            print(stdout)
    # full output including submodules
    elif args[2] == "all":
        stdout = RunGit(["rev-parse", "--show-superproject-working-tree"])
        # this is superproject
        if stdout != None and len(stdout) == 0:
            stdout = RunGit(["rev-parse", "--show-toplevel"])
            toplevel_basename = os.path.basename(stdout)[:-1]

            # root project
            print("{}[{}]{}".format(TerminalColors.OKCYAN + TerminalColors.BOLD, toplevel_basename, TerminalColors.ENDC))
            stdout = RunGit(["status"])
            if stdout != None:
                PrintStatusWithHighlightedBranch(stdout)

            # submodules
            stdout = RunGit(["rev-parse", "--show-toplevel"])
            root_project_top: str = stdout[:-1]
            os.chdir(root_project_top)

            for submodule_name in SUBMODULE_LIBS:
                submodule_dir: str = root_project_top + "/libraries/" + submodule_name
                if os.path.exists(submodule_dir):
                    os.chdir(submodule_dir)
                    print("{}[{}]{}".format(TerminalColors.WARNING + TerminalColors.BOLD, submodule_name, TerminalColors.ENDC))
                    stdout = RunGit(["status"])
                    if stdout != None:
                        PrintStatusWithHighlightedBranch(stdout)
                        print()
        # this is some subproject
        elif stdout != None:
            stdout = RunGit(["status"])
            if stdout != None:
                print(stdout)
        else:
            pass
    else:
        PrintError("unknown additional key for status command")

def ApplyClangFormat():
    # is this super-project or sub-project
    stdout = RunGit(["rev-parse", "--show-superproject-working-tree"])
    if None == stdout:
        return

    superproject_dir: str
    is_superproject: bool = False
    if len(stdout) == 0:
        is_superproject = True
    else:
        superproject_dir = stdout[:-1]

    # go to repo root
    stdout = RunGit(["rev-parse", "--show-toplevel"])
    project_root: str = stdout[:-1]

    if not is_superproject:
        subproject_name: str = os.path.basename(project_root)

    os.chdir(project_root)

    # collect modified files
    stdout = RunGit(["status"])
    compiled_regexp = re.compile("\t(?:modified|new file):[ ]*(.*\.(?:h|cpp|c|inl))")

    modified_files_relative_to_repo: list = []
    for line in stdout.splitlines():
        match = compiled_regexp.match(line)
        if match != None:
            modified_files_relative_to_repo.append(match.group(1))

    if len(modified_files_relative_to_repo) == 0:
        print("nothing to format, exit")
        return

    # if superproject exists - go to it and then jump to clang-format dir
    if not is_superproject:
        os.chdir(superproject_dir)

    clang_format_dir: str = os.getcwd() + "/libraries/repo-tools"
    os.chdir(clang_format_dir)

    for file in modified_files_relative_to_repo:
        file_absolute_path: str
        if is_superproject:
            file_absolute_path = project_root + "/" + file
        else:
            file_absolute_path = superproject_dir + "/libraries/" + subproject_name + "/" + file

        print("clang-format applied to: {}".format(file_absolute_path))
        RunClangFormat(file_absolute_path)

def CommitChanges(args: list):
    # create message with ticket number from branch name
    stdout = RunGit(["branch", "--show-current"])
    if None == stdout:
        return
        
    compiled_regexp = re.compile("^(TRAFFIC-[0-9]{1,5}).*")
    match = compiled_regexp.match(stdout)
    commit_message: str
    if match != None:
        commit_message = "[" + match.group(1) + "]"
        for i in range(len(args) - 2):
            commit_message = commit_message + " " + args[i+2]
    else:
        PrintError("'TRAFFIC-xxxxx' prefix is not found in branch name, exit")
        return

    # commit
    stdout = RunGit(["commit", "-m", commit_message])
    print(stdout)

    # for ensure
    stdout = RunGit(["log", "-n", "5", "--oneline"])
    print(stdout)

def PrepareNewProject():
    print("TODO: prepare new project")
    # choose type (moses, router, attractor, etc...)
    # dir name
    # ask 'are you sure?'

def BackupModifiedFiles():
    print("TODO: backup modified files")
    # run git status and get paths with prefix "modified: "
    # copy this files to dir [project dir name_branch-name_commit]
    # checkout them in current workspace

def FullRebuild():
    print("TODO: full rebuild")
    # delete build dir
    # build boost
    # call build.sh

def SquachCommits(args: list):
    if len(args) < 4:
        PrintError("too few arguments for commits squashing")
        return

    commits_count_to_squash: int = int(args[2]) # TODO: hint is just a recomendation ?
    if commits_count_to_squash < 2:
        PrintError("nothing to squash, commits count must be greater than 1, exit")
        return

    # get ticket prefix from branch name
    stdout = RunGit(["branch", "--show-current"])
    if None == stdout:
        return
    branch_name: str = stdout
        
    compiled_regexp = re.compile("^(TRAFFIC-[0-9]{1,5}).*")
    match = compiled_regexp.match(branch_name)
    if None == match:
        PrintError("'TRAFFIC-xxxxx' prefix is not found in branch name, exit")
        return
    ticket_number: str = "[" + match.group(1) + "]"

    # check presense of this prefix in all N commits (in order to prevent from squashing commits, which is not related to this ticket)
    commits_to_log: int = commits_count_to_squash + 1
    git_log_cmd: list = ["log", "-n", str(commits_to_log), "--oneline"]
    stdout = RunGit(git_log_cmd)

    commits_with_this_ticket_num: int = 0
    for line in stdout.splitlines():
        if line.find(ticket_number) != -1:
            commits_with_this_ticket_num = commits_with_this_ticket_num + 1

    if commits_count_to_squash > commits_with_this_ticket_num:
        PrintError("number of requested commits more than found, exit")
        return

    print("> try to squash {} commits, current log:".format(commits_count_to_squash))
    print(stdout)

    stdout = RunGit(["reset", "--soft", "HEAD~" + str(commits_count_to_squash)])
    if stdout != None:
        print(stdout)

    print("> save all resetted commits as one")
    stdout = RunGit(["commit", "-m", ticket_number + " " + args[3]])
    if stdout != None:
        print(stdout)

def PrintHelp():
    print("sw - [BRANCH_NAME] switch to another branch in all repos")
    print("up - update current repo")
    print("if - print repo info")
    print("st - git status")
    print("cf - run clang-format on modified files in current repo")

    print("ci - [MSG] commit formatted message")
    print("np - [PRJ_NAME] [DIR_NAME] create fresh project")
    print("bk - backup modified files of current repo and checkout them")
    print("rb - completely remove build directory and build project again")
    print("sq - [COMMITS_COUNT] [COMMIT_MSG] squash commits")

# ----------------------------------------------------------------------------------------------------------------------
# entry point
# ----------------------------------------------------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        PrintError("too few args, print 'hp' for help, exit")
        sys.exit(1)

    if "sw" == sys.argv[1]:
        SwitchToBranch(sys.argv)
    elif "up" == sys.argv[1]:
        UpdateCurrentRepo()
    elif "if" == sys.argv[1]:
        PrintInfo()
    elif "st" == sys.argv[1]:
        PrintStatus(sys.argv)
    elif "cf" == sys.argv[1]:
        ApplyClangFormat()
    elif "ci" == sys.argv[1]:
        CommitChanges(sys.argv)
    elif "np" == sys.argv[1]:
        PrepareNewProject()
    elif "bk" == sys.argv[1]:
        BackupModifiedFiles()
    elif "rb" == sys.argv[1]:
        FullRebuild()
    elif "sq" == sys.argv[1]:
        SquachCommits(sys.argv)
    elif "hp" == sys.argv[1]:
        PrintHelp()
    else:
        PrintError("unknown command, print 'hp' for help, exit")
        sys.exit(1)

if __name__ == "__main__":
    main()

