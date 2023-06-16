import xarray as xr

ds = xr.open_dataset('./resized/test.nc')
print(ds)

print(ds['CH4_column_volume_mixing_ratio_dry_air'].data.min())
print(ds['CH4_column_volume_mixing_ratio_dry_air'].data.max())