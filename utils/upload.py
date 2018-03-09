import imghdr
import random
import string

from PIL import Image


def get_random_name(length=25):
    y = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(25))
    return y


def avatar_upload(instance, filename):
    """
    Returns location to saved into. Relative to MEDIA_ROOT folder in settings.
    Location format = <avatars> / <phone> / <randomfilename>.
    """
    y = get_random_name()
    return u"avatars/{}/{}.{}".format(instance.phone, y, imghdr.what(instance.avatar))


def avatar_upload_v2(instance, filename):
    """
    """
    y = get_random_name()
    return u"avatars/{}/{}.{}".format(instance.phone, y, filename)


def certificate_upload(instance, filename):
    """
    Returns location to saved into. Relative to MEDIA_ROOT folder in settings.
    Location format = <person_id or business_id> / <certificates> / <randomfilename>.
    """
    y = get_random_name()
    format = imghdr.what(instance.certificate)
    if format is None:
        try:
            format = str(instance.certificate)[str(instance.certificate).rfind('.') + 1:]
        except:
            format = "unknown"
    try:
        return u"certificates/{}/{}.{}".format(instance.person_id or instance.business_id or '0', y,
                                               format)
    except:
        return u"certificates/{}/{}.{}".format(instance.pk, y,
                                               format)


def comfort_image_upload(instance, filename):
    """
    Returns location to saved into. Relative to MEDIA_ROOT folder in settings.
    Location format = <person_id or business_id> / <certificates> / <randomfilename>.
    """
    y = get_random_name()
    image_format = imghdr.what(instance.image)
    if image_format is None:
        try:
            image_format = str(instance.image)[str(instance.image).rfind('.') + 1:]
        except:
            image_format = "unknown"
    try:
        return u"comforts/{}/{}.{}".format(instance.pk, y, image_format)
    except:
        return u"comforts/{}.{}".format(y, image_format)


def certificate_upload_path(realtor, image):
    """
    """
    y = get_random_name()
    format = imghdr.what(image)
    if format is None:
        try:
            format = str(image)[str(image).rfind('.') + 1:]
        except:
            format = "unknown"
    try:
        return u"certificates/{}/{}.{}".format(realtor.pk, y,
                                               format)
    except:
        return u"certificates/{}/{}.{}".format(realtor.pk, y,
                                               format)


def space_image_upload(instance, filename):
    """
    Returns location to saved into. Relative to MEDIA_ROOT folder in settings.
    Location format =  /photos/ <owner_id> / <randomfilename>.
    """
    y = get_random_name()
    return u"photos/{}/{}.{}".format(instance.owner.phone, y, imghdr.what(instance.image))


def logo_upload_32x32(instance, filename):
    """
    Returns location to saved into. Relative to MEDIA_ROOT folder in settings.
    Location format =  /photos/ <owner_id> / <randomfilename>.
    """
    y = get_random_name()
    return u"logos/{}.{}".format(y, imghdr.what(instance.logo_32x32))


def logo_upload_64x64(instance, filename):
    """
    Returns location to saved into. Relative to MEDIA_ROOT folder in settings.
    Location format =  /photos/ <owner_id> / <randomfilename>.
    """
    y = get_random_name()
    return u"logos/{}.{}".format(y, imghdr.what(instance.logo_64x64))


def resize_image(obj, big):
    im = Image.open(obj.path)

    width, height = obj.width, obj.height

    thumb_size = 400, 400
    big_thumb_size = 800, 800

    if width > height:
       delta = width - height
       left = int(delta/2)
       upper = 0
       right = height + left
       lower = height
    else:
       delta = height - width
       left = 0
       upper = int(delta/2)
       right = width
       lower = width + upper

    im = im.crop((left, upper, right, lower))
    im.thumbnail(thumb_size, Image.ANTIALIAS)

    background = Image.new('RGB', thumb_size, (255, 255, 255, 0))
    background.paste(
        im, (int((thumb_size[0] - im.size[0]) / 2), int((thumb_size[1] - im.size[1]) / 2))
    )

    background.save(obj.path, quality=80)

    big_im = Image.open(big.path)
    big_im.thumbnail(big_thumb_size, Image.ANTIALIAS)
    big_im.save(big.path, quality=85)

