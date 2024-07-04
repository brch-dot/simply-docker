FROM iwaseyusuke/mininet  

# Install Open vSwitch
RUN apt-get update && \
    apt-get install -y openvswitch-switch openvswitch-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the entrypoint script and make it executable
COPY mininet_entrypoint.sh /home/btsonev/docker2/mininet_entrypoint.sh
RUN chmod +x /home/btsonev/docker2/mininet_entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/bin/bash", "/mininet_entrypoint.sh"]

