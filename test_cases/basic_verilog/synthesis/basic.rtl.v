/* Verilog module written by vlog2Verilog (qflow) */
/* With explicit power connections */

module basic(
    inout vdd,
    inout gnd,
    input a,
    inout gnd,
    output o,
    inout vdd
);

wire a ;
wire o ;
wire _0_ ;

INVX1 _1_ (
    .gnd(gnd),
    .vdd(vdd),
    .A(a),
    .Y(_0_)
);

BUFX2 _2_ (
    .gnd(gnd),
    .vdd(vdd),
    .A(_0_),
    .Y(o)
);

endmodule
