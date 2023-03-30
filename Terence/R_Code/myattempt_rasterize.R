library(sf)
library(raster)
library(rayshader)
library(stars)
library(remotes)
library(terra)
library(dplyr)

#install_version("sf", version = "1.0-11", repos = "http://cran.us.r-project.org")


# List the layers in the GeoPackage file
layers <- st_layers("/Users/antonglad/Master/Terence/geopackage_traffic.gpkg")

# Print the layer names and geometry types
cat("Layer names and geometry types:\n")
for (i in seq_along(layers$name)) {
  cat(paste0(layers$name[i], ": ", layers$geometry[i], "\n"))
}


# Read in the traffic dataset from the GeoPackage file
traffic <- st_read("/Users/antonglad/Master/Terence/geopackage_traffic.gpkg", layer = "trafikkmengde")

#Attempting to adjust the CRS
#traffic_transformed <- st_transform(traffic, crs = 4326)

# Select the desired columns
#selected_columns <- traffic %>% select(geom, SHAPE_Length, OBJECTID, adttotal)


# Rasterize the data (DOES NOT WORK: NA VALUES ASSIGNED TO EVERY GRID AFTER RASTERIZATION PROCESS, ADJUSTING RES DOES NOT CHANGE THE OUTCOME)
norway_raster <- st_rasterize(selected_columns, 
                              field = "adttotal",
                              res = 500,
                              crs = st_crs(traffic))

# Method 1:Convert the stars object to a raster object
#norway_raster_raster <- st_as_stars(norway_raster) %>% as_raster()

# Method 1:Convert the raster to a matrix: trying to replace this for now
#norway_matrix <- raster_to_matrix(norway_raster)

# Method 2: Convert the stars object to a GeoTIFF file
stars::write_stars(norway_raster, "norway_raster.tif")
# Method 2: Read the GeoTIFF file as a Raster object
norway_raster_raster <- raster::brick("norway_raster.tif")


# Replacement 1:Convert the stars object to a raster object
#norway_raster_raster <- st_as_stars(norway_raster) %>% stars::as_raster()

# AS MATRIX: Convert the raster to a matrix
norway_matrix <- as.matrix(norway_raster_raster)



# Create the 3D map (I HAVE NOT BEEN ABLE TO TEST BECAUSE THE DATA HAS NOT WORKED YET)
plot_3d(heightmap=norway_matrix, 
        zoom = 0.5, 
        scale = 1000, 
        phi = 45, 
        theta = -30)
