/* Verilog module written by vlog2Verilog (qflow) */
/* With explicit power connections */

module mux_using_if(
    inout vdd,
    inout gnd,
    input din_0,
    input din_1,
    output mux_out,
    input sel
);

wire _1_ ;
wire _0_ ;
wire mux_out ;
wire din_0 ;
wire din_1 ;
wire _2_ ;
wire sel ;

INVX1 _3_ (
    .gnd(gnd),
    .vdd(vdd),
    .A(din_0),
    .Y(_0_)
);

NAND2X1 _4_ (
    .gnd(gnd),
    .vdd(vdd),
    .A(din_1),
    .B(sel),
    .Y(_1_)
);

OAI21X1 _5_ (
    .gnd(gnd),
    .vdd(vdd),
    .A(sel),
    .B(_0_),
    .C(_1_),
    .Y(_2_)
);

BUFX2 _6_ (
    .gnd(gnd),
    .vdd(vdd),
    .A(_2_),
    .Y(mux_out)
);

endmodule
