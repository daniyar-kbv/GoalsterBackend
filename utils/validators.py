import os
import constants, re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utils import response


def validate_file_size(value):
    if value.size > constants.MAX_REGULAR_FILE_SIZE:
        raise ValidationError(
            f'{_("Maximum file size is")}: {constants.MAX_REGULAR_FILE_SIZE/1000000}{_("Mb")}'
        )


def basic_validate_images(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in constants.IMAGE_EXTENSIONS:
        raise ValidationError(
            f'{_("Allowed extensions")}: {", ".join(constants.IMAGE_EXTENSIONS)}'
        )
