"""
This module containts constants that are for internal use only.
"""
from . import utils
from ostinato.core import ost_pb

class _Protocols(utils.Enum):

    """
    Enum for the available protocols
    """

    # Layer 1 protocols
    MAC                     = ost_pb.Protocol.kMacFieldNumber

    # Layer 2 protocols
    ETHERNET_II             = ost_pb.Protocol.kEth2FieldNumber
    ETHERNET_802_DOT_3      = ost_pb.Protocol.kDot3FieldNumber
    LLC                     = ost_pb.Protocol.kLlcFieldNumber
    SNAP                    = ost_pb.Protocol.kSnapFieldNumber
    SVLAN                   = ost_pb.Protocol.kSvlanFieldNumber
    VLAN                    = ost_pb.Protocol.kVlanFieldNumber
    VLAN_STACK              = ost_pb.Protocol.kVlanStackFieldNumber
    ETHERNET_802_DOT_2_LLC  = ost_pb.Protocol.kDot2LlcFieldNumber
    ETHERNET_802_DOT_2_SNAP = ost_pb.Protocol.kDot2SnapFieldNumber

    # Layer 3 protocols
    ARP                     = ost_pb.Protocol.kArpFieldNumber
    IP4                     = ost_pb.Protocol.kIp4FieldNumber
    IP6                     = ost_pb.Protocol.kIp6FieldNumber
    IP4_OVER_IP4            = ost_pb.Protocol.kIp4over4FieldNumber
    IP4_OVER_IP6            = ost_pb.Protocol.kIp4over6FieldNumber
    IP6_OVER_IP4            = ost_pb.Protocol.kIp6over4FieldNumber
    IP6_OVER_IP6            = ost_pb.Protocol.kIp6over6FieldNumber

    # Layer 4 protocols
    TCP                     = ost_pb.Protocol.kTcpFieldNumber
    UDP                     = ost_pb.Protocol.kUdpFieldNumber
    ICMP                    = ost_pb.Protocol.kIcmpFieldNumber
    IGMP                    = ost_pb.Protocol.kIgmpFieldNumber
    MLD                     = ost_pb.Protocol.kMldFieldNumber

    # Layer 5 protocols
    TEXT_PROTOCOL           = ost_pb.Protocol.kTextProtocolFieldNumber

    # Layer independant "protocols"
    PAYLOAD                 = ost_pb.Protocol.kPayloadFieldNumber
    SAMPLE                  = ost_pb.Protocol.kSampleFieldNumber
    USER_SCRIPT             = ost_pb.Protocol.kUserScriptFieldNumber
    HEX_DUMP                = ost_pb.Protocol.kHexDumpFieldNumber
