from utils import title_to_permalink, request, load_cockpit, ensure_path, has_cockpit


def get_page_path(collection_name, entry):
    return "pages/{}/{}.md".format(collection_name, title_to_permalink(entry['title']))


def get_collection_data(cockpit, collection):
    endpoint = "{}/collections/get/{}?token={}".format(cockpit['api_endpoint'], collection,
                                                       cockpit['api_token'])
    return request(endpoint)


# TODO: this is gross... make it a recursive method
def generate_collection_files(collection_name, data):
    for entry in data['entries']:
        ensure_path("pages/{}".format(collection_name))
        filepath = get_page_path(collection_name, entry)

        with open(filepath, 'w') as page:
            for key, val in entry.items():
                # ignore metadata for now
                if not key.startswith("_"):
                    # if basic string the key: val
                    if type(val) is str:
                        page.write("{}: {}\n".format(key, val))
                    # if dict loop k, v to k: v
                    elif type(val) is dict:
                        page.write("{}:\n".format(key))
                        for k, v in val.items():
                            page.write("  {}: {}\n".format(k, v))
                    # if list loop list
                    elif type(val) is list:
                        page.write("{}:\n".format(key))
                        # prefix array value with -
                        for v in val:
                            if type(v) is str:
                                page.write("  - {}".format(v))
                            # if is dict write array line -
                            elif type(v) is dict:
                                page.write("  -\n")
                                for k, w in v.items():
                                    # if is dict tab twice then set a: b
                                    if type(w) is dict:
                                        for a, b in w.items():
                                            page.write("    {}: {}\n".format(a, b))
                                    else:
                                        # else write tab twice with k: w
                                        page.write("    {}: {}\n".format(k, w))


def fetch_data():
    if has_cockpit():
        cockpit = load_cockpit()

        if cockpit['collections']:
            for collection_name in cockpit['collections']:
                generate_collection_files(collection_name, get_collection_data(cockpit, collection_name))

        # TODO: add singletons and forms
        # if cockpit['singletons']:
        #     for singleton in cockpit['singletons']:
        #         print(singleton)
        #
        # if cockpit['forms']:
        #     for form in cockpit['forms']:
        #         print(form)
    else:
        return "skipping fetch_data, cockpit.json does not exist"
