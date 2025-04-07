import meshio
import numpy as np

# Load the STL file
mesh = meshio.read("LORIP45V2_UTCX_CD.STL")  # replace with your STL path

# Define scale factor
scale = 0.001  

# Apply scaling to the points
mesh.points *= scale

# Write to OBJ
meshio.write("LORIP45V2_UTCX_CD_scaled.obj", mesh)