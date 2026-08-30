import httpx

def download_file(url,out_path):
    with httpx.Client() as client:
        response = client.get(url)
        with open(out_path, 'wb+') as f:
            f.write(response.content)