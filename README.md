# neosmartblinds

Neo Smart Blinds custom component for Home Assistant to enable Louvolite blinds to be automated

Simple component which allows ``cover.open`` and ``cover.close`` services. Not as fancy as [https://github.com/mtgeekman/Home_Assistant_NeoSmartBlinds](https://github.com/mtgeekman/Home_Assistant_NeoSmartBlinds) but does the job for me, and I wrote this before realising someone else had beaten me to it.

## Installation

Copy all files to the ``custom_components/neosmartblinds`` folder

## Configuration

Add the following lines to ``configuration.yaml``

cover:
  - platform: neosmartblinds
    id: ``id_of_your_hub``
    host: ``ip_address_of_hub``
    devices:
      ``blind1_id``:
        name: "friendly name in HA"
      ``blind2_id``:
        name: "friendly name in HA"

Hub and Blind IDs can be found in the neosmartblinds app