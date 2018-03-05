import os

if "Jesse" in os.uname().nodename:
    data_dir = r"/Users/jesse/Data/SOC/2018-02-16 Tomografie/data"
    photo_dir_edited = r"/Users/jesse/Data/SOC/2018-02-16 Tomografie/gesorteerd bewerkt"
    photo_dir_orig = r"/Users/jesse/Data/SOC/2018-02-16 Tomografie/gesorteerd"
else:
    data_dir = r"Z:\projects\cigar\fototomografie en 3D printen\data"
    photo_dir_edited = r"Z:\projects\cigar\fototomografie en 3D printen\fotos\gesorteerd bewerkt"
    photo_dir_orig = r"Z:\projects\cigar\fototomografie en 3D printen\fotos\gesorteerd"

photo_edited_fn_format = os.path.join(photo_dir_edited, "plak_%03d_%s%d.JPG")
photo_orig_fn_format = os.path.join(photo_dir_orig, "plak_%03d_%s%d.JPG")
data_fn_format = os.path.join(data_dir, "data_plak_%03d_%s%d.npz")
cutout_fn_format = os.path.join(data_dir, "cutout_plak_%03d_%s%d.jpg")
cutout_selected_fn_format = os.path.join(data_dir, "selectie", "cutout_plak_%03d_%s%d.jpg")
rotated_fn_format = os.path.join(data_dir, "geroteerd", "rplak_%03d_%s%d.JPG")
normed_fn_format = os.path.join(data_dir, "genormeerd", "seq_nrplak_%s%03d.JPG")
blended_fn_format = os.path.join(data_dir, "geblend", "blended_nrplak_%s%06d.JPG")