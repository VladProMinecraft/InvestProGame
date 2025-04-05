# Центрує вікна

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    print(f"Screen width: {screen_width}, Screen height: {screen_height}")
    print(f"Window width: {width}, Window height: {height}")

    position_top = int(screen_height / 2 - height / 2)
    position_left = int(screen_width / 2 - width / 2)

    print(f"Position Top: {position_top}, Position Left: {position_left}")

    geometry_string = f'{width}x{height}+{position_left}+{position_top}'
    print(f"Geometry string: {geometry_string}")
    window.geometry(geometry_string)