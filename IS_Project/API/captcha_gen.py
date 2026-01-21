import random
import string
import base64
from io import BytesIO
from captcha.image import ImageCaptcha

def generate_visual_captcha():
    # Create random 6-character text
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Distort text into an image
    image_gen = ImageCaptcha(width=280, height=90)
    image_data = image_gen.generate(captcha_text)
    
    # Convert to base64 for JS
    base64_image = base64.b64encode(image_data.getvalue()).decode()
    return captcha_text, f"data:image/png;base64,{base64_image}"