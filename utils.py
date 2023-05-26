import properties


def prepare_url(url):
    return url \
        if url.startswith(properties.BASE_DOMAIN) \
        else properties.BASE_DOMAIN_FORMAT.format(url)
