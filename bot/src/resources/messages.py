class Log:
    ready = "\033[92mLOG: bot is up and ready\033[0m"


class On:
    active = "I'm active now!"
    already_active = "Keep calm! I'm already active"


class Off:
    inactive = "I'm going to sleep now. See you!"
    already_inactive = "Don't disturb me while I'm sleeping!"


class SetTime:
    def success(self, minutes):
        return f"Ok I'm going to remind you every {minutes} minutes."

    failure = "I'm sorry but you didn't provide a proper time argument."


class Information:
    def message(self, name, minutes):
        return (
            f"Hi my name is {name}. I'm here to help you while you're working on your computer. Once you turn me"
            f" on I'm going to remind you every {minutes} minutes, or you can also tell me another "
            f"time, to either drink or stretch. This should help you to stay relaxed and healthy and thus "
            f"improve your productivity and well-being. I'm always happy to hear from you! :)"
        )


class HydrationMessages:
    message01 = "Do you feel like you need to hydrate?"


class StretchMessages:
    message01 = "It's time to stretch now!"
