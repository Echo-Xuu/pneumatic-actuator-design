import igl
import numpy as np
import meshio
import math

def make_selections(volumetric_mesh_fname, volume_1_fname, volume_2_fname):
    mm = meshio.read(volumetric_mesh_fname)
    v = mm.points
    t = mm.cells_dict["tetra"]
    f = igl.boundary_facets(t)
    c = igl.facet_components(f)
    tet_barycenters = np.mean(v[t, :], axis=1)
    triangle_barycenters = np.mean(v[f, :], axis=1)
    #At the cervix, find: min y and x at min y (x lower bound), max x (x upper bound) and y at max x, and to the right of the slope = (max x - x at min y)/ (y at max x - min y)
    min_y = 46.4724
    x_at_min_y = 278.501
    max_x = 293.131
    y_at_max_x = 70.1934
    lower_x = round(x_at_min_y - 0.5, 1)
    upper_x = math.ceil(max_x)
    slope = (max_x - x_at_min_y)/ (y_at_max_x - min_y)

    dirichlet_selection = (triangle_barycenters[:, 0] > lower_x) & \
                      (triangle_barycenters[:, 0] < upper_x) & \
                      ((triangle_barycenters[:, 0] - x_at_min_y) / (triangle_barycenters[:, 1] - min_y) >= slope)

    with open("surface_selections.txt", "w") as file_:
        # Select inner surface and label as 2
        for i, j, k in f[c == 1]:
            file_.write(f"2 {i} {j} {k}\n")

        # Write dirichlet boundary as 1
        for idx in np.where(dirichlet_selection)[0]:  
            i, j, k = f[idx]
            file_.write(f"1 {i} {j} {k}\n")
        # Select outer surface and label as 3 (excluding Dirichlet)
        outer_surface_indices = np.where((c == 0) & ~dirichlet_selection)[0] 
        for idx in outer_surface_indices:
            i, j, k = f[idx]
            file_.write(f"3 {i} {j} {k}\n")

    volume_1 = meshio.read(volume_1_fname) 
    volume_2 = meshio.read(volume_2_fname)

    with open("volume_selections.txt", "w") as file_:
        w1 = igl.winding_number(volume_1.points.astype(np.double), volume_1.cells_dict["triangle"], tet_barycenters)
        w2 = igl.winding_number(volume_2.points.astype(np.double), volume_2.cells_dict["triangle"], tet_barycenters)
        volume_selections = np.zeros(t.shape[0], dtype=int) + 3
        volume_selections[w1 > 0.5] = 1
        volume_selections[w2 > 0.5] = 2

        print("First volume gets volume id 1")
        print("Second volume gets volume id 2")
        print(f"Found {(volume_selections == 3).sum()} tets outside these two volumes, giving them id 3")

        for i in volume_selections:
            file_.write(f"{i}\n")

if __name__ == "__main__":
    make_selections("LORIP45V1_UTCX_CD.msh", "LORIP45V1_CX_CD.STL", "LORIP45V1_UT_CD.STL")
