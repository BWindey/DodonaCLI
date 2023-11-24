# use base Ubuntu
FROM ubuntu:latest

# Avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Add "tester" user
RUN <<EOF
useradd -m -s /bin/bash -u 1000 tester
echo 'tester:testerpwd' | chpasswd
EOF

# Install vim, git and python, as I'll need it to clone DodonaCLI
RUN <<EOF
apt-get update && apt-get install -y git
apt-get install -y python3
apt-get install -y python3-pip
apt-get install -y vim
apt-get install -y sudo
apt-get install -y tmux
EOF

# Custom green prompt and dodona alias
RUN <<EOF
echo "PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /home/tester/.bashrc
echo 'alias dodona="python3 /home/tester/DodonaCLI/main.py $*"' >> /home/tester/.bashrc
EOF

# Install DodonaCLI
RUN <<EOF
git clone https://github.com/BWindey/DodonaCLI.git /home/tester/DodonaCLI
chown -R tester:tester /home/tester/DodonaCLI
EOF

# Switch to 'tester' user
USER tester
WORKDIR /home/tester/DodonaCLI

RUN pip install -r requirements.txt

WORKDIR /home/tester

# Default command to execute when container starts
CMD ["/bin/bash"]
