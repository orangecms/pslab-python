import PSL.commands_proto as CP
from PSL import packet_handler
def check_calibration():
    H = packet_handler.Handler()
    H.__sendByte__(CP.FLASH)
    H.__sendByte__(CP.READ_BULK_FLASH)
    H.__sendInt__(38)
    H.__sendByte__(0)
    ss = H.fd.read(38)
    H.__get_ack__()
    return ss[:37]
check_calibration()
