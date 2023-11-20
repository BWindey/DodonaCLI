# use base Ubuntu
FROM ubuntu:latest

# Avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Add "tester" user
RUN useradd -m -s /bin/bash -u 1000 tester
RUN echo 'tester:testerpwd' | chpasswd

# Install vim, git and python, as I'll need it to clone DodonaCLI
RUN apt-get update && apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y vim

# Custom green prompt and dodona alias
RUN echo "PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /home/tester/.bashrc
RUN echo 'alias dodona="python3 /home/tester/DodonaCLI/main.py $*"' >> /home/tester/.bashrc

# Install DodonaCLI
RUN git clone https://github.com/BWindey/DodonaCLI.git /home/tester/DodonaCLI
RUN chown -R tester:tester /home/tester/DodonaCLI

# Switch to 'tester' user
USER tester
WORKDIR /home/tester/DodonaCLI

RUN pip install -r requirements.txt

WORKDIR /home/tester

# Default command to execute when container starts
CMD ["/bin/bash"]