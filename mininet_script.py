from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo

class CustomTopo(Topo):
    def build(self):
        # Add 119 switches in a tree structure
        switches = []
        for i in range(1, 120):
            switch = self.addSwitch(f's{i}')
            switches.append(switch)

        # Manually creating a tree structure by linking switches
        for i in range(0, 59):  # Linking 59 switches to their children
            self.addLink(switches[i], switches[2 * i + 1])
            self.addLink(switches[i], switches[2 * i + 2])

        # Add 4 hosts to different switches in the middle of the tree (e.g., switches 30 to 33)
        middle_hosts = []
        middle_switches_indices = [29, 30, 31, 32]  # Switches s30 to s33

        for i, switch_index in enumerate(middle_switches_indices):
            host = self.addHost(f'h_middle_{i+1}')
            middle_hosts.append(host)
            self.addLink(host, switches[switch_index])

        # Add 7 hosts to the very bottom of the tree (switches 113 to 119)
        bottom_hosts = []
        for i in range(7):
            host = self.addHost(f'h_bottom_{i+1}')
            bottom_hosts.append(host)
            self.addLink(host, switches[112 + i])

def clearFlows(net):
    for switch in net.switches:
        switch.cmd('ovs-ofctl del-flows', switch)

def addFlowRules(net):
    # Adding rules to allow traffic between h_bottom_1 (10.0.0.1) and h_bottom_7 (10.0.0.7)
    net.get('s113').cmd('ovs-ofctl add-flow s113 "ip,nw_src=10.0.0.1,nw_dst=10.0.0.7,actions=output:2"')
    net.get('s113').cmd('ovs-ofctl add-flow s113 "ip,nw_src=10.0.0.7,nw_dst=10.0.0.1,actions=output:1"')

    net.get('s1').cmd('ovs-ofctl add-flow s1 "ip,nw_src=10.0.0.1,nw_dst=10.0.0.7,actions=output:3"')
    net.get('s1').cmd('ovs-ofctl add-flow s1 "ip,nw_src=10.0.0.7,nw_dst=10.0.0.1,actions=output:1"')

    net.get('s119').cmd('ovs-ofctl add-flow s119 "ip,nw_src=10.0.0.1,nw_dst=10.0.0.7,actions=output:1"')
    net.get('s119').cmd('ovs-ofctl add-flow s119 "ip,nw_src=10.0.0.7,nw_dst=10.0.0.1,actions=output:2"')

def run():
    topo = CustomTopo()
    
    # Set up the Mininet network with the Floodlight controller
    net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
    
    # Add the Floodlight controller
    floodlight_controller = net.addController('floodlight', 
                                              controller=RemoteController, 
                                              ip='floodlight',  # Use service name as IP
                                              port=6653)
    
    # Start the network
    net.start()
    
    # Add flow rules for two-way communication between h_bottom_1 and h_bottom_7
    addFlowRules(net)
    
    # Verify flow rules
    info("*** Flow rules for s113 ***\n")
    info(net.get('s113').cmd('ovs-ofctl dump-flows s113'))
    info("*** Flow rules for s1 ***\n")
    info(net.get('s1').cmd('ovs-ofctl dump-flows s1'))
    info("*** Flow rules for s119 ***\n")
    info(net.get('s119').cmd('ovs-ofctl dump-flows s119'))
    
    # Start the CLI for interactive use
    CLI(net)
    
    # Clear flow rules before stopping the network
    clearFlows(net)
    
    # Stop the network when done

if __name__ == '__main__':
    setLogLevel('info')
    run()

