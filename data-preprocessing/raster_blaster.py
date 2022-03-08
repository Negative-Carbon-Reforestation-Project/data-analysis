import pandas as pd
import arcpy
from arcpy import env

workspace = arcpy.GetParameterAsText(0)
arcpy.AddMessage("Workspace: " + workspace)
env.workspace = workspace

# Convert raster to point data

# Input raster - change to your desired raster
inRaster = arcpy.GetParameterAsText(1)
# Slicing to remove path
# inRaster = inRaster.rsplit("\\",1)[-1]
# Print output
arcpy.AddMessage("inRaster: " + inRaster)

# Output raster to point file - change to your desired point file name
outPoint = arcpy.GetParameterAsText(2)
# Slicing to remove path
# outPoint = outPoint.rsplit("\\",1)[-1]
arcpy.AddMessage("outPoint: " + outPoint)
# Field
field = "VALUE"

arcpy.RasterToPoint_conversion(inRaster, outPoint, field)

# Standardize grid_code to minimum/maximum normalized value

# Input layer for standardization
# inputFeature = outPoint[:-4]
inputFeature = outPoint

# Set the field(s) that will be standardized
field = "grid_code norm_value"

# Set the standardization method
method = "MIN-MAX"

arcpy.management.StandardizeField(inputFeature, field, method)

# Add lat and long fields to table

# inputFeature
field1 = "long"
field2 = "lat"
field_type = "DOUBLE"

arcpy.AddField_management(inputFeature, field1, field_type)
arcpy.AddField_management(inputFeature, field2, field_type)

# Calculate Geometry

# inputFeature
# Coordinate System

coord_system = arcpy.SpatialReference("USA Contiguous Albers Equal Area Conic USGS")
# Coordinate format = decimal degrees
coord_format = "DD"

arcpy.CalculateGeometryAttributes_management(inputFeature,
    [["long", "POINT_X"],
     ["lat", "POINT_Y"]],
    coordinate_system=coord_system,
    coordinate_format=coord_format)

# Convert table to CSV

# inputFeature = your input value defined earlier
df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(in_table=inputFeature,
    field_names=["long", "lat", "norm_value"]))
# output_name = "WA_" + inputFeature + "_stand_density.csv"
output_name = outPoint.rsplit("\\",1)[-1]
output_name = output_name[:-4] + ".csv"
output_name = workspace + "\\" + output_name
arcpy.AddMessage("output_name: " + output_name)
df.to_csv(output_name, index=False)