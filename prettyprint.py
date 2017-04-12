def able(value):
    return 'Enabled' if value else 'Disabled'


def on(value):
    return 'On' if value else 'Off'


def mouse_sensitivity(value):
    if value == .5:
        return 'Very Low'

    elif value == .75:
        return 'Low'

    elif value == 1:
        return 'Normal'

    elif value == 1.25:
        return 'High'

    elif value == 1.5:
        return 'Very High'


def screen_mode(value):
    return 'Fullscreen' if value else 'Windowed'