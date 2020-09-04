v {xschem version=2.9.7 file_version=1.1}
G {}
V {}
S {}
E {}
N 250 520 440 520 {lab=a}
C {devices/lab_wire.sym} 250 520 0 0 {lab=a}
N 250 520 340 520 {lab=a}
N 340 520 340 600 {lab=a}
N 340 600 420 600 {lab=a}
C {devices/lab_wire.sym} 250 520 0 0 {lab=a}
N 560 500 620 500 {lab=_2_}
N 620 500 620 640 {lab=_2_}
N 620 640 690 640 {lab=_2_}
C {devices/lab_wire.sym} 560 500 0 0 {lab=_2_}
N 250 480 440 480 {lab=c}
C {devices/lab_wire.sym} 250 480 0 0 {lab=c}
N 250 480 340 480 {lab=c}
N 340 480 340 560 {lab=c}
N 340 560 420 560 {lab=c}
C {devices/lab_wire.sym} 250 480 0 0 {lab=c}
N 1060 620 1210 620 {lab=_4_}
C {devices/lab_wire.sym} 1060 620 0 0 {lab=_4_}
N 1290 620 1500 620 {lab=o}
C {devices/lab_wire.sym} 1290 620 0 0 {lab=o}
N 580 620 760 620 {lab=_0_}
N 760 620 760 600 {lab=_0_}
N 760 600 940 600 {lab=_0_}
C {devices/lab_wire.sym} 580 620 0 0 {lab=_0_}
N 810 620 880 620 {lab=_3_}
N 880 620 880 640 {lab=_3_}
N 880 640 940 640 {lab=_3_}
C {devices/lab_wire.sym} 810 620 0 0 {lab=_3_}
N 250 770 440 770 {lab=b}
C {devices/lab_wire.sym} 250 770 0 0 {lab=b}
N 250 770 340 770 {lab=b}
N 340 770 340 680 {lab=b}
N 340 680 420 680 {lab=b}
C {devices/lab_wire.sym} 250 770 0 0 {lab=b}
N 560 750 620 750 {lab=_1_}
N 620 750 620 600 {lab=_1_}
N 620 600 690 600 {lab=_1_}
C {devices/lab_wire.sym} 560 750 0 0 {lab=_1_}
N 250 730 440 730 {lab=d}
C {devices/lab_wire.sym} 250 730 0 0 {lab=d}
N 250 730 340 730 {lab=d}
N 340 730 340 640 {lab=d}
N 340 640 420 640 {lab=d}
C {devices/lab_wire.sym} 250 730 0 0 {lab=d}
C {osu035_xschem/NOR2X1.sym} 500 500 0 0 {name=X_7_ VCCPIN=vcc VSSPIN=gnd embed=true}
[
G {type=stdcell
vhdl_stop=true
verilog_stop=true
format="@name @pinlist @VCCPIN @VSSPIN @symname"
template="name=x1 VCCPIN=VCC VSSPIN=VSS"
generic_type="VCCPIN=string VSSPIN=string"
extra="VCCPIN VSSPIN"}
V {}
S {}
E {}
L 4 -60 -20 -25 -20 {}
L 4 -60 20 -25 20 {}
L 4 45 0 60 0 {}
L 4 -30 -30 -15 -30 {}
L 4 -30 30 -15 30 {}
B 5 57.5 -2.5 62.5 2.5 {name=Y dir=out verilog_type=wire}
B 5 -62.5 -22.5 -57.5 -17.5 {name=A dir=in}
B 5 -62.5 17.5 -57.5 22.5 {name=B dir=in}
A 4 40 0 5 0 360 {}
A 4 -77.5 0 56.18051263561058 327.7243556854224 64.55128862915524 {}
A 4 -21.07142857142857 36.78571428571428 67.06112046149408 33.26691584358777 51.53865524867743 {}
A 4 -21.07142857142857 -36.78571428571428 67.06112046149408 275.1944289077348 51.53865524867743 {}
T {@name} -16.25 -5 0 0 0.2 0.2 {}
T {@symname} -25 -45 0 0 0.2 0.2 {}
]
C {osu035_xschem/BUFX2.sym} 1250 620 0 0 {name=X_10_ VCCPIN=vcc VSSPIN=gnd embed=true}
[
G {type=stdcell
vhdl_stop=true
verilog_stop=true
format="@name @pinlist @VCCPIN @VSSPIN @symname"
template="name=x1 VCCPIN=VCC VSSPIN=VSS"
generic_type="VCCPIN=string VSSPIN=string"
extra="VCCPIN VSSPIN"}
V {}
S {}
E {}
L 4 -20 -20 -20 20 {}
L 4 -20 -20 20 0 {}
L 4 -20 20 20 0 {}
L 4 20 0 40 0 {}
L 4 -40 -0 -20 0 {}
B 5 37.5 -2.5 42.5 2.5 {name=Y dir=out verilog_type=wire}
B 5 -42.5 -2.5 -37.5 2.5 {name=A dir=in}
T {@name} 2.5 15 0 0 0.2 0.2 {}
T {@symname} 2.5 -25 0 0 0.2 0.2 {}
]
C {osu035_xschem/NAND2X1.sym} 1000 620 0 0 {name=X_9_ VCCPIN=vcc VSSPIN=gnd embed=true}
[
G {type=stdcell
vhdl_stop=true
verilog_stop=true
format="@name @pinlist @VCCPIN @VSSPIN @symname"
template="name=x1 VCCPIN=VCC VSSPIN=VSS"
generic_type="VCCPIN=string VSSPIN=string"
extra="VCCPIN VSSPIN"}
V {}
S {}
E {}
L 4 -60 -20 -30 -20 {}
L 4 -60 20 -30 20 {}
L 4 -30 -30 -30 30 {}
L 4 -30 30 5 30 {}
L 4 -30 -30 5 -30 {}
L 4 45 0 60 0 {}
B 5 57.5 -2.5 62.5 2.5 {name=Y dir=out verilog_type=wire}
B 5 -62.5 -22.5 -57.5 -17.5 {name=A dir=in}
B 5 -62.5 17.5 -57.5 22.5 {name=B dir=in}
A 4 5 0 30 270 180 {}
A 4 40 0 5 0 360 {}
T {@name} -28.75 -5 0 0 0.2 0.2 {}
T {@symname} -25 -45 0 0 0.2 0.2 {}
]
C {osu035_xschem/NOR2X1.sym} 500 750 0 0 {name=X_6_ VCCPIN=vcc VSSPIN=gnd embed=true}
[
G {type=stdcell
vhdl_stop=true
verilog_stop=true
format="@name @pinlist @VCCPIN @VSSPIN @symname"
template="name=x1 VCCPIN=VCC VSSPIN=VSS"
generic_type="VCCPIN=string VSSPIN=string"
extra="VCCPIN VSSPIN"}
V {}
S {}
E {}
L 4 -60 -20 -25 -20 {}
L 4 -60 20 -25 20 {}
L 4 45 0 60 0 {}
L 4 -30 -30 -15 -30 {}
L 4 -30 30 -15 30 {}
B 5 57.5 -2.5 62.5 2.5 {name=Y dir=out verilog_type=wire}
B 5 -62.5 -22.5 -57.5 -17.5 {name=A dir=in}
B 5 -62.5 17.5 -57.5 22.5 {name=B dir=in}
A 4 40 0 5 0 360 {}
A 4 -77.5 0 56.18051263561058 327.7243556854224 64.55128862915524 {}
A 4 -21.07142857142857 36.78571428571428 67.06112046149408 33.26691584358777 51.53865524867743 {}
A 4 -21.07142857142857 -36.78571428571428 67.06112046149408 275.1944289077348 51.53865524867743 {}
T {@name} -16.25 -5 0 0 0.2 0.2 {}
T {@symname} -25 -45 0 0 0.2 0.2 {}
]
C {osu035_xschem/NAND2X1.sym} 750 620 0 0 {name=X_8_ VCCPIN=vcc VSSPIN=gnd embed=true}
[
G {type=stdcell
vhdl_stop=true
verilog_stop=true
format="@name @pinlist @VCCPIN @VSSPIN @symname"
template="name=x1 VCCPIN=VCC VSSPIN=VSS"
generic_type="VCCPIN=string VSSPIN=string"
extra="VCCPIN VSSPIN"}
V {}
S {}
E {}
L 4 -60 -20 -30 -20 {}
L 4 -60 20 -30 20 {}
L 4 -30 -30 -30 30 {}
L 4 -30 30 5 30 {}
L 4 -30 -30 5 -30 {}
L 4 45 0 60 0 {}
B 5 57.5 -2.5 62.5 2.5 {name=Y dir=out verilog_type=wire}
B 5 -62.5 -22.5 -57.5 -17.5 {name=A dir=in}
B 5 -62.5 17.5 -57.5 22.5 {name=B dir=in}
A 4 5 0 30 270 180 {}
A 4 40 0 5 0 360 {}
T {@name} -28.75 -5 0 0 0.2 0.2 {}
T {@symname} -25 -45 0 0 0.2 0.2 {}
]
C {osu035_xschem/OAI22X1.sym} 500 620 0 0 {name=X_5_ VCCPIN=vcc VSSPIN=gnd embed=true}
[
G {type=stdcell
vhdl_stop=true
verilog_stop=true
format="@name @pinlist @VCCPIN @VSSPIN @symname"
template="name=x1 VCCPIN=VCC VSSPIN=VSS"
generic_type="VCCPIN=string VSSPIN=string"
extra="VCCPIN VSSPIN"}
V {}
S {}
E {}
L 4 -80 -60 -52.5 -60 {}
L 4 -80 -20 -52.5 -20 {}
L 4 67.5 0 80 0 {}
L 4 -57.5 -70 -50 -70 {}
L 4 -57.5 -10 -50 -10 {}
L 4 10 -30 27.5 -30 {}
L 4 10 -30 10 30 {}
L 4 10 30 27.5 30 {}
L 4 -80 20 -52.5 20 {}
L 4 -80 60 -52.5 60 {}
L 4 -57.5 10 -50 10 {}
L 4 -57.5 70 -50 70 {}
L 4 -5 -40 0 -40 {}
L 4 0 -40 -0 -20 {}
L 4 -0 -20 10 -20 {}
L 4 -5 40 0 40 {}
L 4 0 20 0 40 {}
L 4 0 20 10 20 {}
B 5 77.5 -2.5 82.5 2.5 {name=Y dir=out verilog_type=wire}
B 5 -82.5 -62.5 -77.5 -57.5 {name=A dir=in}
B 5 -82.5 -22.5 -77.5 -17.5 {name=B dir=in}
B 5 -82.5 17.5 -77.5 22.5 {name=C dir=in}
B 5 -82.5 57.5 -77.5 62.5 {name=D dir=in}
A 4 62.5 0 5 0 360 {}
A 4 -105 -40 56.18051263561058 327.7243556854224 64.55128862915524 {}
A 4 27.5 0 30 270 180 {}
A 4 -54.64285714285714 -14.28571428571428 55.90740340153566 27.38350663876661 57.85285167050722 {}
A 4 -54.64285714285714 -65.71428571428572 55.90740340153566 274.7636416907262 57.85285167050722 {}
A 4 -105 40 56.18051263561058 327.7243556854224 64.55128862915524 {}
A 4 -54.64285714285714 65.71428571428572 55.90740340153566 27.38350663876661 57.85285167050722 {}
A 4 -54.64285714285714 14.28571428571428 55.90740340153566 274.7636416907262 57.85285167050722 {}
T {@name} 15 -5 0 0 0.2 0.2 {}
T {@symname} -11.25 -65 0 0 0.2 0.2 {}
]
C {devices/ipin.sym} 250 520 0 0 {lab=a}
C {devices/ipin.sym} 250 770 0 0 {lab=b}
C {devices/ipin.sym} 250 480 0 0 {lab=c}
C {devices/ipin.sym} 250 730 0 0 {lab=d}
C {devices/opin.sym} 1500 620 0 0 {lab=o}
