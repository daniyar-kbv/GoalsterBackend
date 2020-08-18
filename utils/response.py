def make_messages(messages=None):
    return {
        'messages': messages
    }


def make_errors(serializer):
    messages = []
    try:
        for key, value in serializer.errors.items():
            if isinstance(value, dict):
                for key2, value2 in value.items():
                    messages.append(f'{key2.capitalize()}: {value2[0]}')
            else:
                messages.append(f'{key.capitalize()}: {value[0]}')
        return make_messages(messages)
    except:
        return serializer.errors
