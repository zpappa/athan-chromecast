import time
from uuid import UUID

import pychromecast

# List chromecasts on the network, but don't connect
from pychromecast import DeviceStatus
from pychromecast.controllers.media import MediaStatus
from pychromecast.controllers.receiver import CastStatus

services, browser = pychromecast.discovery.discover_chromecasts()
# Shut down discovery
pychromecast.discovery.stop_discovery(browser)

# Discover and connect to chromecasts named Living Room
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Basement speaker"])
#chromecasts, browser = pychromecast.get_chromecast_from_host("192.168.86.21")

cast = chromecasts[0]
# Start worker thread and wait for cast device to be ready
cast.wait()
print(cast.device)
#DeviceStatus(friendly_name='Living Room', model_name='Chromecast', manufacturer='Google Inc.', uuid=UUID('df6944da-f016-4cb8-97d0-3da2ccaa380b'), cast_type='cast', multizone_supported=True)

print(cast.status)
#CastStatus(is_active_input=True, is_stand_by=False, volume_level=1.0, volume_muted=False, app_id='CC1AD845', display_name='Default Media Receiver', namespaces=['urn:x-cast:com.google.cast.player.message', 'urn:x-cast:com.google.cast.media'], session_id='CCA39713-9A4F-34A6-A8BF-5D97BE7ECA5C', transport_id='web-9', status_text='', icon_url=None, volume_control_type=None)

mc = cast.media_controller
mc.play_media(url='https://drive.google.com/uc?export=download&id=1kC8afyTAJPTZm3RtmgSu2Io5mhTkNvNd', content_type='audio/mp3', )
mc.block_until_active()
print(mc.status)
# MediaStatus(content_id='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', content_type='video/mp4', duration=596.474195, stream_type='BUFFERED', idle_reason=None, media_session_id=1, playback_rate=1, player_state='PLAYING', supported_media_commands=15, volume_level=1, volume_muted=False)
#
# mc.pause()
# time.sleep(5)
# mc.play()

# Shut down discovery
pychromecast.discovery.stop_discovery(browser)
