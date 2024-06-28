use sampledata;
create table months ( id int PRIMARY KEY, name text );
create table seeds_data ( id int PRIMARY KEY,
    area_val double,
    perimeter_val double,
    compactness_val double,
    kernel_length_val double,
    kernel_width_val double,
    asymmetry_coeff_val double,
    kernel_groove_val double,
    type_val int
);