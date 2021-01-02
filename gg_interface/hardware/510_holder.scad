include <BOSL2/std.scad>
include <BOSL2/shapes.scad>
include <BOSL2/masks.scad>

tube_height = 80;
tube_ceiling_thickness = 5;
tube_inner_height = tube_height - tube_ceiling_thickness;
tube_outer_radius = 40;
tube_inner_radius = 30;
tube_thickness = tube_outer_radius - tube_inner_radius + 2;
cutout_dims = [15, 20];
510_outer_diameter = 22;
510_inner_diameter = 8;

/**
  * This object allows you to mount a female 510 connector securely to a table or other work surface.
  */

difference() {
    cylinder(r=tube_outer_radius, h=tube_height);
    cylinder(r=tube_inner_radius, h=tube_inner_height);
    up(tube_height) chamfer_cylinder_mask(r=tube_outer_radius, chamfer=10);
    up(tube_height - 1) cylinder(d=510_outer_diameter, h=1);
    up(tube_inner_height) cylinder(d=510_inner_diameter, h=tube_ceiling_thickness);
    
    translate([-cutout_dims[0] / 2, -tube_outer_radius, cutout_dims[1]]) rotate([-90, 0, 0]) hull() linear_extrude(tube_thickness) {
        square(cutout_dims);
        translate([cutout_dims[0] / 2, 0, 0]) circle(d=cutout_dims[0]);
    }
}
