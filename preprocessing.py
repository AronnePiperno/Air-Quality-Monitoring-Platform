import harp

filename = './data/S5P_OFFL_L2__CH4____20230530T002422_20230530T020552_29150_03_020500_20230531T162852.nc'

operations = ';'.join([
    "CH4_column_volume_mixing_ratio_dry_air_validity>50",
    "keep(latitude_bounds,longitude_bounds,CH4_column_volume_mixing_ratio_dry_air)",
    "derive(CH4_column_volume_mixing_ratio_dry_air [ppb])"
    #"derive(latitude {latitude})",
    #"derive(longitude {longitude})",
])

product = harp.import_product(filename, operations)
print(product)

product.to_xarray().to_netcdf('./resized/test.nc')