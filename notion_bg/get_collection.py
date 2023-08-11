from retry import retry


@retry(tries=10, delay=3, backoff=2)
def get_collection(bgg, **kwargs):
    collection = bgg.collection(**kwargs)
    return collection
