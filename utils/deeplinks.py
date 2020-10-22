import constants, requests


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


def construct_link_v2(link_type, email=None):
    link = f'{constants.FIREBASE_DEEPLINKS_PREFIX}' \
           f'?link={constants.FIREBASE_DEEPLINKS_LINK}' \
           f'&isi={constants.FIREBASE_DEEPLINKS_ISI}' \
           f'&ibi={constants.FIREBASE_DEEPLINKS_IBI}' \
           f'&efr={constants.FIREBASE_DEEPLINKS_EFR}' \
           f'&type={link_type}'
    if email:
        link += f'&email={email}'
    response = requests.post(
        constants.FIREBASE_SHORT_LINK_URL,
        json={
            "dynamicLinkInfo": {
                "dynamicLinkDomain": constants.FIREBASE_DEEPLINKS_DOMAIN,
                "link": link
            },
            "suffix": {
                "option": "UNGUESSABLE"
            }
        }
    )
    return response.json().get('shortLink')
