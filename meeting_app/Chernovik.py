import os

print(os.path.abspath("meeting_app/app_backend/user_avatars/watermark.png"))

"""def add_watermark(input_image_path): #Добавление ватермарки на картинку
    base_image = Image.open(input_image_path)
    watermark = Image.open((os.path.abspath("app_backend/user_avatars/watermark.png"))).convert("RGBA")
    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0,0))
    transparent.paste(watermark, (0, 0), mask=watermark)
    transparent.save(input_image_path)
    return input_image_path"""