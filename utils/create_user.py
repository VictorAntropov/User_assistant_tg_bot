import base64
from datetime import datetime

import qrcode

from constants.information import PROJECT_DIR, PROJECT_UTF, QR
from core.db import AsyncSessionLocal
from models.users import User


async def create_user_in_db(user_info):
    created_qr = create_user_qrkod(user_info)
    user = User(
        chat_id=user_info['chat_id'],
        first_name=user_info['first_name'],
        second_name=user_info['second_name'],
        number=user_info['number'],
        company=user_info['company'],
        address=user_info['address'],
        email=user_info['email'],
        qr_kod=created_qr,
        created_at=datetime.now())
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()


def create_user_qrkod(user_info):
    data = f'BEGIN:VCARD\n' \
        f'VERSION:3.0\n' \
        f'N:{user_info["second_name"]};{user_info["first_name"]}\n' \
        f'TEL;TYPE=cell:{user_info["number"]}\n' \
        f'ORG:{user_info["company"]}\n' \
        f'ADR;TYPE=work: Россия, {user_info["address"]}\n'\
        f'EMAIL:{user_info["email"]}\n'\
        f'END:VCARD'\

    qr_kod = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
        )
    qr_kod.add_data(data)
    qr_kod.make(fit=True)
    img = qr_kod.make_image(fill_color='black', back_color='white')
    file_dir = f'{PROJECT_DIR}{user_info["number"]}_{QR}.png'
    img.save(file_dir)
    created_img = image_in_db(file_dir)
    return created_img


def image_in_db(img):
    with open(img, 'rb') as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        base64_string = base64_bytes.decode(PROJECT_UTF)
    return base64_string
