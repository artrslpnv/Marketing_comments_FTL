
import mimetypes


def get_video_w_h(file):
    """Returns image's width and height

    :param file: path to video
    :return: width, height
    """
    height = 1080
    width = 540
    return width, height


def is_video(file):
    mime = mimetypes.guess_type(file)[0]
    return mime in ['video/x-msvideo', 'video/mpeg', 'video/quicktime', 'video/x-sgi-movie', 'video/mp4',
                    'video/quicktime', 'video/webm']
