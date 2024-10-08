
    sudo passwd root

    apt install synaptic
    apt install mc
    apt install htop
    apt install terminator

    gsettings set org.gnome.desktop.wm.keybindings switch-input-source "['<Shift>Alt_L']"
    gsettings set org.gnome.desktop.wm.keybindings switch-input-source-backward "['<Alt>Shift_L']"
    gsettings set org.freedesktop.ibus.panel.emoji hotkey "[]"

    apt install openssh-server
    
    vpn2gis.sh

    VNC (built-in) settings -> sharing -> remote desktop ON -> remote desktop/remote control/legacy : all ON -> your own password
    
    apt install ninja-build
    apt install cmake

    apt install postgresql
    sudo -i -u postgres
    createuser --interactive
    alter user renat with password 'bla-bla';
    
    https://apt.llvm.org/llvm.sh 17
    apt install clang-format-17
    apt install clang-tidy-17
    cd /usr/bin && ln -s /usr/bin/lldb-17 lldb
    ./llvm_update_alternatives.sh 17 0

    gcc-13 install:
    sudo add-apt-repository ppa:ubuntu-toolchain-r/test
    sudo apt update
    sudo apt install gcc-13 g++-13
    update-alternatives --display gcc
    sudo update-alternatives --remove-all gcc
    sudo update-alternatives --remove-all g++
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 10 --slave /usr/bin/g++ g++ /usr/bin/g++-13
    
    for bug "ModuleNotFoundError: No module named 'lldb.embedded_interpreter'"
    mkdir -p /usr/lib/local/lib/python3.10 && cd /usr/lib/local/lib/python3.10 && ln -s /usr/lib/llvm-14/lib/python3.10/dist-packages dist-packages
    
    dpkg -i google-chrome-stable_current_amd64.deb
    
    apt install libxcb-xinerama0
    launch WITHOUT INTERNET CONNECTION ./qt-creator-opensource-linux-x86_64-10.0.0.run
    + styles, settings
    help -> about plugins -> clangCodeModel
    ! Preferences -> C++ -> Clangd -> Diagnostic configuraion -> Checks for questionable constructs (must be empty)
    Preferences -> C++ -> Clang-Format -> full formatting
    put .clang-format file at root of project (near CMakeLists.txt)
    
    apt install git
    (not root)
    git config --global alias.st status
    git config --global alias.lg 'log --oneline -n 10'
    git config --global alias.pf 'push --force'
    git config --global alias.up 'remote update origin --prune'
    git config --global alias.co 'checkout'
    git config --global user.name '...'
    git config --global user.email ...
    git config --global core.editor "mcedit"
    apt install gitk
    
    apt install python3-pip
    pip3 install conan==1.64.0 (via sudo for global)
    (pip3 install --force-reinstall -v "conan==x.x.x")
    source ~/.profile
    + remotes, profiles
    
    apt install libcurl4-openssl-dev
    apt install curl
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt update
    apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    apt install docker-compose
    
    usermod -aG docker $USER
    
    curl -O https://storage.googleapis.com/kubernetes-release/release/v1.25.0/bin/linux/amd64/kubectl && chmod +x kubectl && mv kubectl /usr/local/bin/kubectl
    
    apt install libfuse2 (for lens)
    
    apt install golang-1.21
    apt install delve (debugger)
    cd /usr/bin && ln -s /usr/lib/go-1.21/bin/go && ln -s /usr/lib/go-1.21/bin/gofmt
    
    apt install python3-pynput (workflow_utility.py)
    
    // ? (for moses)
    apt install libfcgi-dev
    apt install libssl-dev
    apt install libunwind-dev

    apt install safeeyes

    apt install openresolv
    apt install wireguard

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash # under user
    nvm install 21 # node & npm will be installed
    npm install -g typescript # check by typing 'tsc'

    smb:
    sudo apt-get install cifs-utils
    /etc/fstab -> //server_ip/dir_name /pathto/mountpoint cifs username=...,password=...,rw,uid=1000,gid=500,vers=1.0    0    0
    check: mount -a

    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh

    mkdir 0-develop 1-sources 2-configs 3-docs 4-notes 5-________ 6-resources 7-artifacts 8-for_sort 9-temp
    mkdir 9-temp/downloads



    settings -> appearance -> dark	
    settings -> privacy -> screen
    settings -> privacy -> file history & trash -> file history OFF
    settings -> keyboard -> input sources
    settings -> accessibility -> enable animations (OFF)
    settings -> multitasking -> workspaces on all displays

    apps -> password and keys -> right click on "login" -> save empty pass
    
    other_locations -> smb://home_cloud -> login/pass
    
    install FreeFileSync
	
	



    
