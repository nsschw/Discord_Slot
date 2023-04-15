from PIL import Image
import pandas as pd
import contextlib
from slot_machine import play

def plot_row(row):
  # Laden Sie die Bilder, die Sie zusammenfügen möchten
  col_1 = Image.open("Bilder/{}.png".format(row[0]))
  col_2 = Image.open("Bilder/{}.png".format(row[1]))
  col_3 = Image.open("Bilder/{}.png".format(row[2]))
  col_4 = Image.open("Bilder/{}.png".format(row[3]))
  col_5 = Image.open("Bilder/{}.png".format(row[4]))

  # Berechnen Sie die Größe des resultierenden Bildes
  widths, heights = zip(*(i.size for i in [col_1, col_2, col_3, col_4, col_5]))
  total_width = sum(widths)
  max_height = max(heights)

  # Erstellen Sie ein leeres Bild mit den berechneten Dimensionen
  result = Image.new("RGB", (total_width, max_height))

  # Fügen Sie die Bilder zusammen
  x_offset = 0
  for im in [col_1, col_2, col_3, col_4, col_5]:
    result.paste(im, (x_offset, 0), mask = im)
    x_offset += im.size[0]
  return result



def plot_image(bild, name):    
    row_1 = plot_row(bild.iloc[0])
    row_2 = plot_row(bild.iloc[1])
    row_3 = plot_row(bild.iloc[2])

    # Berechnen Sie die Größe des resultierenden Bildes
    widths, heights = zip(*(i.size for i in [row_1, row_2, row_3]))
    max_width = max(widths)
    total_height = sum(heights)

    # Erstellen Sie ein leeres Bild mit den berechneten Dimensionen
    result = Image.new("RGB", (max_width, total_height))

    # Fügen Sie die Bilder zusammen
    y_offset = 0
    for im in [row_1, row_2, row_3]:

      result.paste(im, (0, y_offset))
      y_offset += im.size[1]

    # Speichern Sie das resultierende Bild

    result = result.resize((max_width // 6, total_height // 6), Image.Resampling.LANCZOS)
    result.save("Bilder/Slot_Bilder/{}.png".format(name), "PNG")


def single_pic_with_line(bild, linie, name):
  bild = Image.open(f"Bilder/Slot_Bilder/{name}.png")
  linie_bild = Image.open(f"Bilder/linie_{linie}.png")
  bild.paste(linie_bild, (0, 0), linie_bild)
  bild.save(f"Bilder/Slot_Bilder/{linie}_{name}.png", "PNG")


def animate_image(bild = None, name = None, hitlinien=None):

  list_gif_imgs = []
  bild = Image.open(f"Bilder/Slot_Bilder/{name}.png")
  
  for linie in hitlinien:
    single_pic_with_line(bild, linie, name)
    list_gif_imgs.append(Image.open(f"Bilder/Slot_Bilder/{linie}_{name}.png")) 
  
  list_gif_imgs[0].save(f"Bilder/Slot_Bilder/{name}.gif", format='GIF', append_images=list_gif_imgs[1:], save_all=True, duration=500, loop=0, optimized=True)  



if __name__=='__main__':
  bild, reward = play()
  
  print(bild)
  plot_image(bild)