from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo

class CustomTopo(Topo):
    def build(self):
        switches = []
        for i in range(1, 120):
            switch = self.addSwitch(f's{i}')
            switches.append(switch)

        for i in range(0, 59):  
            self.addLink(switches[i], switches[2 * i + 1])
            self.addLink(switches[i], switches[2 * i + 2])

        middle_hosts = []
        middle_switches_indices = [29, 30, 31, 32]  

        for i, switch_index in enumerate(middle_switches_indices):
            host = self.addHost(f'h_middle_{i+1}')
            middle_hosts.append(host)
            self.addLink(host, switches[switch_index])

        bottom_hosts = []
        for i in range(7):
            host = self.addHost(f'h_bottom_{i+1}')
            bottom_hosts.append(host)
            self.addLink(host, switches[112 + i])

def clearFlows(net):
    for switch in net.switches:
        switch.cmd('ovs-ofctl del-flows', switch)

def addFlowRules(net):
    net.get('s113').cmd('ovs-ofctl add-flow s113 "ip,nw_src=10.0.0.1,nw_dst=10.0.0.7,actions=output:2"')
    net.get('s113').cmd('ovs-ofctl add-flow s113 "ip,nw_src=10.0.0.7,nw_dst=10.0.0.1,actions=output:1"')

    net.get('s1').cmd('ovs-ofctl add-flow s1 "ip,nw_src=10.0.0.1,nw_dst=10.0.0.7,actions=output:3"')
    net.get('s1').cmd('ovs-ofctl add-flow s1 "ip,nw_src=10.0.0.7,nw_dst=10.0.0.1,actions=output:1"')

    net.get('s119').cmd('ovs-ofctl add-flow s119 "ip,nw_src=10.0.0.1,nw_dst=10.0.0.7,actions=output:1"')
    net.get('s119').cmd('ovs-ofctl add-flow s119 "ip,nw_src=10.0.0.7,nw_dst=10.0.0.1,actions=output:2"')

def run():
    topo = CustomTopo()
    
    net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
    
    floodlight_controller = net.addController('floodlight', 
                                              controller=RemoteController, 
                                              ip='floodlight',  
                                              port=6653)
    
    net.start()
    
    addFlowRules(net)
   
    info("*** Flow rules for s113 ***\n")
    info(net.get('s113').cmd('ovs-ofctl dump-flows s113'))
    info("*** Flow rules for s1 ***\n")
    info(net.get('s1').cmd('ovs-ofctl dump-flows s1'))
    info("*** Flow rules for s119 ***\n")
    info(net.get('s119').cmd('ovs-ofctl dump-flows s119'))
    
    CLI(net)

if __name__ == '__main__':
    setLogLevel('info')
    run()

