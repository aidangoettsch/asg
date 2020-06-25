gds vendor true ; gds rescale false ; gds read  /usr/local/share/qflow/tech/osu035/osu035_stdcells.gds2


 ; lef read  /usr/local/share/qflow/tech/osu035/osu035_stdcells.lef

def read mux_using_if
select top cell
expand
