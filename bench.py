from pymaging import Image

Image.open_from_path('testimage.png').flip_left_right().save_to_path('benchimage.png')

