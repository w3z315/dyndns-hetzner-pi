import os

import miniupnpc
from dotenv import load_dotenv
from hetzner_dns_tools.record_list import record_list
from hetzner_dns_tools.record_create import record_create
from hetzner_dns_tools.record_delete import record_delete

load_dotenv()

ZONE_NAME = os.environ.get('HETZNER_DNS_ZONE_NAME')
RECORD_SUBDOMAIN = os.environ.get('HETZNER_DNS_RECORD_SUBDOMAIN')


def fetch_external_ipv4() -> str:
    """
    Fetches external ipv4 address using upnp
    :return str:
    """
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 200
    upnp.discover()
    upnp.selectigd()
    return upnp.externalipaddress()


def set_a_record_for_ip(ip_address: str):
    print(f'Getting list of records...')
    records = record_list(
        zone_name=os.environ.get('HETZNER_DNS_ZONE_NAME'),
    )
    existing_records = [record for record in records['records'] if
                        record['name'] == RECORD_SUBDOMAIN]
    # Delete old existing records
    if len(existing_records) > 0:
        print(f'Deleting old record.')
        record_delete(
            zone_name=ZONE_NAME,
            record_id=existing_records[0]['id'],
            record_type='A'
        )

    created_record = record_create(
        record_type='A',
        zone_name=ZONE_NAME,
        name=RECORD_SUBDOMAIN,
        ttl=3600,
        value=ip_address
    )
    print(
        f"Created record {created_record['record']['name']} with value {created_record['record']['value']} in {created_record['record']['zone_id']} at {created_record['record']['created']}")


if __name__ == '__main__':
    print('Fetching external ip...')
    external_ip = fetch_external_ipv4()
    print(f'External ip: {external_ip}')
    print('Setting dns records at hetzner...')
    set_a_record_for_ip(external_ip)
