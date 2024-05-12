
    sudo passwd root

    apt install synaptic
    apt install mc

    gsettings set org.gnome.desktop.wm.keybindings switch-input-source "['<Shift>Alt_L']"
    gsettings set org.gnome.desktop.wm.keybindings switch-input-source-backward "['<Alt>Shift_L']"
    gsettings set org.freedesktop.ibus.panel.emoji hotkey "[]"

    apt install openssh-server
    
    vpn2gis.sh

    VNC (built-in) settings -> sharing -> remote desktop ON -> remote desktop/remote control/legacy : all ON -> your own password
    
    apt install htop
    
    apt install cmake
    
    https://apt.llvm.org/llvm.sh 17
    apt install clang-format-17
    apt install clang-tidy-17
    ./llvm_update_alternatives.sh 17 0
    
    for bug "ModuleNotFoundError: No module named 'lldb.embedded_interpreter'"
    mkdir -p /usr/lib/local/lib/python3.10 && cd /usr/lib/local/lib/python3.10 && ln -s /usr/lib/llvm-14/lib/python3.10/dist-packages dist-packages
    
    dpkg -i google-chrome-stable_current_amd64.deb
    
    apt install libxcb-xinerama0
    launch WITHOUT INTERNET CONNECTION ./qt-creator-opensource-linux-x86_64-10.0.0.run
    + styles, settings
    ! Preferences -> C++ -> Clangd -> Diagnostic configuraion -> Checks for questionable constructs (must be empty)
    
    apt install git
    (not root)
    git config --global alias.st status
    git config --global alias.lg 'log --oneline -n 10'
    git config --global user.name '...'
    git config --global user.email ...
    git config --global core.editor "mcedit"
    
    apt install python3-pip
    pip3 install conan==1.60.0 (via sudo for global)
    (pip3 install --force-reinstall -v "conan==x.x.x")
    source ~/.profile
    + remotes, profiles
    
    apt install ninja-build
    
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
    
    apt install gitk
    
    apt install terminator  
    
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


    
