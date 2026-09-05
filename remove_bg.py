from PIL import Image
import os

def remove_white(image_path, output_path):
    if not os.path.exists(image_path):
        return
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        # If pixel is white or very close to white, make transparent
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    
    # Also crop the transparent borders to make them the same relative size
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, "PNG")
    print(f"Processed {output_path}")

remove_white('ps.png', 'ps_t.png')
remove_white('pr.png', 'pr_t.png')
remove_white('lightroom.png', 'lr_t.png')
remove_white('capcut.jpg', 'capcut_t.png')
