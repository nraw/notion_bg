from functools import partial


def text_handler(text, variable):
    update_dict = {variable: [{"text": {"content": text}}]}
    return update_dict


title_handler = partial(text_handler, variable="title")
rich_text_handler = partial(text_handler, variable="rich_text")


def number_handler(number):
    update_dict = {"number": number}
    return update_dict


def checkbox_handler(checkbox):
    update_dict = {"checkbox": checkbox}
    return update_dict


def multiselect_handler(multi):
    players_multi_select = [dict(name=str(p)) for p in multi]
    update_dict = {"multi_select": players_multi_select}
    return update_dict


def url_handler(variable):
    hyperlink = get_hyperlink(variable)
    update_dict = {"url": hyperlink}
    return update_dict


def get_hyperlink(yt_channel):
    if type(yt_channel) is dict:
        yt_url = f"[{yt_channel['title']}]({yt_channel['url']})"
    elif type(yt_channel) is str:
        yt_url = yt_channel
    else:
        yt_url = None
    return yt_url
