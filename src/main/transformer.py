import rasterio
import rasterio.mask
from shapely.geometry import shape
import sys
import pickle
import geopandas as gpd


def extract_geometry(gdf_polygon, 
                     all_touched=False,
                     raster_path='./data/prep/transformed.tif'):
    # extract shapely midpoint
    geom = shape(gdf_polygon['geometry'].iloc[0])

    # re
    with rasterio.open(raster_path) as src:
        out_image, _ = rasterio.mask.mask(dataset=src,
                                          shapes=[geom],
                                          all_touched=all_touched, 
                                          crop=True)
        out_meta = src.meta

    return out_image, out_meta

def run_exctraction(current_date,
                    polygon_path='./data/shapes/Einzugsgebiete_NEW.shp'):
        
    polygon_gdf = gpd.read_file(polygon_path)
    polygon_gdf = polygon_gdf.reset_index(names='id_mapping')

    all_poly_info = {}
    for row_ in range(polygon_gdf.shape[0]):
        relevant_row = polygon_gdf.loc[polygon_gdf.id_mapping == row_]
        geometry, _ = extract_geometry(relevant_row)
        geometry = geometry.squeeze()

        all_poly_info[row_] = {}
        all_poly_info[row_]['sum'] = geometry.sum()
        all_poly_info[row_]['mean'] = geometry.mean()
        all_poly_info[row_]['std'] = geometry.std()
        all_poly_info[row_]['min'] = geometry.min()
        all_poly_info[row_]['max'] = geometry.max()

        all_poly_info[row_]['total'] = geometry.shape[0]*geometry.shape[1]
        all_poly_info[row_]['nonzero'] = (geometry > 0).sum()


    with open(f'data/results/{current_date}_processed.pkl', 'wb') as con_:
        pickle.dump(all_poly_info, con_)


if __name__ == '__main__':
    date_key = str(sys.argv[1])
    run_exctraction(current_date=date_key)