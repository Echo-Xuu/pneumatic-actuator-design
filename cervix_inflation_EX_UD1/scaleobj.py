import meshio
import trimesh
import numpy as np

ori_stl = "LORIP45V2_UTCX_CD_UD1.STL"
out_stl = "LORIP45V2_UTCX_CD_UD1_out_only.STL"
scaled_obj = "LORIP45V2_UTCX_CD_UD1_scaled.obj"

#Removing the inner surface
 # 1. Load your mesh (STL, OBJ, etc.)
mesh = trimesh.load(ori_stl, force='mesh')
# 2. Split into connected sub‑meshes
components = mesh.split(only_watertight=False)
# 3. Pick the largest by surface area (i.e. the outer surface)
areas      = [m.area for m in components]
outer_mesh = components[np.argmax(areas)]
# 4. Export the result
outer_mesh.export(out_stl)
#Scaling
# Load the STL file
mesh = meshio.read(out_stl)     
# Define scale factor
scale = 0.001  
# Apply scaling to the points
mesh.points *= scale
# Write to OBJ
meshio.write(scaled_obj, mesh)