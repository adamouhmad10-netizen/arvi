import sys
from PIL import Image
im=Image.open(sys.argv[1]); y0=int(sys.argv[2]); h=int(sys.argv[3]) if len(sys.argv)>3 else 1100
im.crop((0,y0,im.width,min(im.height,y0+h))).save(sys.argv[4] if len(sys.argv)>4 else '/private/tmp/claude-501/-Users-adamm-Documents-shopify/9eec9230-be1e-42af-bc38-7c13628577a9/scratchpad/crop.png')
