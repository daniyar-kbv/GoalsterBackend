import constants


def construct_link(link_type, email=None):
    link = f'{constants.FIREBASE_DEEPLINKS_PREFIX}' \
           f'?link={constants.FIREBASE_DEEPLINKS_LINK}' \
           f'&isi={constants.FIREBASE_DEEPLINKS_ISI}' \
           f'&ibi={constants.FIREBASE_DEEPLINKS_IBI}' \
           f'&efr={constants.FIREBASE_DEEPLINKS_EFR}' \
           f'&type={link_type}'
    if email:
        link += f'&email={email}'
    return link
