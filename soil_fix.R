soil <- sol_chem.pnts_horizons
Encoding(soil) <- "latin1"
soil_fixed <- iconv(soil, "latin1", "UTF-8", sub='')
saveRDS(soil_fixed, "fixed_soil.rds")
print("Done!")