from bots.commands.base_command import BaseCommand

class PlaybackCommand(BaseCommand):

    @staticmethod
    def name():
        return "playback"

    def _validate(self):
        return True

    def _execute(self):
        print("LMAO")