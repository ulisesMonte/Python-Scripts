from mitmproxy import http


def response(packet):
    
    content_type = packet.response.headers.get("content-type")

    try:
        if "image" in content_type:
            url = packet.request.url
            extension = content_type.split("/")[-1]
            if extension == "jpeg":
                extension = "jpg"
            file_name = f"images/{url.replace("/","_").replace(":","_")}.{extension}"
            image_data = packet.response.content

            with open(file_name,"wb") as f:
                f.write(image_data)
    except: 
        pass