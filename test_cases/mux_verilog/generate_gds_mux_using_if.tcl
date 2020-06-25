drc off
box 0 0 0 0
gds readonly true
gds rescale false
gds read /usr/local/share/qflow/tech/osu035/osu035_stdcells.gds2
load mux_using_if
select top cell
expand
cif *hier write disable
cif *array write disable
gds write mux_using_if
quit
