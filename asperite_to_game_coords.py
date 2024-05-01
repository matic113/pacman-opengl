while True:
    coords = input("Enter coordinates from aseprite: ")
    x, y = coords.split(" ")
    new_x = 2 * int(x) + 4
    new_y = 496 - 2 * int(y) + 4

    print(f"New coordinates: {new_x}, {new_y}")
