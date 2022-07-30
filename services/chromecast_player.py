from services.base_player import BasePlayer
import pychromecast


class ChromeCastPlayer(BasePlayer):

    def __init__(self, parameters={}):
        super(ChromeCastPlayer, self).__init__(parameters)

    def playAthan(self):
        services, browser = pychromecast.discovery.discover_chromecasts()
        # Shut down discovery
        pychromecast.discovery.stop_discovery(browser)

        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Basement speaker"])
        cast = chromecasts[0]
        cast.wait()
        mc = cast.media_controller
        mc.play_media(url=self.parameters.media_url,
                      content_type='audio/mp3', )
        #mc.block_until_active()
        pychromecast.discovery.stop_discovery(browser)
