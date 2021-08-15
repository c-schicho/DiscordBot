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
    message02 = "A sip of water will keep your mind productive!"
    message03 = "Your body needs water to work properly. Take a sip!"
    message04 = "Your body might be lacking water."
    message05 = "Now is the right time. Grab a drink and take a sip!"


class StretchMessages:
    message01 = "It's time to stretch now!"
    message02 = "You're working hard, take a minute to stretch your body."
    message03 = "Time to activate your body! Stretch it!"
    message04 = "Refresh your mind, do some short stretching activities."
    message05 = "Some time passed by already, it's time to stretch now!"

