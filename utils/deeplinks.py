import constants, requests


def construct_link(link_type, email=None):
    link = f'{constants.FIREBASE_DEEPLINKS_PREFIX}' \
           f'?link={constants.FIREBASE_DEEPLINKS_LINK}' \
           f'&isi={constants.FIREBASE_DEEPLINKS_ISI}' \
           f'&ibi={constants.FIREBASE_DEEPLINKS_IBI}' \
           f'&type={link_type}'
    if email:
        link += f'&email={email}'
    return link


def construct_link_v2(link_type, email=None):
    link = construct_link(link_type, email)
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


def construct_link_v3(link_type, email=None):
    link = f'{constants.FIREBASE_DEEPLINKS_LINK}/?type={link_type}'
    if email:
        link += f'&email={email}'
    response = requests.post(
        constants.FIREBASE_SHORT_LINK_URL,
        json={
            "dynamicLinkInfo": {
                "domainUriPrefix": constants.FIREBASE_DEEPLINKS_DOMAIN,
                "link": link,
                "iosInfo": {
                    "iosBundleId": constants.FIREBASE_DEEPLINKS_IBI,
                    "iosAppStoreId": constants.FIREBASE_DEEPLINKS_ISI
                },
                "navigationInfo": {
                    "enableForcedRedirect": False,
                },
            },
            "suffix": {
                "option": "UNGUESSABLE"
            }
        }
    )
    return response.json().get('shortLink')
