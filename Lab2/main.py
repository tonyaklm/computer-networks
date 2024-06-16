import os
import ipaddress
from icmplib import ping, exceptions
import ping3


def check_icmp_block(ip_address: str):
    try:
        response_time = ping3.ping(ip_address, timeout=1)
        if response_time is None:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return True


def mtu_discovery(target_address: str, min_size: int, max_size: int):
    global host
    while max_size > min_size + 1:
        mid_size = (max_size + min_size) // 2
        try:
            host = ping(target_address,
                        count=2,
                        payload_size=mid_size - 28,
                        interval=0.2,
                        timeout=1,
                        privileged=False)
        except exceptions.NameLookupError:
            print('Host cannot be resolved')
            exit(0)
        except exceptions.ICMPLibError as e:
            print('Error occurred: %s' % e)
            exit(1)
        if host.is_alive:
            print('MTU size %s is not enough' % mid_size)
            min_size = mid_size
        else:
            print('MTU size %s must be cut' % mid_size)
            max_size = mid_size
    return min_size


if __name__ == '__main__':
    target_address = os.getenv('ADDRESS', "localhost")
    min_size = os.getenv('MIN_SIZE', 0)
    max_size = os.getenv('MAX_SIZE', 6000)

    try:
        min_size = int(min_size)
        max_size = int(max_size)
    except ValueError:
        print('MIN_SIZE and MAX_SIZE must be integers')
        exit(0)
    if min_size < 0 or max_size < 0:
        print('MIN_SIZE and MAX_SIZE must be more than 0 or equal')
        exit(0)

    try:
        ip = ipaddress.ip_address(target_address)
        print('%s is a correct IP%s address.' % (ip, ip.version))
    except ValueError:
        print('Address/netmask is invalid: %s' % target_address)

    if check_icmp_block(target_address):
        print('ICMP is blocked for %s' % target_address)
        exit(0)

    print('MTU:', mtu_discovery(target_address, min_size, max_size))
